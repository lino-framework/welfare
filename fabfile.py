from atelier.fablib import *
setup_from_project('lino_welfare')

#~ env.django_databases.append('docs')
#~ env.django_databases.append('userdocs')
#~ env.tolerate_sphinx_warnings = True

env.languages = 'fr nl de'.split()
