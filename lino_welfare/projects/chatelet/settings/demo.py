from lino_welfare.projects.chatelet.settings import *

class Site(Site):
    the_demo_date = datetime.date(2014, 05, 22)
    ignore_dates_after = datetime.date(2019, 05, 22)

    # the_demo_date = datetime.date(2015, 01, 25)
    # test cases which rely on this date:
    # docs/tested/cv2.rst

SITE = Site(globals())
