"""
The settings.py used for building both `/docs` and `/userdocs`
"""
from lino_welfare.settings import *

class Site(Site):

    title = "Lino pour CPAS"
    languages = 'fr nl'
    hidden_languages = None
    uppercase_last_name = True

    demo_fixtures = """std few_languages props all_countries
    be demo cbss mini demo2 local """.split()

    # hidden_apps = 'debts courses'
    hidden_apps = 'debts'

    def get_installed_apps(self):
        for a in super(Site, self).get_installed_apps():
            if a == 'lino_welfare.modlib.courses':
                yield 'lino.modlib.courses'
            elif a == 'lino_welfare.modlib.pcsw':
                yield 'lino_welfare.settings.fr.pcsw'
            else:
                yield a

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        self.plugins.courses.configure(pupil_model='pcsw.Client')
        # self.plugins.courses.configure(teacher_model='users.User')
        super(Site, self).setup_plugins()

    def get_default_language(self):
        return 'fr'

    def setup_choicelists(self):
        """
        This defines default user profiles for
        :mod:`lino_welfare.settings.fr`.
        """

        # must import it to activate workflows:
        from lino.modlib.courses import workflows

        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset(
            '* office coaching integ courses cbss newcomers reception')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),                   '_ _ _ _ _ _ _ _',
            name='anonymous',
            readonly=True,
            authenticated=False)
        add('100', _("Integration Agent"),           'U U U U U U _ _')
        add('110', _("Integration Agent (Manager)"), 'U M M M M U _ _')
        add('200', _("Newcomers consultant"),        'U U U _ M U U _')
        add('210', _("Reception clerk"),             'U _ _ _ _ _ _ U')
        add('400', _("Social agent"),                'U U U _ U U _ _')
        add('410', _("Social agent (Manager)"),      'U M M _ M U _ _')
        add('900', _("Administrator"),               'A A A A A A A A',
            name='admin')



# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
