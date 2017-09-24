import datetime

from ..settings import *


class Site(Site):
    the_demo_date = datetime.date(2014, 5, 22)
    # ignore_dates_after = datetime.date(2019, 05, 22)
    use_java = False

SITE = Site(globals())
DEBUG = True
