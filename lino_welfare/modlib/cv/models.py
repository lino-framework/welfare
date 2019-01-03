# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Rumma & Ko Ltd
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.
"""
The :xfile:`models.py` file for :mod:`lino_welfare.modlib.cv`.
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino_xl.lib.cv.models import *

from lino_welfare.modlib.integ.roles import IntegUser
from lino_welfare.modlib.pcsw.roles import SocialStaff

from lino_xl.lib.properties import models as properties


#
# PROPERTIES
#


class PersonProperty(properties.PropertyOccurence):

    """The occurrence of a given property on a given client. """

    allow_cascaded_delete = ['person']

    class Meta:
        app_label = 'cv'
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    person = dd.ForeignKey(dd.plugins.cv.person_model)
    remark = models.CharField(max_length=200,
                              blank=True,  # null=True,
                              verbose_name=_("Remark"))


class PersonProperties(dd.Table):
    model = 'cv.PersonProperty'
    hidden_columns = 'group id'
    required_roles = dd.login_required(SocialStaff)


class PropsByPerson(PersonProperties):

    """Shows the :class:`PersonProperty` instances of a :class:`Client
    <lino_welfare.modlib.pcsw.models.Client>`.

    """
    master_key = 'person'
    column_names = "property value remark *"
    required_roles = dd.login_required(IntegUser)
    #~ hidden_columns = 'id'
    auto_fit_column_widths = True


class PersonPropsByProp(PersonProperties):
    master_key = 'property'
    column_names = "person value remark *"

#~ class PersonPropsByType(dd.Table):
    #~ model = PersonProperty
    #~ master_key = 'type'
    #~ column_names = "person property value remark *"
    #~ hidden_columns = frozenset(['group'])


class ConfiguredPropsByPerson(PropsByPerson):

    """Base class for :class`SkillsByPerson`, :class`SoftSkillsByPerson`
    and :class`ObstaclesByPerson`.

    """

    propgroup_config_name = None

    typo_check = False  # to avoid warning "ConfiguredPropsByPerson
                       # defines new attribute(s) propgroup_config_name"

    @classmethod
    def get_known_values(self):
        pg = getattr(settings.SITE.site_config, self.propgroup_config_name)
        return dict(group=pg)

    @classmethod
    def get_actor_label(self):
        if self.propgroup_config_name is None:
            return self.__name__
        pg = getattr(settings.SITE.site_config, self.propgroup_config_name)
        if pg is None:
            return _("(SiteConfig %s is empty)" % self.propgroup_config_name)
        return dd.babelattr(pg, 'name')


class SkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_skills'


class SoftSkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_softskills'


class ObstaclesByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_obstacles'


def customize_siteconfig():

    dd.inject_field(
        'system.SiteConfig',
        'propgroup_skills',
        dd.ForeignKey(
            'properties.PropGroup',
            blank=True, null=True,
            verbose_name=_("Skills Property Group"),
            related_name='skills_sites',
            help_text=_(
                "The property group to be used as master "
                "for the SkillsByPerson table.")))
    dd.inject_field(
        'system.SiteConfig',
        'propgroup_softskills',
        dd.ForeignKey(
            'properties.PropGroup',
            blank=True, null=True,
            verbose_name=_("Soft Skills Property Group"),
            related_name='softskills_sites',
            help_text=_(
                "The property group to be used as master "
                "for the SoftSkillsByPerson table.")))
    dd.inject_field(
        'system.SiteConfig',
        'propgroup_obstacles',
        dd.ForeignKey(
            'properties.PropGroup',
            blank=True, null=True,
            verbose_name=_("Obstacles Property Group"),
            related_name='obstacles_sites',
            help_text=_(
                "The property group to be used as master "
                "for the ObstaclesByPerson table.")))


customize_siteconfig()


@dd.receiver(dd.post_analyze)
def set_detail_layouts(sender=None, **kwargs):
    rt.models.properties.Properties.set_detail_layout("""
    id group type
    name
    cv.PersonPropsByProp
    """)
    Sectors.set_detail_layout("""
    id name
    remark FunctionsBySector
    cv.ExperiencesBySector
    jobs.CandidaturesBySector
    """)
    Functions.set_detail_layout("""
    id name sector
    remark
    jobs.CandidaturesByFunction
    cv.ExperiencesByFunction
    """)


def properties_list(owner, *prop_ids):
    for pk in prop_ids:
        try:
            yield owner.personproperty_set.get(property__id=pk)
        except PersonProperty.DoesNotExist:
            pass

