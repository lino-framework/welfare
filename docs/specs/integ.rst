.. _welfare.specs.integ:

===================
Integration Service
===================

.. How to test only this document:

    $ py.test -k test_integ

   NOTE (see blog 20161202) that this test fails when called like
   this::

    $ python setup.py test -s tests.SpecsTests.test_integ
    
    
    Doctest initialization:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *

    >>> ses = rt.login('robin')
    >>> translation.activate('en')

A technical tour into the :mod:`lino_welfare.modlib.integ` module.
See also :doc:`/tour/autoevents`.

Table of contents:

.. contents::
   :local:


Configuration
=============

>>> ses.show(isip.ContractEndings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=============== ====== =============== ========= ====================
 designation     ISIP   Job supplying   Success   Require date ended
--------------- ------ --------------- --------- --------------------
 Alcohol         Yes    Yes             No        Yes
 Force majeure   Yes    Yes             No        Yes
 Health          Yes    Yes             No        Yes
 Normal          Yes    Yes             No        No
=============== ====== =============== ========= ====================
<BLANKLINE>


>>> ses.show(jobs.Schedules)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== =========================== ========================= ===========================
 ID   Designation                 Designation (fr)          Designation (de)
---- --------------------------- ------------------------- ---------------------------
 1    5 days/week                 5 jours/semaine           5-Tage-Woche
 2    Individual                  individuel                Individuell
 3    Monday, Wednesday, Friday   lundi,mercredi,vendredi   Montag, Mittwoch, Freitag
==== =========================== ========================= ===========================
<BLANKLINE>

>>> ses.show(jobs.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================ =========================== =========================== ===========
 Designation                  Designation (fr)            Designation (de)            Reference
---------------------------- --------------------------- --------------------------- -----------
 social economy               économie sociale            Sozialökonomie              art60-7a
 social economy - increased   économie sociale - majoré   Sozialökonomie - majoré     art60-7b
 social economy school        avec remboursement école    mit Rückerstattung Schule   art60-7d
 social economy with refund   avec remboursement          mit Rückerstattung          art60-7c
 town                         ville d'Eupen               Stadt Eupen                 art60-7e
============================ =========================== =========================== ===========
<BLANKLINE>

>>> ses.show(art61.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================== ======================== =================== ===========
 Designation            Designation (fr)         Designation (de)    Reference
---------------------- ------------------------ ------------------- -----------
 Art61 job supplyment   Mise à l'emploi art.61   Art.61-Konvention
====================== ======================== =================== ===========
<BLANKLINE>

>>> ses.show(immersion.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== =========================== ===================== ==================== ================
 Designation           Designation (fr)            Designation (de)      Examination Policy   Template
--------------------- --------------------------- --------------------- -------------------- ----------------
 Immersion training    Stage d'immersion           Immersion training                         StageForem.odt
 Internal engagement   Mise en situation interne   Internal engagement                        Default.odt
 MISIP                 MISIP                       MISIP                                      Default.odt
===================== =========================== ===================== ==================== ================
<BLANKLINE>

>>> ses.show(jobs.JobTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== ======== ================================================ ======== ================
 ID   No.      Designation                                      Remark   Social economy
---- -------- ------------------------------------------------ -------- ----------------
 4    4        Extern (Privat Kostenrückerstattung)                      No
 3    3        Extern (Öffentl. VoE mit Kostenrückerstattung)            No
 2    2        Intern                                                    No
 5    5        Sonstige                                                  No
 1    1        Sozialwirtschaft = "majorés"                              No
      **15**
==== ======== ================================================ ======== ================
<BLANKLINE>



UsersWithClients
================

>>> ses.show(integ.UsersWithClients)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ============ =========== ======== ======= ========= ================= ================ ========
 Coach                Evaluation   Formation   Search   Work    Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- ------- --------- ----------------- ---------------- --------
 Alicia Allmanns      **2**        **2**       **1**    **1**   **1**     **3**             **3**            **7**
 Hubert Huppertz      **3**        **5**       **6**    **3**   **2**     **11**            **11**           **19**
 Mélanie Mélard       **4**        **1**       **4**    **5**   **4**     **11**            **11**           **18**
 **Total (3 rows)**   **9**        **8**       **11**   **9**   **7**     **25**            **25**           **44**
==================== ============ =========== ======== ======= ========= ================= ================ ========
<BLANKLINE>

Note that the numbers in this table depend on
:attr:`lino_welfare.modlib.integ.Plugin.only_primary` whose default
value is `False`.

>>> dd.plugins.integ.only_primary
False


Activity report
===============

>>> ses.show(integ.ActivityReport, stripped=True)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
------------
Introduction
------------
<BLANKLINE>
Ceci est un **rapport**,
càd un document complet généré par Lino, contenant des
sections, des tables et du texte libre.
Dans la version écran cliquer sur un chiffre pour voir d'où
il vient.
<BLANKLINE>
<BLANKLINE>
------------------------
Users with their Clients
------------------------
<BLANKLINE>
==================== ============ =========== ======== ======= ========= ================= ================ ========
 Coach                Evaluation   Formation   Search   Work    Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- ------- --------- ----------------- ---------------- --------
 Alicia Allmanns      **2**        **2**       **1**    **1**   **1**     **3**             **3**            **7**
 Hubert Huppertz      **3**        **5**       **6**    **3**   **2**     **11**            **11**           **19**
 Mélanie Mélard       **4**        **1**       **4**    **5**   **4**     **11**            **11**           **18**
 **Total (3 rows)**   **9**        **8**       **11**   **9**   **7**     **25**            **25**           **44**
==================== ============ =========== ======== ======= ========= ================= ================ ========
<BLANKLINE>
--------------------
Indicateurs généraux
--------------------
<BLANKLINE>
No data to display
.
<BLANKLINE>
No data to display
--------------------------------
Causes d'arrêt des interventions
--------------------------------
<BLANKLINE>
============================ ======== ======== ========= ========= ======== ====== ======= =======
 Description                  alicia   hubert   melanie   patrick   romain   rolf   robin   Total
---------------------------- -------- -------- --------- --------- -------- ------ ------- -------
 Transfer to colleague
 End of right on social aid
 Moved to another town
 Found a job
============================ ======== ======== ========= ========= ======== ====== ======= =======
<BLANKLINE>
=====
ISIPs
=====
<BLANKLINE>
----------------------
PIIS par agent et type
----------------------
<BLANKLINE>
================== ================ ================== =========== ===================== ================ =======
 Description        VSE Ausbildung   VSE Arbeitssuche   VSE Lehre   VSE Vollzeitstudium   VSE Sprachkurs   Total
------------------ ---------------- ------------------ ----------- --------------------- ---------------- -------
 Alicia Allmanns
 Caroline Carnol
 Hubert Huppertz
 Judith Jousten
 Kerstin Kerres
 Mélanie Mélard
 nicolas
 Patrick Paraneau
 Robin Rood
 Rolf Rompen
 Romain Raffault
 Theresia Thelen
 Wilfried Willems
================== ================ ================== =========== ===================== ================ =======
<BLANKLINE>
----------------------------------
Organisations externes et contrats
----------------------------------
<BLANKLINE>
======================== ================ ================== =========== ===================== ================ =======
 Organisation             VSE Ausbildung   VSE Arbeitssuche   VSE Lehre   VSE Vollzeitstudium   VSE Sprachkurs   Total
------------------------ ---------------- ------------------ ----------- --------------------- ---------------- -------
 Belgisches Rotes Kreuz
 Bäckerei Ausdemwald
 Bäckerei Mießen
 Bäckerei Schmitz
 Rumma & Ko OÜ
======================== ================ ================== =========== ===================== ================ =======
<BLANKLINE>
------------------------
Contract endings by type
------------------------
<BLANKLINE>
=============== ================ ================== =========== ===================== ================ =======
 Description     VSE Ausbildung   VSE Arbeitssuche   VSE Lehre   VSE Vollzeitstudium   VSE Sprachkurs   Total
--------------- ---------------- ------------------ ----------- --------------------- ---------------- -------
 Alcohol
 Force majeure
 Health
 Normal
=============== ================ ================== =========== ===================== ================ =======
<BLANKLINE>
--------------------------
PIIS et types de formation
--------------------------
<BLANKLINE>
================= ================ ===================== =======
 Education Type    VSE Ausbildung   VSE Vollzeitstudium   Total
----------------- ---------------- --------------------- -------
 Alpha
 Apprenticeship
 Highschool
 Part-time study
 Prequalifying
 Qualifying
 Remote study
 School
 Special school
 Training
 University
================= ================ ===================== =======
<BLANKLINE>
=======================
Art60§7 job supplyments
=======================
<BLANKLINE>
-------------------------
Art60§7 par agent et type
-------------------------
<BLANKLINE>
================== ================ ============================ ======================= ============================ ====== =======
 Description        social economy   social economy - increased   social economy school   social economy with refund   town   Total
------------------ ---------------- ---------------------------- ----------------------- ---------------------------- ------ -------
 Alicia Allmanns
 Caroline Carnol
 Hubert Huppertz
 Judith Jousten
 Kerstin Kerres
 Mélanie Mélard
 nicolas
 Patrick Paraneau
 Robin Rood
 Rolf Rompen
 Romain Raffault
 Theresia Thelen
 Wilfried Willems
================== ================ ============================ ======================= ============================ ====== =======
<BLANKLINE>
--------------------------
Job providers and contrats
--------------------------
<BLANKLINE>
================================ ================ ============================ ======================= ============================ ====== =======
 Organisation                     social economy   social economy - increased   social economy school   social economy with refund   town   Total
-------------------------------- ---------------- ---------------------------- ----------------------- ---------------------------- ------ -------
 BISA
 R-Cycle Sperrgutsortierzentrum
 Pro Aktiv V.o.G.
================================ ================ ============================ ======================= ============================ ====== =======
<BLANKLINE>
------------------------
Contract endings by type
------------------------
<BLANKLINE>
=============== ================ ============================ ======================= ============================ ====== =======
 Description     social economy   social economy - increased   social economy school   social economy with refund   town   Total
--------------- ---------------- ---------------------------- ----------------------- ---------------------------- ------ -------
 Alcohol
 Force majeure
 Health
 Normal
=============== ================ ============================ ======================= ============================ ====== =======
<BLANKLINE>


Printing UsersWithClients to pdf
--------------------------------

User problem report:

  | pdf-Dokument aus Startseite erstellen:
  | kommt leider nur ein leeres Dok-pdf bei raus auf den 30/09/2011 datiert

The following lines reproduced this problem 
and passed when it was fixed:

>>> settings.SITE.appy_params.update(raiseOnError=True)
>>> url = 'http://127.0.0.1:8000/api/integ/UsersWithClients?an=as_pdf'
>>> test_client.force_login(rt.login('rolf').user)
>>> res = test_client.get(url, REMOTE_USER='rolf')  #doctest: -SKIP
>>> print(res.status_code)  #doctest: -SKIP
200
>>> result = json.loads(res.content)  #doctest: -SKIP
>>> print(result)  #doctest: -SKIP
{u'open_url': u'/media/cache/appypdf/127.0.0.1/integ.UsersWithClients.pdf', u'success': True}


