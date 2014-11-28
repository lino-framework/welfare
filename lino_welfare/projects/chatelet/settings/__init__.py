# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The settings.py used for building both `/docs` and `/userdocs`
"""
from lino_welfare.projects.base import *


class Site(Site):

    title = "Lino pour CPAS"
    languages = 'fr nl en'
    hidden_languages = None

    demo_fixtures = """std few_languages props all_countries
    demo cbss mini demo2 jobsearch local """.split()

    migration_class = 'lino_welfare.projects.chatelet.migrate.Migrator'

    # def get_installed_apps(self):
    #     for a in super(Site, self). get_installed_apps():
    #         yield a
    #     yield 'lino_welfare.modlib.projects'
    #     yield 'lino_welfare.modlib.polls'

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        # remove whole apps:
        kw.update(debts=None)
        kw.update(aids=None)
        kw.update(sepa=None)
        kw.update(iban=None)
        kw.update(badges=None)
        kw.update(properties=None)
        # alternative implementations:
        kw.update(courses='lino_welfare.projects.chatelet.modlib.courses')
        kw.update(pcsw='lino_welfare.projects.chatelet.modlib.pcsw')
        kw.update(isip='lino_welfare.projects.chatelet.modlib.isip')
        kw.update(cv='lino_welfare.projects.chatelet.modlib.cv')
        return kw

    # def setup_plugins(self):
    #     """
    #     Change the default value of certain plugin settings.

    #     """
    #     self.plugins.courses.configure(pupil_model='pcsw.Client')
    #     # self.plugins.courses.configure(teacher_model='users.User')
    #     super(Site, self).setup_plugins()

    # def get_default_language(self):
    #     return 'fr'

    def setup_choicelists(self):
        """
        This defines default user profiles for
        :mod:`lino_welfare.settings.chatelet`.
        """

        # must import it to activate workflows:
        from lino.modlib.courses import workflows

        from django.utils.translation import ugettext_lazy as _
        from lino.modlib.users.mixins import UserProfiles
        UserProfiles.reset(
            '* office coaching integ courses cbss newcomers '
            'reception beid')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),                   '_ _ _ _ _ _ _ _ _',
            name='anonymous',
            readonly=True,
            authenticated=False)
        add('100', _("Integration Agent"),           'U U U U U U _ _ U')
        add('110', _("Integration Agent (Manager)"), 'U M M M M U _ _ U')
        add('200', _("Newcomers consultant"),        'U U U _ M U U _ U')
        add('210', _("Reception clerk"),             'U U _ _ _ _ _ U U')
        add('400', _("Social agent"),                'U U U _ U U _ _ U')
        add('410', _("Social agent (Manager)"),      'U M M _ M U _ _ U')
        add('900', _("Administrator"),               'A A A A A A A A U',
            name='admin')

    def get_admin_main_items(self):

        # Mathieu: je remarque que le module "Visiteurs qui
        # m'attendent" ne fonctionne plus. Hors, c'est surtout ce
        # système qui est intéressant pour les travailleurs sociaux
        # qui attendent leurs rdv ou qui tiennent des permanences.

        yield self.modules.reception.MyWaitingVisitors
        yield self.modules.cal.MyEvents
        yield self.modules.cal.MyTasks
        
        yield self.modules.reception.WaitingVisitors
        yield self.modules.integ.UsersWithClients
        #~ yield self.modules.reception.ReceivedVisitors


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
