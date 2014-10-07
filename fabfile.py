from atelier.fablib import *
setup_from_project('lino_welfare', 'lino_welfare.projects.docs.settings.demo')

env.demo_databases.append('lino_welfare.projects.eupen.settings.demo')
env.demo_databases.append('lino_welfare.projects.chatelet.settings.demo')

env.use_mercurial = False
env.apidoc_exclude_pathnames = ['lino_welfare/projects']
env.doc_trees = ['docs', 'docs_de', 'docs_fr']
