from ..settings import *

class Site(Site):
    the_demo_date = datetime.date(2015, 01, 25)
    # test cases which rely on this date:
    # docs/tested/cv2.rst

SITE = Site(globals())

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
