from .demo import *
SITE = Site(
    globals(),
    no_local=True,
    use_java=True,
    is_local_project_dir=True,
    ignore_model_errors=True,
    remote_user_header='REMOTE_USER')
DEBUG = True
SITE.appy_params.update(raiseOnError=True)
SITE.appy_params.update(pythonWithUnoPath='/usr/bin/python3')
SITE.webdav_url = '/'
