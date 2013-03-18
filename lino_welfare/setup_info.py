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
      version='1.1.0+', 
      install_requires=['Lino==1.6.3','suds','vobject'],
      #~ version=VERSION,
      description=u"A Lino application for Belgian Public Welfare Centres",
      long_description="""\
Lino-Welfare is a modular customized application for Belgian 
*Public Centres for Social Welfare*. 
It currently covers the following functions of a PCSW:

- General client management
- Integration service
- Debt mediation

It started as a part of the `Lino <http://code.google.com/p/lino/>`_
project and forked off in August 2012 
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
      packages=[
        'lino_welfare',
        'lino_welfare.demo',
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
        'lino_welfare.modlib.isip',
        'lino_welfare.modlib.jobs',
        'lino_welfare.modlib.jobs.fixtures',
        'lino_welfare.modlib.newcomers',
        'lino_welfare.modlib.newcomers.fixtures',
        'lino_welfare.modlib.pcsw',
        'lino_welfare.modlib.pcsw.fixtures',
        'lino_welfare.modlib.pcsw.management',
        'lino_welfare.modlib.pcsw.management.commands',
        'lino_welfare.modlib.pcsw.templates',
        'lino_welfare.modlib.pcsw.tests',
        'lino_welfare.modlib.statbel',
        'lino_welfare.modlib.statbel.fixtures',
      ],
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
