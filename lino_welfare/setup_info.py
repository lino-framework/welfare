# -*- coding: UTF-8 -*-
# Copyright 2002-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# This module is part of the Lino Welfare test suite.
# To test only this module:
#
#   $ python setup.py test -s tests.PackagesTests

requires = ['lino-cosi',
            'pytidylib',
            'django-iban', 'metafone',
            'cairocffi']
requires.append('suds-py3')

SETUP_INFO = dict(
    name='lino-welfare',
    version='20.8.0',
    install_requires=requires,
    test_suite='tests',
    tests_require=['pytest'],
    include_package_data=True,
    zip_safe=False,
    description="A Lino plugin library for Belgian PCSWs",
    long_description="""\
Lino Welfare is a
`Lino <http://www.lino-framework.org>`__
plugin library
for Belgian
*Public Centres for Social Welfare*.

- The central project homepage is
  http://welfare.lino-framework.org

- There are two applications using this library:
  `welcht <http://welcht.lino-framework.org>`__
  and `weleup <http://weleup.lino-framework.org>`__

- There are *user guides* in `French
  <http://fr.welfare.lino-framework.org>`_ and `German
  <http://de.welfare.lino-framework.org>`_.

- Online demo sites at
  http://welfare-demo.lino-framework.org
  and
  http://welfare-demo-fr.lino-framework.org

- For *introductions* and *commercial information* about Lino Welfare
  see `www.saffre-rumma.net
  <http://www.saffre-rumma.net/welfare/>`__.


""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://welfare.lino-framework.org",
    license='BSD-2-Clause',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Natural Language :: English
Natural Language :: French
Natural Language :: German
Operating System :: OS Independent
Topic :: Database :: Front-Ends
Topic :: Home Automation
Topic :: Office/Business
Topic :: Sociology :: Genealogy
Topic :: Education""".splitlines())

SETUP_INFO.update(packages=[
    'lino_welfare',
    'lino_welfare.modlib',
    'lino_welfare.modlib.active_job_search',
    'lino_welfare.modlib.active_job_search.fixtures',
    'lino_welfare.modlib.aids',
    'lino_welfare.modlib.aids.fixtures',
    'lino_welfare.modlib.art61',
    'lino_welfare.modlib.art61.fixtures',
    'lino_welfare.modlib.badges',
    'lino_welfare.modlib.cal',
    'lino_welfare.modlib.cal.fixtures',
    'lino_welfare.modlib.cbss',
    'lino_welfare.modlib.cbss.fixtures',
    'lino_welfare.modlib.cbss.management',
    'lino_welfare.modlib.cbss.management.commands',
    'lino_welfare.modlib.client_vouchers',
    'lino_welfare.modlib.contacts',
    'lino_welfare.modlib.contacts.fixtures',
    'lino_welfare.modlib.contacts.management',
    'lino_welfare.modlib.contacts.management.commands',
    'lino_welfare.modlib.xcourses',
    'lino_welfare.modlib.xcourses.fixtures',
    'lino_welfare.modlib.cv',
    'lino_welfare.modlib.cv.fixtures',
    'lino_welfare.modlib.debts',
    'lino_welfare.modlib.debts.fixtures',
    'lino_welfare.modlib.dupable_clients',
    'lino_welfare.modlib.dupable_clients.fixtures',
    'lino_welfare.modlib.finan',
    'lino_welfare.modlib.finan.fixtures',
    'lino_welfare.modlib.esf',
    'lino_welfare.modlib.esf.fixtures',
    'lino_welfare.modlib.households',
    'lino_welfare.modlib.households.fixtures',
    'lino_welfare.modlib.integ',
    'lino_welfare.modlib.integ.fixtures',
    'lino_welfare.modlib.isip',
    'lino_welfare.modlib.jobs',
    'lino_welfare.modlib.jobs.fixtures',
    'lino_welfare.modlib.ledger',
    'lino_welfare.modlib.ledger.fixtures',
    'lino_welfare.modlib.notes',
    'lino_welfare.modlib.notes.fixtures',
    'lino_welfare.modlib.newcomers',
    'lino_welfare.modlib.newcomers.fixtures',
    'lino_welfare.modlib.pcsw',
    'lino_welfare.modlib.pcsw.fixtures',
    'lino_welfare.modlib.polls',
    'lino_welfare.modlib.polls.fixtures',
    'lino_welfare.modlib.projects',
    'lino_welfare.modlib.reception',
    'lino_welfare.modlib.sales',
    'lino_welfare.modlib.sepa',
    'lino_welfare.modlib.sepa.fixtures',
    'lino_welfare.modlib.system',
    'lino_welfare.modlib.immersion',
    'lino_welfare.modlib.immersion.fixtures',
    'lino_welfare.modlib.users',
    'lino_welfare.modlib.users.fixtures',
    'lino_welfare.modlib.welfare',
    'lino_welfare.modlib.welfare.fixtures',
    'lino_welfare.modlib.welfare.management',
    'lino_welfare.modlib.welfare.management.commands',
    'lino_welfare.scripts',
    'lino_welfare.projects',
    'lino_welfare.projects.gerd',
    'lino_welfare.projects.gerd.settings',
    'lino_welfare.projects.gerd.tests',
    'lino_welfare.projects.mathieu',
    'lino_welfare.projects.mathieu.settings',
    'lino_welfare.projects.mathieu.tests',
])

SETUP_INFO.update(message_extractors={
    'lino_welfare': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
        #~ ('**/templates/**.txt',  'genshi', {
        #~ 'template_class': 'genshi.template:TextTemplate'
        #~ })
    ],
})
SETUP_INFO.update(include_package_data=True)

# SETUP_INFO.update(package_data=dict())


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l
#
# add_package_data('lino_welfare.modlib.cbss',
#                  'WSDL/*.wsdl',
#                  'XSD/*.xsd',
#                  'XSD/SSDN/Common/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/IdentifyPerson/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/ManageAccess/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/PerformInvestigation/*.xsd',
#                  'XSD/SSDN/OCMW_CPAS/Loi65Wet65/*.xsd',
#                  'XSD/SSDN/Person/*.xsd',
#                  'XSD/SSDN/Service/*.xsd')
#
# add_package_data('lino_welfare.modlib.cbss',
#                  'config/cbss/RetrieveTIGroupsRequest/*.odt')
# add_package_data('lino_welfare.modlib.cbss',
#                  'config/cbss/IdentifyPersonRequest/*.odt')
# add_package_data('lino_welfare.modlib.cbss', 'fixtures/*.csv')
# add_package_data('lino_welfare.modlib.cbss', 'fixtures/*.xml')
# add_package_data('lino_welfare.modlib.debts', 'config/debts/Budget/*.odt')
# add_package_data('lino_welfare.modlib.courses', 'config/courses/Course/*.odt')
# add_package_data('lino_welfare.modlib.pcsw', 'config/pcsw/Client/*.odt')
# add_package_data('lino_welfare.modlib.cal', 'config/cal/Guest/*.odt')
# add_package_data('lino_welfare.modlib.jobs',
#                  'config/jobs/ContractsSituation/*.odt')
# add_package_data('lino_welfare.modlib.jobs',
#                  'config/jobs/OldJobsOverview/*.odt')
# add_package_data('lino_welfare.modlib.jobs', 'config/jobs/JobsOverview/*.odt')
# add_package_data('lino_welfare.settings', 'media/pictures/contacts.Person.jpg')
# add_package_data('lino_welfare', 'config/lino_welfare/ActivityReport/*.odt')
# add_package_data('lino_welfare', 'config/admin_main.html')
# l = add_package_data('lino_welfare.modlib.welfare')
# for lng in 'fr de nl'.split():
#     l.append('lino_welfare/modlib/welfare/locale/%s/LC_MESSAGES/*.mo' % lng)
#
