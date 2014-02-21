"""
The settings.py used for building both `/docs` and `/userdocs`
"""
from lino_welfare.settings import *


class Site(Site):

    title = "Lino pour CPAS"
    languages = 'fr nl'
    hidden_languages = None

    demo_fixtures = """std all_countries
    be
    few_languages demo mini demo2 local """.split()

    def get_default_language(self):
        return 'fr'

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
