## Copyright 2009-2012 Luc Saffre
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
from os.path import join, abspath, dirname

from lino_welfare.modlib.pcsw.settings import *

class Site(Site):
  
    title = "Lino/Welfare demo"
    languages = 'de fr en'.split()
    #~ languages = ['de','fr']
    #~ languages = ['fr','de']
    #~ languages = ['de']
    use_jasmine = True
    use_davlink = False
    use_extensible = True
    use_eid_jslib = False
    remote_user_header = None # 20121003
          
    #~ def override_user_language(self):
        #~ return os.environ.get('OVERRIDE_USER_LANGUAGE')
        #~ return os.environ.set('OVERRIDE_USER_LANGUAGE',file(join(self.project_dir,'override_user_language.txt')).read().strip())
        
    def is_imported_partner(self,obj):
        if obj.id is not None and (obj.id > 110 and obj.id < 121):
            return True
        if obj.id == 180:
            return True
        return False
    
    
SITE = Site(__file__,globals()) 

ADMINS = []

DEBUG = True

# uncomment for testing in temporary database:
#~ DATABASES['default']['NAME'] = ':memory:'
