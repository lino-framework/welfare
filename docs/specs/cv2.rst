.. _welfare.tested.cv2:
.. _welfare.specs.cv2:

=====================
Career (new version)
=====================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_cv2
    
    doctest init:
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.chatelet.settings.doctests'
    >>> from lino.api.doctest import *

A technical tour into the
:mod:`lino_welfare.projects.chatelet.modlib.cv` plugin.

Lino Welfare extends the standard :mod:`lino.modlib.cv` plugin 

.. contents::
   :depth: 2

    
>>> dd.today()
datetime.date(2014, 5, 22)


Configuration data
========================

This is the list of training types:

>>> rt.login('robin').show(cv.EducationLevels)
====================== ================== ================== ======= ===========
 Description            Description (de)   Description (en)   Étude   Formation
---------------------- ------------------ ------------------ ------- -----------
 Bachelor               Bachelor           Bachelor           Oui     Non
 Master                 Master             Master             Oui     Non
 Primaire               Primär             Primary            Oui     Non
 Secondaire             Sekundär           Secondary          Oui     Non
 Supérieur              Hochschule         Higher             Oui     Non
 **Total (5 lignes)**                                         **5**   **0**
====================== ================== ================== ======= ===========
<BLANKLINE>

And the list of Study types:

>>> rt.login('robin').show(cv.StudyTypes)
==== ======================= ==================== ================== ======= =========== ===================
 ID   Description             Description (de)     Description (en)   Étude   Formation   Niveau académique
---- ----------------------- -------------------- ------------------ ------- ----------- -------------------
 11   Alpha                   Alpha                Alpha              Non     Oui
 4    Apprentissage           Lehre                Apprenticeship     Oui     Non
 8    Cours à distance        Fernkurs             Remote study       Oui     Non
 7    Cours à temps partiel   Teilzeitunterricht   Part-time study    Oui     Non
 3    Formation               Ausbildung           Training           Oui     Non
 9    Préqualification        Prequalifying        Prequalifying      Non     Oui
 10   Qualification           Qualifying           Qualifying         Non     Oui
 6    Université              Universität          University         Oui     Non
 1    École                   Schule               School             Oui     Non
 2    École spéciale          Sonderschule         Special school     Oui     Non
 5    École supérieure        Hochschule           Highschool         Oui     Non
                                                                      **8**   **3**
==== ======================= ==================== ================== ======= =========== ===================
<BLANKLINE>


>>> for m, f in rt.modules.cv.StudyType._lino_ddh.fklist:
...     print dd.full_model_name(m), f.name
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
==== ================= ================== ==================
 ID   Description       Description (de)   Description (en)
---- ----------------- ------------------ ------------------
 1    Alcohol           Alkohol            Alcohol
 2    Santé             Gesundheit         Health
 3    Dettes            Schulden           Debts
 4    Family problems   Family problems    Family problems
==== ================= ================== ==================
<BLANKLINE>

>>> rt.show(cv.Obstacles)
==== ======================= ========== ================= ============= ============
 ID   Personne                Remarque   Type              Détecté par   Date
---- ----------------------- ---------- ----------------- ------------- ------------
 1    M. Luc FAYMONVILLE                 Alcohol                         22/05/2014
 2    M. Gregory GROTECLAES              Santé                           22/05/2014
 3    Mme Hildegard HILGERS              Dettes                          22/05/2014
 4    Mme Jacqueline JACOBS              Family problems                 22/05/2014
 5    M. Jérôme JEANÉMART                Alcohol                         22/05/2014
 6    M. Luc FAYMONVILLE                 Santé                           22/05/2014
 7    M. Gregory GROTECLAES              Dettes                          22/05/2014
 8    Mme Hildegard HILGERS              Family problems                 22/05/2014
 9    Mme Jacqueline JACOBS              Alcohol                         22/05/2014
 10   M. Jérôme JEANÉMART                Santé                           22/05/2014
 11   M. Luc FAYMONVILLE                 Dettes                          22/05/2014
 12   M. Gregory GROTECLAES              Family problems                 22/05/2014
 13   Mme Hildegard HILGERS              Alcohol                         22/05/2014
 14   Mme Jacqueline JACOBS              Santé                           22/05/2014
 15   M. Jérôme JEANÉMART                Dettes                          22/05/2014
 16   M. Luc FAYMONVILLE                 Family problems                 22/05/2014
 17   M. Gregory GROTECLAES              Alcohol                         22/05/2014
 18   Mme Hildegard HILGERS              Santé                           22/05/2014
 19   Mme Jacqueline JACOBS              Dettes                          22/05/2014
 20   M. Jérôme JEANÉMART                Family problems                 22/05/2014
==== ======================= ========== ================= ============= ============
<BLANKLINE>

>>> hildegard = pcsw.Client.objects.get(first_name="Hildegard")
>>> rt.login('robin').show(cv.ObstaclesByPerson, hildegard)
================= ============= ============ ==========
 Type              Détecté par   Date         Remarque
----------------- ------------- ------------ ----------
 Dettes                          22/05/2014
 Family problems                 22/05/2014
 Alcohol                         22/05/2014
 Santé                           22/05/2014
================= ============= ============ ==========
<BLANKLINE>
