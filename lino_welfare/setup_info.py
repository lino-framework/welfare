# -*- coding: UTF-8 -*-
## Copyright 2002-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

#~ Note that this module may not have a docstring because any 
#~ global variable defined here will override the global 
#~ namespace of lino_welfare/__init__.py who includes it with execfile
#~ 
#~ After editing this file, also edit the following files:
#~ 
#~ - ../docs/releases/index.rst
#~ - ../docs/releases/<__version__>.rst

SETUP_INFO = dict(name='lino-welfare',
      #~ distclass=MyDistribution,
      #~ dist_dir=os.path.join('docs','dist'),
      version='1.1.10', # released 20131007(?)
      install_requires=['lino','suds','vobject'],
      #~ version=VERSION,
      test_suite = 'tests',
      description=u"A Lino application for Belgian Public Welfare Centres",
      long_description="""\
Lino-Welfare is a modular customized 
`Lino <http://www.lino-framework.org>`__ 
application for Belgian 
*Public Centres for Social Welfare*. 
It currently covers the following functions of a PCSW:

- General client management
- Integration service
- Debt mediation

It started as a part of the Lino project and 
forked off in August 2012 
to become an independent project,
possibly to be maintained by an independant organization.""",
      author = 'Luc Saffre',
      author_email = 'luc.saffre@gmail.com',
      #~ description=settings.LINO.description,
      #~ author=settings.LINO.author,
      #~ author_email=settings.LINO.author_email,
      #~ url="http://code.google.com/p/lino-welfare/",
      url="http://welfare.lino-framework.org",
      #~ url=settings.LINO.url,
      license='GPL',
      classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: French
Natural Language :: German
Operating System :: OS Independent
Topic :: Database :: Front-Ends
Topic :: Home Automation
Topic :: Office/Business
Topic :: Software Development :: Libraries :: Application Frameworks""".splitlines())

SETUP_INFO.update(packages=[
  'lino_welfare',
  'lino_welfare.settings',
  'lino_welfare.fixtures',
  'lino_welfare.management',
  'lino_welfare.management.commands',
  'lino_welfare.tests',
  'lino_welfare.modlib',
  'lino_welfare.modlib.cbss',
  'lino_welfare.modlib.cbss.fixtures',
  'lino_welfare.modlib.cbss.management',
  'lino_welfare.modlib.cbss.management.commands',
  'lino_welfare.modlib.cbss.tests',
  'lino_welfare.modlib.courses',
  'lino_welfare.modlib.cv',
  'lino_welfare.modlib.debts',
  'lino_welfare.modlib.debts.fixtures',
  'lino_welfare.modlib.integ',
  'lino_welfare.modlib.isip',
  'lino_welfare.modlib.cal',
  'lino_welfare.modlib.cal.fixtures',
  'lino_welfare.modlib.households',
  'lino_welfare.modlib.households.fixtures',
  'lino_welfare.modlib.contacts',
  'lino_welfare.modlib.contacts.fixtures',
  'lino_welfare.modlib.notes',
  'lino_welfare.modlib.notes.fixtures',
  'lino_welfare.modlib.system',
  'lino_welfare.modlib.system.fixtures',
  'lino_welfare.modlib.jobs',
  'lino_welfare.modlib.jobs.fixtures',
  'lino_welfare.modlib.newcomers',
  'lino_welfare.modlib.newcomers.fixtures',
  'lino_welfare.modlib.pcsw',
  'lino_welfare.modlib.pcsw.fixtures',
  'lino_welfare.modlib.reception',
])

SETUP_INFO.update(message_extractors = {
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
def add_package_data(package,*patterns):
    l = SETUP_INFO['package_data'].setdefault(package,[])
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

add_package_data('lino_welfare.modlib.cbss','config/cbss/RetrieveTIGroupsRequest/*.odt')
add_package_data('lino_welfare.modlib.cbss','config/cbss/IdentifyPersonRequest/*.odt')
add_package_data('lino_welfare.modlib.cbss','fixtures/*.csv')
add_package_data('lino_welfare.modlib.cbss','fixtures/*.xml')
add_package_data('lino_welfare.modlib.debts','config/debts/Budget/*.odt')
add_package_data('lino_welfare.modlib.courses','config/courses/Course/*.odt')
add_package_data('lino_welfare.modlib.pcsw','config/pcsw/Client/*.odt')
add_package_data('lino_welfare.modlib.cal','config/cal/Guest/*.odt')
add_package_data('lino_welfare.modlib.jobs','config/jobs/ContractsSituation/*.odt')
add_package_data('lino_welfare.modlib.jobs','config/jobs/OldJobsOverview/*.odt')
add_package_data('lino_welfare.modlib.jobs','config/jobs/JobsOverview/*.odt')
add_package_data('lino_welfare.settings','media/pictures/contacts.Person.jpg')
add_package_data('lino_welfare','config/lino_welfare/ActivityReport/*.odt')
add_package_data('lino_welfare','config/admin_main.html')
l = add_package_data('lino_welfare')
for lng in 'fr de nl'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
    

