#!/usr/bin/env python
if __name__ == "__main__":

    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_welfare.settings.demo'

    from lino_welfare.settings import demo

    from django.core.management import execute_manager

    execute_manager(demo)







