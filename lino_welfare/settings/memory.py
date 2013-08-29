from lino_welfare.settings.demo import *
SITE = Site(globals(),title = "Lino-Welfare (:memory:)") 
DATABASES['default']['NAME'] = ':memory:'

