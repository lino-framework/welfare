.. doctest docs/specs/welcht/cv2.rst
.. _welfare.specs.cv2:

=====================
Career (new version)
=====================

This document describes the
:mod:`lino_welcht.lib.cv` plugin, which
extends the standard :mod:`lino_xl.lib.cv` plugin.


>>> import lino
>>> lino.startup('lino_welfare.projects.mathieu.settings.doctests')
>>> from lino.api.doctest import *


.. contents::
   :depth: 2


>>> dd.today()
datetime.date(2014, 5, 22)


Configuration data
==================

This is the list of training types:

>>> rt.login('robin').show(cv.EducationLevels)
============= ================== ================== ======= ===========
 Désignation   Désignation (de)   Désignation (en)   Étude   Formation
------------- ------------------ ------------------ ------- -----------
 Bachelor      Bachelor           Bachelor           Oui     Non
 Master        Master             Master             Oui     Non
 Primaire      Primär             Primary            Oui     Non
 Secondaire    Sekundär           Secondary          Oui     Non
 Supérieur     Hochschule         Higher             Oui     Non
============= ================== ================== ======= ===========
<BLANKLINE>

And the list of Study types:

>>> rt.login('robin').show(cv.StudyTypes)
==== ======================= ==================== ================== ======= =========== ===================
 ID   Désignation             Désignation (de)     Désignation (en)   Étude   Formation   Niveau académique
---- ----------------------- -------------------- ------------------ ------- ----------- -------------------
 11   Alpha                   Alpha                Alpha              Non     Oui
 4    Apprentissage           Lehre                Apprenticeship     Oui     Non
 8    Cours à distance        Fernkurs             Remote study       Oui     Non
 7    Cours à temps partiel   Teilzeitunterricht   Part-time study    Oui     Non
 3    Formation               Ausbildung           Training           Oui     Non
 9    Préqualification        Préqualification     Prequalifying      Non     Oui
 10   Qualification           Qualification        Qualifying         Non     Oui
 6    Université              Universität          University         Oui     Non
 1    École                   Schule               School             Oui     Non
 2    École spéciale          Sonderschule         Special school     Oui     Non
 5    École supérieure        Hochschule           Highschool         Oui     Non
==== ======================= ==================== ================== ======= =========== ===================
<BLANKLINE>


>>> for m, f in rt.models.cv.StudyType._lino_ddh.fklist:
...     print ("{} {}".format(dd.full_model_name(m), f.name))
cv.Study type
cv.Training type
isip.Contract study_type

>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get('romain', 'choices/cv/Training/type', fields, 3, **kw)
>>> demo_get('romain', 'choices/cv/Study/type', fields, 8, **kw)
>>> demo_get('romain', 'choices/isip/Contract/study_type', fields, 11, **kw)


Obstacles
=========


>>> rt.show(cv.ObstacleTypes)
==== ===================== ===================== ==================
 ID   Désignation           Désignation (de)      Désignation (en)
---- --------------------- --------------------- ------------------
 1    Alcohol               Alkohol               Alcohol
 2    Santé                 Gesundheit            Health
 3    Dettes                Schulden              Debts
 4    Problèmes familiers   Problèmes familiers   Family problems
==== ===================== ===================== ==================
<BLANKLINE>

>>> rt.show(cv.Obstacles)
==== ======================= ========== ===================== ============= ============
 ID   Personne                Remarque   Type                  Détecté par   Date
---- ----------------------- ---------- --------------------- ------------- ------------
 1    M. Luc FAYMONVILLE                 Alcohol                             22/05/2014
 2    M. Gregory GROTECLAES              Santé                               22/05/2014
 3    Mme Hildegard HILGERS              Dettes                              22/05/2014
 4    Mme Jacqueline JACOBS              Problèmes familiers                 22/05/2014
 5    M. Jérôme JEANÉMART                Alcohol                             22/05/2014
 6    M. Luc FAYMONVILLE                 Santé                               22/05/2014
 7    M. Gregory GROTECLAES              Dettes                              22/05/2014
 8    Mme Hildegard HILGERS              Problèmes familiers                 22/05/2014
 9    Mme Jacqueline JACOBS              Alcohol                             22/05/2014
 10   M. Jérôme JEANÉMART                Santé                               22/05/2014
 11   M. Luc FAYMONVILLE                 Dettes                              22/05/2014
 12   M. Gregory GROTECLAES              Problèmes familiers                 22/05/2014
 13   Mme Hildegard HILGERS              Alcohol                             22/05/2014
 14   Mme Jacqueline JACOBS              Santé                               22/05/2014
 15   M. Jérôme JEANÉMART                Dettes                              22/05/2014
 16   M. Luc FAYMONVILLE                 Problèmes familiers                 22/05/2014
 17   M. Gregory GROTECLAES              Alcohol                             22/05/2014
 18   Mme Hildegard HILGERS              Santé                               22/05/2014
 19   Mme Jacqueline JACOBS              Dettes                              22/05/2014
 20   M. Jérôme JEANÉMART                Problèmes familiers                 22/05/2014
==== ======================= ========== ===================== ============= ============
<BLANKLINE>

>>> hildegard = pcsw.Client.objects.get(first_name="Hildegard")
>>> rt.login('robin').show(cv.ObstaclesByPerson, hildegard)
===================== ============= ============ ==========
 Type                  Détecté par   Date         Remarque
--------------------- ------------- ------------ ----------
 Dettes                              22/05/2014
 Problèmes familiers                 22/05/2014
 Alcohol                             22/05/2014
 Santé                               22/05/2014
===================== ============= ============ ==========
<BLANKLINE>

The list of :term:`activity sectors <activity sector>` is configurable via
:menuselection:`Configuration --> Career --> Activity sectors`.

>>> show_menu_path(cv.Sectors, language="en")
Configure --> Career --> Activity sectors
>>> show_menu_path(cv.Sectors, language="fr")
Configuration --> Parcours --> Secteurs d'activité

>>> rt.show(cv.Sectors)
==== ============================ ========================== ============================ ==========
 ID   Désignation                  Désignation (de)           Désignation (en)             Remarque
---- ---------------------------- -------------------------- ---------------------------- ----------
 14   Administration & Finance     Verwaltung & Finanzwesen   Administration & Finance
 1    Agriculture & horticulture   Landwirtschaft & Garten    Agriculture & horticulture
 4    Construction & bâtiment      Bauwesen & Gebäudepflege   Construction & buildings
 12   Cosmétique                   Kosmetik                   Esthetical
 10   Culture                      Kultur                     Cultural
 6    Enseignement                 Unterricht                 Education
 5    Horeca                       Horeca                     Tourism
 11   Informatique                 Informatik                 Information Technology
 2    Maritime                     Seefahrt                   Maritime
 3    Médical & paramédical        Medizin & Paramedizin      Medical & paramedical
 7    Nettoyage                    Reinigung                  Cleaning
 9    Textile                      Textil                     Textile
 8    Transport                    Transport                  Transport
 13   Vente                        Verkauf                    Sales
==== ============================ ========================== ============================ ==========
<BLANKLINE>

The list of :term:`job titles <job title>` is configurable via
:menuselection:`Configure --> Career --> Job titles`.

>>> show_menu_path(cv.Functions, language="en")
Configure --> Career --> Job titles

>>> show_menu_path(cv.Functions, language="fr")
Configuration --> Parcours --> Fonctions professionnelles

>>> rt.show(cv.Functions)
================ ================== ================== ====================
 Désignation      Désignation (de)   Désignation (en)   Secteur d'activité
---------------- ------------------ ------------------ --------------------
 Aide Cuisinier   Küchenassistent    Cook assistant     Horeca
 Cuisinier        Koch               Cook               Horeca
 Plongeur         Tellerwäscher      Dishwasher         Horeca
 Serveur          Kellner            Waiter             Horeca
================ ================== ================== ====================
<BLANKLINE>
