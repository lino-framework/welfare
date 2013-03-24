from djangosite.utils.fablib import *
setup_from_project('lino_welfare')

env.django_databases.append('docs')

#~ env.django_doctests.append('tutorials.fixtures1.settings')

#~ env.django_admin_tests.append('tutorials.fixtures1.settings')

env.docs_doctests.append('tested/index.rst')

env.languages = 'en fr nl de'.split()