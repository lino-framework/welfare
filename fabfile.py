from atelier.fablib import *
setup_from_project('lino_welfare')

add_demo_database('lino_welfare.projects.docs.settings.demo')
add_demo_database('lino_welfare.projects.eupen.settings.demo')
add_demo_database('lino_welfare.projects.chatelet.settings.demo')

env.languages = ['en', 'de', 'fr']
env.use_mercurial = False
env.apidoc_exclude_pathnames = ['lino_welfare/projects']
# env.tolerate_sphinx_warnings = True
