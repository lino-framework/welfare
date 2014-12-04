# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

from lino.modlib.cv.models import *


LanguageKnowledgesByPerson.column_names = "language native spoken \
written spoken_passively written_passively *"


class PersonProperty(dd.Model):

    allow_cascaded_delete = ['person']

    class Meta:
        abstract = True

    person = models.ForeignKey(config.person_model)
    remark = models.CharField(max_length=200,
                              blank=True,  # null=True,
                              verbose_name=_("Remark"))


class PropsByPerson(dd.Table):
    master_key = 'person'
    auto_fit_column_widths = True
    

##
## SKILLS
##

class Skill(PersonProperty, SectorFunction):

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

dd.update_field(Skill, 'remark', verbose_name=_("Competences"))


class Skills(dd.Table):
    model = 'cv.Skill'


class SkillsByPerson(PropsByPerson, Skills):
    column_names = 'sector function remark'


##
## SOFTSKILLS
##


class SoftSkillType(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Soft skill type")
        verbose_name_plural = _("Soft skill types")


class SoftSkillTypes(dd.Table):
    model = 'cv.SoftSkillType'

    
class SoftSkill(PersonProperty):
    class Meta:
        verbose_name = _("Soft skill")
        verbose_name_plural = _("Soft skills")
    type = dd.ForeignKey('cv.SoftSkillType', verbose_name=_("Type"))


class SoftSkills(dd.Table):
    model = 'cv.SoftSkill'


class SoftSkillsByPerson(PropsByPerson, SoftSkills):
    column_names = 'type remark'

##
## OBSTACLES
##


class ObstacleType(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Obstacle type")
        verbose_name_plural = _("Obstacle types")


class ObstacleTypes(dd.Table):
    model = 'cv.ObstacleType'


class Obstacle(PersonProperty):
    class Meta:
        verbose_name = _("Obstacle")
        verbose_name_plural = _("Obstacles")
    type = dd.ForeignKey('cv.ObstacleType', verbose_name=_("Type"))
    user = dd.ForeignKey(
        'users.User',
        related_name='obstacles_detected',
        verbose_name=_("Detected by"),
        blank=True, null=True)


class Obstacles(dd.Table):
    model = 'cv.Obstacle'


class ObstaclesByPerson(PropsByPerson, Obstacles):
    column_names = 'type user remark'


dd.inject_field('system.SiteConfig', 'propgroup_skills', dd.DummyField())
dd.inject_field('system.SiteConfig', 'propgroup_softskills', dd.DummyField())
dd.inject_field('system.SiteConfig', 'propgroup_obstacles', dd.DummyField())


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action(SoftSkillTypes)
    m.add_action(ObstacleTypes)


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action(LanguageKnowledges)
    m.add_action(Skills)
    m.add_action(SoftSkills)
    m.add_action(Obstacles)
