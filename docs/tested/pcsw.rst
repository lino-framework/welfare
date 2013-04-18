.. _welfare.tested.pcsw:

General PCSW
============

.. include:: /include/tested.rst

.. 
  >>> from lino.runtime import *

>>> ses = settings.SITE.login('rolf')
>>> ses.show(pcsw.UsersWithClients)
====================== ======= =========== =========== ========= ========= ================= ================= ========
 Begleiter              Bilan   Formation   Recherche   Travail   Standby   Komplette Akten   Aktive Klienten   Total
---------------------- ------- ----------- ----------- --------- --------- ----------------- ----------------- --------
 Alicia Allmanns                            2           2         1         4                 4                 7
 Hubert Huppertz        3       2           4           3         3         9                 12                22
 Mélanie Mélard         4       4           3           2         4         13                13                22
 **Total (3 Zeilen)**   **7**   **6**       **9**       **7**     **8**     **26**            **29**            **51**
====================== ======= =========== =========== ========= ========= ================= ================= ========
<BLANKLINE>


Printing
-----------------

>>> ses.spawn(pcsw.UsersWithClients).appy_render('tmp.odt')
>>> import os
>>> os.remove('tmp.odt')



