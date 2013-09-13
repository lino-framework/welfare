.. _welfare.tested.pcsw:

General PCSW
============

.. include:: /include/tested.rst

Some administrative stuff:

>>> from __future__ import print_function
>>> from lino.runtime import *
>>> from django.test import Client
>>> import json
>>> client = Client()

>>> ses = settings.SITE.login('rolf')
>>> ses.show(integ.UsersWithClients,language='de')
====================== ============ ============ ======= ======== ========= ================= ================= ========
 Begleiter              Auswertung   Ausbildung   Suche   Arbeit   Standby   Komplette Akten   Aktive Klienten   Total
---------------------- ------------ ------------ ------- -------- --------- ----------------- ----------------- --------
 Alicia Allmanns                     1                    1        1         2                 3                 5
 Hubert Huppertz        3            2            3       4        4         11                16                23
 Mélanie Mélard         4            4            2       2        3         12                15                20
 **Total (3 Zeilen)**   **7**        **7**        **5**   **7**    **8**     **25**            **34**            **48**
====================== ============ ============ ======= ======== ========= ================= ================= ========
<BLANKLINE>

Printing UsersWithClients to pdf
--------------------------------

User problem report:

  | pdf-Dokument aus Startseite erstellen:
  | kommt leider nur ein leeres Dok-pdf bei raus auf den 30/09/2011 datiert

The following lines reproduced this problem 
(and passed when it was fixed):

>>> url = 'http://127.0.0.1:8000/api/integ/UsersWithClients?an=as_pdf'
>>> res = client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result)
{u'open_url': u'/media/cache/appypdf/127.0.0.1/integ.UsersWithClients.pdf', u'success': True}




Printing an eID card summary
----------------------------

>>> obj = pcsw.Client.objects.get(pk=123)
>>> from pprint import pprint
>>> pprint(ses.run(obj.print_eid_content)) #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/userdocs/appyodt/pcsw.Client-123.odt', 'success': True}


And here another case (fixed :blogref:`20130827`) 
to test the new `eid_info` field:

>>> url = '/api/pcsw/Clients/176?an=detail&fmt=json'
>>> res = client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'navinfo', u'data', u'disable_delete', u'id', u'title']
>>> print(result['data']['eid_info'])
<div class="lino-info">Karte Nr. 591413288107 (Belgischer Staatsb&#252;rger), ausgestellt durch Eupen, g&#252;ltig von 19.08.11 bis 19.08.16</div>


>>> url = '/api/reception/Clients/115?an=detail&fmt=json'
>>> res = client.get(url,REMOTE_USER='rolf')
>>> result = json.loads(res.content)
>>> "Muss eID-Karte einlesen" in result['data']['client_info'][0]
True



