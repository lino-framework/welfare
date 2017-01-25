.. _welfare.specs.coachings:

===============
Coachings
===============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_coachings
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

.. contents::
   :depth: 2
   :local:




>>> from lino_xl.lib.coachings.roles import CoachingsStaff
>>> username = 'rolf'
>>> rt.login(username).user.profile.has_required_roles([CoachingsStaff])
True

>>> from lino_xl.lib.coachings.choicelists import ClientStates
>>> ClientStates.required_roles
set([<class 'lino_xl.lib.coachings.roles.CoachingsStaff'>])

>>> url = 'api/coachings/ClientStates'
>>> url = settings.SITE.buildurl(url, fmt='json')
>>> response = test_client.get(url, REMOTE_USER=username)
>>> result = check_json_result(response, None, "GET %s for user %s" % (url, username))
>>> result['count']
4
