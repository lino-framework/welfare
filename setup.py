# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

import os
#~ from distutils.core import setup
from setuptools import setup
#~ from distutils.core import setup, Distribution
#~ import lino_welfare

#~ class MyDistribution(Distribution):

#~ VERSION = file(os.path.join(os.path.dirname(__file__),'VERSION')).read().strip()

execfile(os.path.join(os.path.dirname(__file__),'lino_welfare','version.py'))

#~ from lino_welfare.modlib.pcsw import settings

#~ VERSION = settings.LINO.version
#~ assert not "+" in VERSION
#~ assert not "-" in VERSION
    
setup(name='lino-welfare',
      #~ distclass=MyDistribution,
      #~ dist_dir=os.path.join('docs','dist'),
      version=__version__, 
      #~ version=VERSION,
      description=u"A Lino application for Belgian Public Welfare Centres",
      author = 'Luc Saffre',
      author_email = 'luc.saffre@gmail.com',
      #~ description=settings.LINO.description,
      #~ author=settings.LINO.author,
      #~ author_email=settings.LINO.author_email,
      url="http://code.google.com/p/lino-welfare/",
      #~ url=settings.LINO.url,
      license='GPL',
      packages=['lino_welfare'],
      requires=['lino','suds'],
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
Topic :: Software Development :: Libraries :: Application Frameworks
""".splitlines()
      )
