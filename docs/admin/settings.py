from lino_welfare.projects.std.settings import *
#from lino_welfare.projects.eupen.settings import *
#from lino_welfare.projects.chatelet.settings import *


class Site(Site):
    verbose_name = "My Lino Welfare demo"

SITE = Site(globals())
