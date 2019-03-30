.. doctest docs/specs/welcht/integ.rst
.. _welfare.specs.integ:

===================
Integration Service
===================

This document describes the :mod:`lino_welfare.modlib.integ` plugin.
See also :ref:`welfare.specs.autoevents`.

.. currentmodule:: lino_welfare.modlib.integ
                   

Table of contents:

.. contents::
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_welfare.projects.mathieu.settings.doctests')
>>> from lino.api.doctest import *

>>> ses = rt.login('robin')
>>> translation.activate('en')
>>> ses.get_user().user_type.hidden_languages = None

Note that we set :attr:`lino.modlib.users.UserType.hidden_languages`
to `None` because in this document we want to see the other languages
as well.

      


Configuration
=============


>>> ses.show(isip.ContractEndings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=============== ====== =============== ========= ====================
 Designation     ISIP   Job supplying   Success   Require date ended
--------------- ------ --------------- --------- --------------------
 Alcohol         Yes    Yes             No        Yes
 Force majeure   Yes    Yes             No        Yes
 Normal          Yes    Yes             No        No
 Santé           Yes    Yes             No        Yes
=============== ====== =============== ========= ====================
<BLANKLINE>

Note that designations are in French because that's the main language
and because :attr:`lino_welfare.modlib.isip.ContractEnding.name` is
not a babel field.

>>> print(settings.SITE.get_default_language())
fr


>>> ses.show(jobs.Schedules)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== ========================= ================== =========================== ===========================
 ID   Designation               Designation (nl)   Designation (de)            Designation (en)
---- ------------------------- ------------------ --------------------------- ---------------------------
 1    5 jours/semaine                              5-Tage-Woche                5 days/week
 2    individuel                                   Individuell                 Individual
 3    lundi,mercredi,vendredi                      Montag, Mittwoch, Freitag   Monday, Wednesday, Friday
==== ========================= ================== =========================== ===========================
<BLANKLINE>


>>> ses.show(jobs.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================== ================== =========================== ============================ ===========
 Designation                 Designation (nl)   Designation (de)            Designation (en)             Reference
--------------------------- ------------------ --------------------------- ---------------------------- -----------
 avec remboursement                             mit Rückerstattung          social economy with refund   art60-7c
 avec remboursement école                       mit Rückerstattung Schule   social economy school        art60-7d
 ville d'Eupen                                  Stadt Eupen                 town                         art60-7e
 économie sociale                               Sozialökonomie              social economy               art60-7a
 économie sociale - majoré                      Sozialökonomie - majoré     social economy - increased   art60-7b
=========================== ================== =========================== ============================ ===========
<BLANKLINE>

>>> ses.show(art61.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
======================== ======================== =================== ====================== ===========
 Designation              Designation (nl)         Designation (de)    Designation (en)       Reference
------------------------ ------------------------ ------------------- ---------------------- -----------
 Mise à l'emploi art.61   Mise à l'emploi art.61   Art.61-Konvention   Art61 job supplyment
======================== ======================== =================== ====================== ===========
<BLANKLINE>

>>> ses.show(immersion.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================== =========================== =========================== ===================== ==================== ================
 Designation                 Designation (nl)            Designation (de)            Designation (en)      Examination Policy   Template
--------------------------- --------------------------- --------------------------- --------------------- -------------------- ----------------
 MISIP                       MISIP                       MISIP                       MISIP                                      Default.odt
 Mise en situation interne   Mise en situation interne   Mise en situation interne   Internal engagement                        Default.odt
 Stage d'immersion           Stage d'immersion           Stage d'immersion           Immersion training                         StageForem.odt
=========================== =========================== =========================== ===================== ==================== ================
<BLANKLINE>

>>> ses.show(jobs.JobTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== ===== ================================================ ======== ================
 ID   No.   Designation                                      Remark   Social economy
---- ----- ------------------------------------------------ -------- ----------------
 4    4     Extern (Privat Kostenrückerstattung)                      No
 3    3     Extern (Öffentl. VoE mit Kostenrückerstattung)            No
 2    2     Intern                                                    No
 5    5     Sonstige                                                  No
 1    1     Sozialwirtschaft = "majorés"                              No
==== ===== ================================================ ======== ================
<BLANKLINE>



UsersWithClients
================

>>> ses.show(integ.UsersWithClients)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ============ =========== ======== ========= ========= ================= ================ ========
 Coach                Évaluation   Formation   Search   Travail   Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- --------- --------- ----------------- ---------------- --------
 Alicia Allmanns      **1**        **1**                          **1**     **3**             **3**            **7**
 Hubert Huppertz      **1**        **3**       **4**    **2**     **1**     **11**            **11**           **19**
 Mélanie Mélard       **2**                    **2**    **4**     **3**     **11**            **11**           **18**
 **Total (3 rows)**   **4**        **4**       **6**    **6**     **5**     **25**            **25**           **44**
==================== ============ =========== ======== ========= ========= ================= ================ ========
<BLANKLINE>

Note that the numbers in this table depend on
:attr:`lino_welfare.modlib.integ.Plugin.only_primary` whose default
value is `False`.

>>> dd.plugins.integ.only_primary
True


Activity report
===============

>>> translation.activate('en')
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
==================== ============ =========== ======== ========= ========= ================= ================ ========
 Coach                Évaluation   Formation   Search   Travail   Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- --------- --------- ----------------- ---------------- --------
 Alicia Allmanns      **1**        **1**                          **1**     **3**             **3**            **7**
 Hubert Huppertz      **1**        **3**       **4**    **2**     **1**     **11**            **11**           **19**
 Mélanie Mélard       **2**                    **2**    **4**     **3**     **11**            **11**           **18**
 **Total (3 rows)**   **4**        **4**       **6**    **6**     **5**     **25**            **25**           **44**
==================== ============ =========== ======== ========= ========= ================= ================ ========
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
================== ================ ================== =========== ===================== ================ =======
<BLANKLINE>
----------------------------------
Organisations externes et contrats
----------------------------------
<BLANKLINE>
======================== ================ ================== =========== ===================== ================ =======
 Organization             VSE Ausbildung   VSE Arbeitssuche   VSE Lehre   VSE Vollzeitstudium   VSE Sprachkurs   Total
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
 Normal
 Santé
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
 Remote study
 Part-time study
 Training
 Prequalifying
 Qualifying
 University
 School
 Special school
 Highschool
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
================== ==================== ========================== =============== ================== =========================== =======
 Description        avec remboursement   avec remboursement école   ville d'Eupen   économie sociale   économie sociale - majoré   Total
------------------ -------------------- -------------------------- --------------- ------------------ --------------------------- -------
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
================== ==================== ========================== =============== ================== =========================== =======
<BLANKLINE>
--------------------------
Job providers and contrats
--------------------------
<BLANKLINE>
================================ ==================== ========================== =============== ================== =========================== =======
 Organization                     avec remboursement   avec remboursement école   ville d'Eupen   économie sociale   économie sociale - majoré   Total
-------------------------------- -------------------- -------------------------- --------------- ------------------ --------------------------- -------
 BISA
 R-Cycle Sperrgutsortierzentrum
 Pro Aktiv V.o.G.
================================ ==================== ========================== =============== ================== =========================== =======
<BLANKLINE>
------------------------
Contract endings by type
------------------------
<BLANKLINE>
=============== ==================== ========================== =============== ================== =========================== =======
 Description     avec remboursement   avec remboursement école   ville d'Eupen   économie sociale   économie sociale - majoré   Total
--------------- -------------------- -------------------------- --------------- ------------------ --------------------------- -------
 Alcohol
 Force majeure
 Normal
 Santé
=============== ==================== ========================== =============== ================== =========================== =======
<BLANKLINE>


Printing UsersWithClients to pdf
================================

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
>>> result = json.loads(res.content.decode())  #doctest: -SKIP
>>> print(result['open_url']) #doctest: +ELLIPSIS +REPORT_UDIFF +NORMALIZE_WHITESPACE
/media/cache/appypdf/127.0.0.1/integ.UsersWithClients.pdf
>>> print(result['success']) #doctest: +ELLIPSIS +REPORT_UDIFF +NORMALIZE_WHITESPACE
True



The following reproduces a bug we discovered on 20180921.
It was not possible to sort reverse on a column with a virtual field.

>>> # url = "/api/integ/Clients?_dc=1537533953315&start=0&limit=33&fmt=json&rp=ext-comp-1251"
>>> url += "&pv=30&pv=200125&pv=&pv=21.09.2018&pv=21.09.2018&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=1&pv=false&pv=false&sort=applies_until&dir=DESC"
>>> url = "/api/integ/Clients?_dc=1541013238935&start=0&limit=12&fmt=json&rp=ext-comp-1497&pv=30&pv=6&pv=&pv=&pv=&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=false&pv=false&sort=applies_until&dir=DESC"

>>> res = test_client.get(url, REMOTE_USER='rolf')  #doctest: -SKIP
>>> print(res.status_code)  #doctest: -SKIP
200


Don't read me
=============

Verify that :ticket:`2784` is fixed:

>>> for ba in integ.ActivityReport.get_actions():
...     if ba.action.is_window_action():
...         print(ba)
<BoundAction(integ.ActivityReport, <lino.core.actions.ShowEmptyTable show ('D\xe9tail')>)>


