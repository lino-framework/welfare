import datetime

from lino_welfare.projects.gerd.settings import *


class Site(Site):
    the_demo_date = datetime.date(2014, 5, 22)
    use_java = False
    project_name = 'test_eupen'

    def get_database_settings(self):
        """See :meth:`lino.core.site.Site.get_database_settings`.

        This was an attempt to run the unit test suite on MySQL
        instead of SQLite.  

        It causes many test cases to fail because
        of the different alphabetical ordering between SQLite and
        MySQL.

        """
        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': self.project_name,
                'USER': 'django',
                'PASSWORD': 'my cool password',
                'HOST': 'localhost',
                'PORT': 3306,
                'OPTIONS': {
                   "init_command": "SET storage_engine=MyISAM",
                }
            }
        }


SITE = Site(globals())
# SITE.appy_params.update(raiseOnError=False)

DEBUG = True
