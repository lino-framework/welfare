"""
The settings.py used for building both `/docs` and `/userdocs`
"""
from lino_welfare.settings import *

class Site(Site):
  
    title = "Lino-Welfare demo"
    #~ use_jasmine = True
    #~ use_davlink = False
    #~ use_extensible = True
    #~ remote_user_header = None # 20121003
    
    def is_imported_partner(self,obj):
        if obj.id is not None and (obj.id > 110 and obj.id < 121):
            return True
        if obj.id == 180:
            return True
        return False

SITE = Site(globals()) 

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

