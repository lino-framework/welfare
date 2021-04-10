# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Provides data definitions used by the Integration Service.


.. autosummary::
   :toctree:

   roles
   fixtures.demo

"""

from lino import ad

from django.utils.translation import gettext_lazy as _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Integration")

    only_primary = False
    """Whether to show only primary coachings in the dynamic ventilation
    columns (coachings per :class:`PersonGroup
    <lino_welfare.modlib.pcsw.models.PersonGroup>) of the
    :class:`UsersWithClients
    <lino_welfare.modlib.integ.models.UsersWithClients>` table.

    """

    def setup_reports_menu(config, site, user_type, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        #~ m.add_action(site.modules.jobs.OldJobsOverview)
        m.add_action(site.modules.integ.UsersWithClients)

        m.add_action('jobs.JobsOverview')
        m.add_action('integ.ActivityReport')

    def setup_main_menu(config, site, user_type, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('integ.Clients')
        m.add_action('isip.MyContracts')

        m.add_action('jobs.MyContracts')
        m.add_action('jobs.JobProviders')
        m.add_action('jobs.Jobs')
        m.add_action('jobs.Offers')

    def setup_config_menu(config, site, user_type, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('isip.ContractTypes')
        m.add_action('isip.ContractEndings')
        m.add_action('isip.ExamPolicies')

        m.add_action('jobs.ContractTypes')
        m.add_action('jobs.JobTypes')
        m.add_action('jobs.Schedules')

    def setup_explorer_menu(config, site, user_type, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('isip.Contracts')
        m.add_action('jobs.Contracts')
        m.add_action('jobs.Candidatures')
        m.add_action('isip.ContractPartners')
