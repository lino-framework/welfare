from ..settings import *


class Site(Site):
    the_demo_date = datetime.date(2014, 05, 22)
    
SITE = Site(globals())

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
