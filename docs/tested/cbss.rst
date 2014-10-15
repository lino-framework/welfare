.. _welfare.tested.cbss:

CBSS connection
===============

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_cbss

.. 
  >>> from lino.runtime import *
  >>> from django.utils import translation

The examples in this document are in German:

>>> translation.activate('de')

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

>>> with translation.override('de'):
...    ses.show(cbss.RetrieveTIGroupsResult.request(obj,limit=5))
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


>>> rv = ses.run(obj.do_print)
>>> print(rv['success'])
True
>>> print(rv['open_url'])
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/.../cbss.RetrieveTIGroupsRequest-1.odt




