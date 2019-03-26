import datetime
from lino_welfare.projects.mathieu.settings import *


class Site(Site):
    # title = "Welfare Chatelet Demo"
    the_demo_date = datetime.date(2014, 5, 22)
    # ignore_dates_after = datetime.date(2019, 05, 22)
    use_java = False
    # use_silk_icons = True  # temporarily
    webdav_protocol = 'webdav'
    # beid_protocol = 'beid'


SITE = Site(globals())

DEBUG = True
