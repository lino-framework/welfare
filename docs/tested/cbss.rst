.. _welfare.tested.cbss:

CBSS connection
===============

.. include:: /include/tested.rst

.. 
  >>> from lino.runtime import *

We retrieve Tx25 no. 1 from the database:

>>> obj = cbss.RetrieveTIGroupsRequest.objects.get(pk=1)
>>> obj
RetrieveTIGroupsRequest #1 (u'Tx25-Anfrage #1')

So far this was standard Django API. To use Lino's extended API we 
first need to "log in" as user `rolf` 
using the :meth:`login <lino.ui.Site.login>` method:

>>> ses = settings.SITE.login('rolf')

Here is the textual representation of the "Result" panel 
(only the first lines, this is just a test after all):

>>> ses.show(cbss.RetrieveTIGroupsResult.request(obj,limit=5))
====================== ===== ========== ==================================================
 Gruppe                 TI    Seit       Information
---------------------- ----- ---------- --------------------------------------------------
 NR-Nummer                    02.07.68   **68070201351** (Männlich)
 Wohnsitze              001   18.10.01   **Estland** (136), Fusion: **0**, Sprache: **2**
                              02.07.68   **Eupen** (63023), Fusion: **0**, Sprache: **2**
 Namen                  010   02.07.68   **Mustermann**, Max Moritz
 Legale Hauptadressen   020   30.07.97   **4700**, **Gülcherstrasse**, Nr. **21**
====================== ===== ========== ==================================================
<BLANKLINE>


Printing a Tx25
-----------------

>>> from pprint import pprint
>>> pprint(ses.run(obj.print_action)) #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/userdocs/appyodt/cbss.RetrieveTIGroupsRequest-1.odt',
 'success': True}


