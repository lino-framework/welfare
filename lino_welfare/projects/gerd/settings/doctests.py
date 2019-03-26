from .demo import *
SITE = Site(
    globals(),
    # use_java=True,
    hidden_languages='fr en',
    remote_user_header='REMOTE_USER')
DEBUG = True
# SITE.appy_params.update(raiseOnError=True)
# SITE.appy_params.update(pythonWithUnoPath='/usr/bin/python3')
SITE.webdav_url = '/'

# just to make the menu item visible:
SITE.plugins.b2c.configure(import_statements_path=SITE.project_dir)
