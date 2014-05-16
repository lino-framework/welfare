.. _welfare.tested.newcomers:

Newcomers
=============

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_newcomers

..  
    >>> from __future__ import print_function
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from django.test import Client

>>> ses = settings.SITE.login('rolf')
>>> translation.activate('en')

>>> ses.show(jobs.Jobs,column_names="name provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================ ====================================== =============================
 Name             Job Provider                           Job Sector
---------------- -------------------------------------- -----------------------------
 Cook             R-Cycle Sperrgutsortierzentrum (225)   Maritime
 Cook             Pro Aktiv V.o.G. (227)                 Education
 Cook assistant   Pro Aktiv V.o.G. (227)                 Medical & paramedical
 Cook assistant   BISA (224)                             Cleaning
 Dishwasher       BISA (224)                             Construction & buildings
 Dishwasher       R-Cycle Sperrgutsortierzentrum (225)   Transport
 Waiter           BISA (224)                             Agriculture & horticulture
 Waiter           R-Cycle Sperrgutsortierzentrum (225)   Tourism
================ ====================================== =============================
<BLANKLINE>

The csv view failed for tables which contained 
at least one :class:`DisplayField <lino.core.fields.DisplayField>`.
The following snippet reproduces this bug:

>>> client = Client()
>>> # url = 'http://welfare-demo.lino-framework.org/api/newcomers/NewClients?fmt=csv'
>>> url = '/api/newcomers/NewClients?fmt=csv'
>>> res = client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> print(res.content[:24])
name_column,client_state



JobsOverview
------------

Printing the document 
:ref:`welfare.jobs.JobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> ses.run(obj.do_print)
... #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/webdav/userdocs/appyodt/jobs.JobsOverview.odt',
 'success': True}

This bug was fixed :blogref:`20130423`.
Note: the ``webdav/`` is only there when :attr:`dd.Site.user_java` is `True`.


>>> with translation.override('de'):
...    ses.show(pcsw.CoachingTypes)
============================== ============================== ===================================================
 Bezeichnung                    Bezeichnung (fr)               Bezeichnung (de)
------------------------------ ------------------------------ ---------------------------------------------------
 GSS (General Social Service)   SSG (Service social général)   ASD (Allgemeiner Sozialdienst)
 Integration service            Service intégration            DSBE (Dienst für Sozial-Berufliche Eingliederung)
 Debts mediation                Médiation de dettes            Schuldnerberatung
============================== ============================== ===================================================
<BLANKLINE>

