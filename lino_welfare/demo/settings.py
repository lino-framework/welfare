"""
The settings.py used for building both `/docs` and `/userdocs`
"""
from lino_welfare.settings import *

class Site(Site):
  
    title = "Lino-Welfare"
  
    #~ languages = ['en']
    languages = 'de fr nl'
    #~ languages = ['de','fr']
    #~ languages = ['fr','de']
    #~ languages = ['de']
    use_jasmine = True
    use_davlink = False
    use_extensible = True
    use_eid_jslib = False
    remote_user_header = None # 20121003
        
    def is_imported_partner(self,obj):
        if obj.id is not None and (obj.id > 110 and obj.id < 121):
            return True
        if obj.id == 180:
            return True
        return False

SITE = Site(globals())
#~ print 20130409, __file__, LOGGING
