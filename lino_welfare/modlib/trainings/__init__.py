# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Provides for managing "immersion trainings" (stages d'immersion).

A tested document is here: :ref:`welfare.tested.trainings`

.. autosummary::
   :toctree:

   models

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("Immersion trainings")

    needs_plugins = ['lino_welfare.modlib.jobs']

    def setup_main_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('trainings.MyTrainings')

    def setup_config_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('trainings.TrainingTypes')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('trainings.Trainings')
