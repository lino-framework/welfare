import datetime

from lino_welfare.projects.eupen.settings import *


class Site(Site):
    the_demo_date = datetime.date(2014, 5, 22)
    # ignore_dates_after = datetime.date(2019, 05, 22)
    use_java = False
    webdav_protocol = 'webdav'
    beid_protocol = 'beid'
    use_websockets = False

SITE = Site(globals())
# SITE.appy_params.update(raiseOnError=False)

DEBUG = True
