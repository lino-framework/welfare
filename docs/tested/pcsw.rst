.. _welfare.tested.pcsw:

General PCSW
============

.. include:: /include/tested.rst

.. 
  >>> from lino.runtime import *
  >>> from django.test import Client
  >>> import json

>>> ses = settings.SITE.login('rolf')
>>> ses.show(pcsw.UsersWithClients)
====================== ============ ============ ======= ======== ========= ================= ================= ========
 Begleiter              Auswertung   Ausbildung   Suche   Arbeit   Standby   Komplette Akten   Aktive Klienten   Total
---------------------- ------------ ------------ ------- -------- --------- ----------------- ----------------- --------
 Alicia Allmanns                                  2       2        1         4                 5                 7
 Hubert Huppertz        3            2            4       3        3         9                 15                22
 Mélanie Mélard         4            4            3       2        3         12                16                21
 **Total (3 Zeilen)**   **7**        **6**        **9**   **7**    **7**     **25**            **36**            **50**
====================== ============ ============ ======= ======== ========= ================= ================= ========
<BLANKLINE>


Printing UsersWithClients to pdf
--------------------------------

User problem report:

  | pdf-Dokument aus Startseite erstellen:
  | kommt leider nur ein leeres Dok-pdf bei raus auf den 30/09/2011 datiert

The following lines reproduced this problem 
(and passed when it was fixed):

>>> ses.spawn(pcsw.UsersWithClients).appy_render('tmp.odt')
>>> import os
>>> os.remove('tmp.odt')



Printing an eID card summary
----------------------------

>>> obj = pcsw.Client.objects.get(pk=123)
>>> from pprint import pprint
>>> pprint(ses.run(obj.print_eid_content)) #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/userdocs/appyodt/pcsw.Client-123.odt', 'success': True}



