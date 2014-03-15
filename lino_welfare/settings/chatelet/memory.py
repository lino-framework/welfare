from lino_welfare.settings.fr.demo import *
SITE = Site(globals(), title=Site.title+" (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
