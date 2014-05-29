"""
The settings used for building both `/docs` and `/userdocs`
"""
from lino_welfare.projects.base import *


class Site(Site):

    title = "Lino Welfare"

    def is_imported_partner(self, obj):
        if obj.id is not None and (obj.id > 110 and obj.id < 121):
            return True
        if obj.id == 180:
            return True
        return False

