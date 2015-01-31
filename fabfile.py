from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_welfare')

add_demo_project('lino_welfare/projects/std')
add_demo_project('lino_welfare/projects/eupen')
add_demo_project('lino_welfare/projects/chatelet')

env.languages = ['en', 'de', 'fr']
env.revision_control_system = 'git'
env.apidoc_exclude_pathnames = ['lino_welfare/projects']
# env.tolerate_sphinx_warnings = True
