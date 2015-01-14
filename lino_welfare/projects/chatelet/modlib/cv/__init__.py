# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Chatelet version of :mod:`welfare.cv`
"""

from lino.modlib.cv import Plugin


class Plugin(Plugin):

    def setup_config_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('cv.SoftSkillTypes')
        m.add_action('cv.ObstacleTypes')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('cv.LanguageKnowledges')
        m.add_action('cv.Skills')
        m.add_action('cv.SoftSkills')
        m.add_action('cv.Obstacles')
