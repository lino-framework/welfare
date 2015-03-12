import datetime

from lino_welfare.projects.std.settings import *


class Site(Site):

    project_name = 'welfare_std'
    # avoid name clash with `lino/projects/docs`.

    ignore_dates_after = datetime.date(2019, 05, 22)
    the_demo_date = datetime.date(2014, 05, 22)
    # many test cases which rely on these dates

    def is_imported_partner(self, obj):
        if obj.id is not None and (obj.id > 110 and obj.id < 121):
            return True
        if obj.id == 180:
            return True
        return False


SITE = Site(globals())
