from djangosite.utils.fablib import *
setup_from_project('lino_welfare')

env.django_databases.append('docs')
env.django_databases.append('userdocs')

#~ env.django_doctests.append('tutorials.fixtures1.settings')

#~ env.django_admin_tests.append('tutorials.fixtures1.settings')

# run only these with `fab t4`
env.docs_doctests.append('tested/misc.rst')
env.docs_doctests.append('tested/debts.rst')

env.languages = 'fr nl de'.split()