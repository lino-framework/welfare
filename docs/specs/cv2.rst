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
cv.Training type
cv.Study type
isip.Contract study_type

>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get('rolf', 'choices/cv/Training/type', fields, 3, **kw)
>>> demo_get('rolf', 'choices/cv/Study/type', fields, 8, **kw)
>>> demo_get('rolf', 'choices/isip/Contract/study_type', fields, 11, **kw)
