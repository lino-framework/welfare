# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality to make CBSS requests.

CBSS (Crossroads Bank for Social Security, French *Banque Carrefour de
la Sécurité Sociale*) is an information system for data exchange
between different Belgian government agencies.
`Official website <http://www.ksz-bcss.fgov.be>`__


.. autosummary::
   :toctree:

    mixins
    choicelists
    models
    tx25
    fixtures

.. rubric:: Plugin configuration


"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("CBSS")

    cbss_live_requests = False
    """Whether executing requests should try to really connect to the
    CBSS.  Real requests would fail with a timeout if run from behind
    an IP address that is not registered at the :term:`CBSS`.

    """

    #~ cbss_environment = None
    cbss_environment = 'test'
    """
    Either `None` or one of 'test', 'acpt' or 'prod'.
    
    Setting this to `None` means that the cbss app is "inactive" even
    if installed.

    """

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cbss.Sectors')
        m.add_action('cbss.Purposes')

    def setup_explorer_menu(self, site, profile, m):
        # if profile.cbss_level < site.modules.users.UserLevels.manager:
        #     return
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cbss.AllIdentifyPersonRequests')
        m.add_action('cbss.AllManageAccessRequests')
        m.add_action('cbss.AllRetrieveTIGroupsRequests')

