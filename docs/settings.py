from lino_welfare.modlib.pcsw.settings import *

class Site(Site):
  
    title = "Lino-Welfare Technical Reference"
  
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
