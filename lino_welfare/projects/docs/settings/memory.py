from ..settings import *
SITE = Site(globals(), title="Lino Welfare (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
