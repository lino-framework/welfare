.. _welfare.tested.integ:

===================
Integration Service
===================

.. How to test only this document:
    $ python setup.py test -s tests.DocsTests.test_integ
    
    Doctest initialization:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *

    >>> ses = rt.login('robin')
    >>> translation.activate('en')

A technical tour into the :mod:`lino_welfare.modlib.integ` module.
See also :doc:`/tour/autoevents`.

.. contents::
   :local:


Configuration
=============

>>> ses.show(isip.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== ===================== ===================== =========== ==================== ==================
 Designation           Designation (fr)      Designation (de)      Reference   Examination Policy   needs Study type
--------------------- --------------------- --------------------- ----------- -------------------- ------------------
 VSE Ausbildung        VSE Ausbildung        VSE Ausbildung        vsea        every month          Yes
 VSE Arbeitssuche      VSE Arbeitssuche      VSE Arbeitssuche      vseb        every month          No
 VSE Lehre             VSE Lehre             VSE Lehre             vsec        every month          No
 VSE Vollzeitstudium   VSE Vollzeitstudium   VSE Vollzeitstudium   vsed        every month          Yes
 VSE Sprachkurs        VSE Sprachkurs        VSE Sprachkurs        vsee        every month          No
 **Total (5 rows)**                                                                                 **2**
===================== ===================== ===================== =========== ==================== ==================
<BLANKLINE>


>>> ses.show(isip.ContractEndings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ======= =============== ========= ====================
 designation          ISIP    Job supplying   Success   Require date ended
-------------------- ------- --------------- --------- --------------------
 Alcohol              Yes     Yes             No        Yes
 Force majeure        Yes     Yes             No        Yes
 Health               Yes     Yes             No        Yes
 Normal               Yes     Yes             No        No
 **Total (4 rows)**   **4**   **4**           **0**     **3**
==================== ======= =============== ========= ====================
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
============= ================== ================== ===========
 Designation   Designation (fr)   Designation (de)   Reference
------------- ------------------ ------------------ -----------
 Default       Default            Standardwert
============= ================== ================== ===========
<BLANKLINE>

>>> ses.show(immersion.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== =========================== =====================
 Designation           Designation (fr)            Designation (de)
--------------------- --------------------------- ---------------------
 Immersion training    Stage d'immersion           Immersion training
 Internal engagement   Mise en situation interne   Internal engagement
 MISIP                 MISIP                       MISIP
===================== =========================== =====================
<BLANKLINE>

>>> ses.show(jobs.JobTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
======= ========= ================================================ ======== ================
 ID      Seq.No.   Designation                                      Remark   Social economy
------- --------- ------------------------------------------------ -------- ----------------
 4       4         Extern (Privat Kostenrückerstattung)                      No
 3       3         Extern (Öffentl. VoE mit Kostenrückerstattung)            No
 2       2         Intern                                                    No
 5       5         Sonstige                                                  No
 1       1         Sozialwirtschaft = "majorés"                              No
 **0**   **15**                                                              **0**
======= ========= ================================================ ======== ================
<BLANKLINE>



UsersWithClients
================

>>> ses.show(integ.UsersWithClients)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ============ =========== ======== ======= ========= ================= ================ ========
 Coach                Evaluation   Formation   Search   Work    Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- ------- --------- ----------------- ---------------- --------
 Alicia Allmanns      **2**        **2**       **1**    **1**   **1**     **3**             **7**            **7**
 Hubert Huppertz      **3**        **5**       **6**    **3**   **2**     **11**            **19**           **19**
 Mélanie Mélard       **4**        **1**       **4**    **5**   **4**     **11**            **18**           **18**
 **Total (3 rows)**   **9**        **8**       **11**   **9**   **7**     **25**            **44**           **44**
==================== ============ =========== ======== ======= ========= ================= ================ ========
<BLANKLINE>


Printing UsersWithClients to pdf
--------------------------------

User problem report:

  | pdf-Dokument aus Startseite erstellen:
  | kommt leider nur ein leeres Dok-pdf bei raus auf den 30/09/2011 datiert

The following lines reproduced this problem 
and passed when it was fixed:

>>> url = 'http://127.0.0.1:8000/api/integ/UsersWithClients?an=as_pdf'
>>> res = test_client.get(url, REMOTE_USER='rolf')  #doctest: +SKIP
>>> print(res.status_code)  #doctest: +SKIP
200
>>> result = json.loads(res.content)  #doctest: +SKIP
>>> print(result)  #doctest: +SKIP
{u'open_url': u'/media/cache/appypdf/127.0.0.1/integ.UsersWithClients.pdf', u'success': True}


Activity report
===============

>>> ses.show(integ.ActivityReport)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
------------
Introduction
------------
Ceci est un **rapport**,
càd un document complet généré par Lino, contenant des
sections, des tables et du texte libre.
Dans la version écran cliquer sur un chiffre pour voir d'où
il vient.
--------------------
Indicateurs généraux
--------------------
<BLANKLINE>
No data to display
<BLANKLINE>
.
<BLANKLINE>
No data to display
<BLANKLINE>
--------------------------------
Causes d'arrêt des interventions
--------------------------------
============================ ========= ======== ========== ======== ======== ========= ========= ======== ====== ======= ========== =======
 Description                  nicolas   alicia   caroline   hubert   judith   kerstin   melanie   romain   rolf   robin   theresia   Total
---------------------------- --------- -------- ---------- -------- -------- --------- --------- -------- ------ ------- ---------- -------
 Transfer to colleague
 End of right on social aid
 Moved to another town
 Found a job
============================ ========= ======== ========== ======== ======== ========= ========= ======== ====== ======= ========== =======
<BLANKLINE>
=====
ISIPs
=====
----------------------
PIIS par agent et type
----------------------
================= ================ ================== =========== ===================== ================ =======
 Description       VSE Ausbildung   VSE Arbeitssuche   VSE Lehre   VSE Vollzeitstudium   VSE Sprachkurs   Total
----------------- ---------------- ------------------ ----------- --------------------- ---------------- -------
 Alicia Allmanns
 Caroline Carnol
 Hubert Huppertz
 Judith Jousten
 Kerstin Kerres
 Mélanie Mélard
 nicolas
 Robin Rood
 Rolf Rompen
 Romain Raffault
 Theresia Thelen
================= ================ ================== =========== ===================== ================ =======
<BLANKLINE>
----------------------------------
Organisations externes et contrats
----------------------------------
Nombre de PIIS actifs par 
    organisation externe et type de contrat.
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
Nombre de PIIS actifs par 
    type de formation et type de contrat.
================ ================ ===================== =======
 Education Type   VSE Ausbildung   VSE Vollzeitstudium   Total
---------------- ---------------- --------------------- -------
 Apprenticeship
 Highschool
 School
 Special school
 Training
 University
================ ================ ===================== =======
<BLANKLINE>
=======================
Art60§7 job supplyments
=======================
-------------------------
Art60§7 par agent et type
-------------------------
================= ================ ============================ ======================= ============================ ====== =======
 Description       social economy   social economy - increased   social economy school   social economy with refund   town   Total
----------------- ---------------- ---------------------------- ----------------------- ---------------------------- ------ -------
 Alicia Allmanns
 Caroline Carnol
 Hubert Huppertz
 Judith Jousten
 Kerstin Kerres
 Mélanie Mélard
 nicolas
 Robin Rood
 Rolf Rompen
 Romain Raffault
 Theresia Thelen
================= ================ ============================ ======================= ============================ ====== =======
<BLANKLINE>
--------------------------
Job providers and contrats
--------------------------
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
=============== ================ ============================ ======================= ============================ ====== =======
 Description     social economy   social economy - increased   social economy school   social economy with refund   town   Total
--------------- ---------------- ---------------------------- ----------------------- ---------------------------- ------ -------
 Alcohol
 Force majeure
 Health
 Normal
=============== ================ ============================ ======================= ============================ ====== =======
<BLANKLINE>
