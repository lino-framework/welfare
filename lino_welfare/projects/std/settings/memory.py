from .demo import *
SITE = Site(globals(), verbose_name="Lino Welfare (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
