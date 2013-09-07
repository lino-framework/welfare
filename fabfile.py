from atelier.fablib import *
setup_from_project('lino_welfare','lino_welfare.settings.demo')

# demo site has no English, but userdocs are still based in English
# so we must manually specify the language settings:
#~ env.userdocs_base_language = 'en'
#~ env.languages = 'en fr nl de'.split()

#~ env.demo_database = 'lino_welfare.demo.settings'

#~ env.demo_databases.append('lino_welfare.settings.demo')
#~ env.django_databases.append('userdocs')
#~ env.tolerate_sphinx_warnings = True

