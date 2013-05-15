from lino_welfare.demo.settings import *
SITE = Site(globals(),
  #~ no_local=True,
  remote_user_header='REMOTE_USER',
  build_js_cache_on_startup=False,
) 
DEBUG=True
