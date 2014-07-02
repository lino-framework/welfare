.. _welfare.tested.jobs:

Jobs
===============

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_jobs

..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.docs.settings.test'
    >>> from django.utils import translation
    >>> from lino.runtime import *
    >>> from lino.utils.instantiator import i2d
    >>> from django.test import Client
    >>> import json

We log in as Rolf:

>>> ses = settings.SITE.login('rolf')

We switch to German because the first PCSW with Lino was the one in Eupen:

>>> translation.activate('de')


.. _welfare.jobs.Offers:

Job Offers
----------


>>> # settings.SITE.catch_layout_exceptions = False
>>> jobs.Offers.show() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ========================== ========== ======================== ======================== ================ ============== =============
 ID   Sektor                     Funktion   Name                     Stellenanbieter          Beginn Auswahl   Ende Auswahl   Beginndatum
---- -------------------------- ---------- ------------------------ ------------------------ ---------------- -------------- -------------
 1     Landwirtschaft & Garten   Kellner    Übersetzer DE-FR (m/w)   Pro Aktiv V.o.G. (...)   ...              ...            ...     
==== ========================== ========== ======================== ======================== ================ ============== =============
<BLANKLINE>


.. _welfare.jobs.ExperiencesByOffer:

Experiences by Job Offer
------------------------

This table shows the Experiences which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.ExperiencesByOffer.request(obj)) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
========== ========== ========================= ===================================================== =============
 begonnen   beendet    Klient                    Firma                                                 Land
---------- ---------- ------------------------- ----------------------------------------------------- -------------
 07.02.11   07.02.11   JACOBS Jacqueline (136)   Rumma & Ko OÜ (100)                                   Estland
 04.04.11   04.04.11   FAYMONVILLE Luc (129)     Alliance Nationale des Mutualités Chrétiennes (232)   Niederlande
========== ========== ========================= ===================================================== =============
<BLANKLINE>


.. _welfare.jobs.CandidaturesByOffer:

Candidatures by Job Offer
-------------------------

This table shows the Candidatures which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.CandidaturesByOffer.request(obj))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============== ========================== ======== ====================
 Anfragedatum   Klient                     Stelle   Kandidatur-Zustand
-------------- -------------------------- -------- --------------------
 ...            JEANÉMART Jérôme (180*)             Aktiv
 ...            GROTECLAES Gregory (131)            Arbeitet
============== ========================== ======== ====================
<BLANKLINE>


>>> translation.activate('en')
>>> obj = jobs.Contract.objects.get(pk=6)
>>> print(unicode(obj.client))
FAYMONVILLE Luc (129)
>>> obj.active_period()
(datetime.date(2013, 12, 13), datetime.date(2015, 12, 12))
>>> obj.update_cal_rset()
ExamPolicy #3 (u'every 3 months')
>>> print(unicode(obj.update_cal_rset().event_type))
Internal meetings with client
>>> print(obj.update_cal_rset().event_type.max_conflicting)
4
>>> settings.SITE.verbose_client_info_message = True
>>> wanted = obj.get_wanted_auto_events(ses)
>>> [i.start_date.strftime('%Y-%m-%d') for i in wanted.values()]
['2014-03-13', '2014-06-13', '2014-09-15', '2014-12-15', '2015-03-16', '2015-06-16', '2015-09-16']
>>> print(ses.response['info_message'])
Generating events between 2014-03-13 and 2015-12-12.
Reached upper date limit 2015-12-12


>>> ses.show(cal.EventsByController.request(obj),
... column_names="linked_date summary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
========================= ===============
 When                      Summary
------------------------- ---------------
 2014 Mar 13 (Thu) 09:00   Appointment 1
 2014 Jun 13 (Fri) 09:00   Appointment 2
 2014 Sep 15 (Mon) 09:00   Appointment 3
 2014 Dec 15 (Mon) 09:00   Appointment 4
 2015 Mar 16 (Mon) 09:00   Appointment 5
 2015 Jun 16 (Tue) 09:00   Appointment 6
 2015 Sep 16 (Wed) 09:00   Appointment 7
========================= ===============
<BLANKLINE>

Mélanie has two appointments on 2014-09-15:

>>> d = i2d(20140915)
>>> pv = dict(start_date=d, end_date=d)
>>> ses.show(cal.EventsByDay.request(param_values=pv),
...     column_names="user summary project")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================== =============== =========================
 Responsible user   Summary         Client
------------------ --------------- -------------------------
 Mélanie Mélard     Appointment 3   FAYMONVILLE Luc (129)
 Mélanie Mélard     Appointment 5   JACOBS Jacqueline (136)
================== =============== =========================
<BLANKLINE>

This is because the EventType of these automatically generated
evaluation appointments is configured to allow for up to 4
conflicting events:

>>> e = cal.EventsByDay.request(param_values=pv).data_iterator[0]
>>> e.event_type
EventType #2 (u'Internal meetings with client')
>>> e.event_type.max_conflicting
4

JobsOverview
------------

Printing the document 
:ref:`welfare.jobs.JobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> ses.run(obj.do_print)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
{'open_url': u'/.../jobs.JobsOverview.odt',
 'success': True}

This bug was fixed :blogref:`20130423`.
Note: the ``webdav/`` is only there when :attr:`dd.Site.user_java` is `True`.

