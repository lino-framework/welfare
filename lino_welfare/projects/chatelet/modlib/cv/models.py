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
from lino_welfare.modlib.jobs.mixins import SectorFunction

config = dd.apps.cv


class DoYouLike(dd.ChoiceList):
    """A list of possible answers to questions of type "How much do you
    like ...?".

    """
    verbose_name = _("Do you like?")

add = DoYouLike.add_item
add('0', _("certainly not"))
add('1', _("rather not"))
add('2', _("normally"), "default")
add('3', _("quite much"))
add('4', _("very much"))


class HowWell(dd.ChoiceList):

    """A list of possible answers to questions of type "How well ...?":
    "not at all", "a bit", "moderate", "quite well" and "very well"
    
    which are stored in the database as '0' to '4',
    and whose `__unicode__()` returns their translated text.

    """
    verbose_name = _("How well?")

add = HowWell.add_item
add('0', _("not at all"))
add('1', _("a bit"))
add('2', _("moderate"), "default")
add('3', _("quite well"))
add('4', _("very well"))


class CefLevel(dd.ChoiceList):

    """
    Levels of the Common European Framework (CEF).
    
    | http://www.coe.int/t/dg4/linguistic/CADRE_EN.asp
    | http://www.coe.int/t/dg4/linguistic/Source/ManualRevision-proofread-FINAL_en.pdf
    | http://www.telc.net/en/what-telc-offers/cef-levels/a2/
    
    """
    verbose_name = _("CEF level")
    verbose_name_plural = _("CEF levels")
    show_values = True

    #~ @classmethod
    #~ def display_text(cls,bc):
        #~ def fn(bc):
            #~ return u"%s (%s)" % (bc.value,unicode(bc))
        #~ return lazy(fn,unicode)(bc)

add = CefLevel.add_item
add('A1', _("basic language skills"))
add('A2', _("basic language skills"))
add('A2+', _("basic language skills"))
add('B1', _("independent use of language"))
add('B2', _("independent use of language"))
add('B2+', _("independent use of language"))
add('C1', _("proficient use of language"))
add('C2', _("proficient use of language"))
add('C2+', _("proficient use of language"))


#
# LanguageKnowledge
#
class LanguageKnowledge(dd.Model):

    """Specifies how well a certain Person knows a certain Language.
    Deserves more documentation."""
    class Meta:
        verbose_name = _("language knowledge")
        verbose_name_plural = _("language knowledges")

    allow_cascaded_delete = ['person']

    person = models.ForeignKey(config.person_model)
    language = dd.ForeignKey("languages.Language")
    spoken = HowWell.field(_("Spoken"), blank=True)
    written = HowWell.field(_("Written"), blank=True)
    spoken_passively = HowWell.field(_("Spoken (passively)"),
                                     blank=True)
    written_passively = HowWell.field(_("Written (passively)"),
                                      blank=True)
    native = models.BooleanField(_("native language"), default=False)
    cef_level = CefLevel.field(blank=True)  # ,null=True)

    def __unicode__(self):
        if self.language_id is None:
            return ''
        if self.cef_level:
            return u"%s (%s)" % (self.language, self.cef_level)
        if self.spoken > '1' and self.written > '1':
            return _(u"%s (s/w)") % self.language
        elif self.spoken > '1':
            return _(u"%s (s)") % self.language
        elif self.written > '1':
            return _(u"%s (w)") % self.language
        else:
            return unicode(self.language)


class LanguageKnowledges(dd.Table):
    model = LanguageKnowledge
    required = dd.required(
        user_groups='coaching', user_level='manager')


class LanguageKnowledgesByPerson(LanguageKnowledges):
    master_key = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    column_names = "language native spoken written cef_level"
    required = dd.required(user_groups='coaching')
    auto_fit_column_widths = True


class KnowledgesByLanguage(LanguageKnowledges):
    master_key = 'language'
    column_names = "person native spoken written cef_level"
    required = dd.required(user_groups='coaching')

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


class SoftskillType(dd.BabelNamed):
    class Meta:
        verbose_name = _("Soft skill type")
        verbose_name_plural = _("Soft skill types")


class SoftskillTypes(dd.Table):
    model = 'cv.SoftskillType'

    
class Softskill(PersonProperty):
    class Meta:
        verbose_name = _("Soft skill")
        verbose_name_plural = _("Soft skills")
    type = dd.ForeignKey('cv.SoftskillType')


class Softskills(dd.Table):
    model = 'cv.Softskill'


class SoftskillsByPerson(PropsByPerson, Softskills):
    column_names = 'type remark'

##
## OBSTACLES
##


class ObstacleType(dd.BabelNamed):
    class Meta:
        verbose_name = _("Obstacle type")
        verbose_name_plural = _("Obstacle types")


class ObstacleTypes(dd.Table):
    model = 'cv.ObstacleType'


class Obstacle(PersonProperty):
    class Meta:
        verbose_name = _("Obstacle")
        verbose_name_plural = _("Obstacle")
    type = dd.ForeignKey('cv.ObstacleType')
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
    m.add_action(SoftskillTypes)
    m.add_action(ObstacleTypes)


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action(LanguageKnowledges)
    m.add_action(Skills)
    m.add_action(Softskills)
    m.add_action(Obstacles)
