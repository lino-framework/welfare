from atelier.fablib import *
setup_from_project('lino_welfare', 'lino_welfare.settings.demo')

env.demo_databases.append('lino_welfare.settings.eupen.demo')
env.demo_databases.append('lino_welfare.settings.chatelet.demo')

env.use_mercurial = False
