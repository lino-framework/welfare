import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_welfare.demo.settings'
from django.conf import settings
settings.LINO.startup()
site = settings.LINO