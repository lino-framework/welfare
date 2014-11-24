import datetime
from lino_welfare.projects.base import *


class Site(Site):

    title = "Lino Welfare"

    the_demo_date = datetime.date(2014, 05, 22)
    # test cases which rely on this date:
    # docs/tested/jobs.rst

    ignore_dates_after = datetime.date(2019, 05, 22)

    def is_imported_partner(self, obj):
        if obj.id is not None and (obj.id > 110 and obj.id < 121):
            return True
        if obj.id == 180:
            return True
        return False

