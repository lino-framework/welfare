from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_welfare')

add_demo_project('lino_welfare.projects.std.settings.demo')
add_demo_project('lino_welfare.projects.eupen.settings.demo')
add_demo_project('lino_welfare.projects.chatelet.settings.demo')

env.locale_dir = 'lino_welfare/modlib/welfare/locale'
env.languages = ['en', 'de', 'fr']
env.revision_control_system = 'git'
env.apidoc_exclude_pathnames = ['lino_welfare/projects']
env.tolerate_sphinx_warnings = False

env.cleanable_files = ['docs/api/lino_welfare.*']
