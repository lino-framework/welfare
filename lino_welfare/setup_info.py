# -*- coding: UTF-8 -*-
# Copyright 2002-2015 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

# Note that this module may not have a docstring because any global
# variable defined here will override the global namespace of modules
# like `lino_welfare/__init__.py` who include this file with execfile

# This module is part of the Lino test suite.
# To test only this module:
#
#   $ python setup.py test -s tests.PackagesTests


SETUP_INFO = dict(
    name='lino-welfare',
    version='1.1.25',  # since 20150918
    install_requires=['lino', 'suds', 'vobject', 'django-iban', 'xlwt'],
    test_suite='tests',
    description=u"A Lino application for Belgian Centres for Public Welfare",
    long_description="""\
Lino Welfare is a modular customized
`Lino <http://www.lino-framework.org>`__
application for Belgian
*Public Centres for Social Welfare*.
It currently covers the following functions of a PCSW:

- General client management
- Integration service
- Debt mediation
- Calendar management
- Issuing attestations

It started as a part of the Lino project and forked off in August 2012
to become an independent project, possibly to be maintained by an
independant organization.""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://welfare.lino-framework.org",
    license='GNU Affero General Public License v3',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU Affero General Public License v3
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
    'lino_welfare.modlib.courses',
    'lino_welfare.modlib.courses.fixtures',
    'lino_welfare.modlib.cv',
    'lino_welfare.modlib.cv.fixtures',
    'lino_welfare.modlib.debts',
    'lino_welfare.modlib.debts.fixtures',
    'lino_welfare.modlib.dupable_clients',
    'lino_welfare.modlib.dupable_clients.fixtures',
    'lino_welfare.modlib.finan',
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
    'lino_welfare.modlib.uploads',
    'lino_welfare.modlib.uploads.fixtures',
    'lino_welfare.modlib.users',
    'lino_welfare.modlib.users.fixtures',
    'lino_welfare.modlib.welfare',
    'lino_welfare.modlib.welfare.fixtures',
    'lino_welfare.modlib.welfare.management',
    'lino_welfare.modlib.welfare.management.commands',
    'lino_welfare.projects',
    'lino_welfare.projects.chatelet',
    'lino_welfare.projects.chatelet.modlib',
    'lino_welfare.projects.chatelet.modlib.courses',
    'lino_welfare.projects.chatelet.modlib.courses.fixtures',
    'lino_welfare.projects.chatelet.modlib.cv',
    'lino_welfare.projects.chatelet.modlib.cv.fixtures',
    'lino_welfare.projects.chatelet.modlib.isip',
    'lino_welfare.projects.chatelet.modlib.pcsw',
    'lino_welfare.projects.chatelet.settings',
    'lino_welfare.projects.chatelet.tests',
    'lino_welfare.projects.std',
    'lino_welfare.projects.std.settings',
    'lino_welfare.projects.std.tests',
    'lino_welfare.projects.eupen',
    'lino_welfare.projects.eupen.modlib',
    'lino_welfare.projects.eupen.modlib.pcsw',
    'lino_welfare.projects.eupen.settings',
    'lino_welfare.projects.eupen.tests',
    'lino_welfare.scripts',
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

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l

add_package_data('lino_welfare.modlib.cbss',
                 'WSDL/*.wsdl',
                 'XSD/*.xsd',
                 'XSD/SSDN/Common/*.xsd',
                 'XSD/SSDN/OCMW_CPAS/IdentifyPerson/*.xsd',
                 'XSD/SSDN/OCMW_CPAS/ManageAccess/*.xsd',
                 'XSD/SSDN/OCMW_CPAS/PerformInvestigation/*.xsd',
                 'XSD/SSDN/OCMW_CPAS/Loi65Wet65/*.xsd',
                 'XSD/SSDN/Person/*.xsd',
                 'XSD/SSDN/Service/*.xsd')

add_package_data('lino_welfare.modlib.cbss',
                 'config/cbss/RetrieveTIGroupsRequest/*.odt')
add_package_data('lino_welfare.modlib.cbss',
                 'config/cbss/IdentifyPersonRequest/*.odt')
add_package_data('lino_welfare.modlib.cbss', 'fixtures/*.csv')
add_package_data('lino_welfare.modlib.cbss', 'fixtures/*.xml')
add_package_data('lino_welfare.modlib.debts', 'config/debts/Budget/*.odt')
add_package_data('lino_welfare.modlib.courses', 'config/courses/Course/*.odt')
add_package_data('lino_welfare.modlib.pcsw', 'config/pcsw/Client/*.odt')
add_package_data('lino_welfare.modlib.cal', 'config/cal/Guest/*.odt')
add_package_data('lino_welfare.modlib.jobs',
                 'config/jobs/ContractsSituation/*.odt')
add_package_data('lino_welfare.modlib.jobs',
                 'config/jobs/OldJobsOverview/*.odt')
add_package_data('lino_welfare.modlib.jobs', 'config/jobs/JobsOverview/*.odt')
add_package_data('lino_welfare.settings', 'media/pictures/contacts.Person.jpg')
add_package_data('lino_welfare', 'config/lino_welfare/ActivityReport/*.odt')
add_package_data('lino_welfare', 'config/admin_main.html')
l = add_package_data('lino_welfare.modlib.welfare')
for lng in 'fr de nl'.split():
    l.append('lino_welfare/modlib/welfare/locale/%s/LC_MESSAGES/*.mo' % lng)
