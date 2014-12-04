# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd, mixins
from lino.modlib.excerpts.mixins import Certifiable


class ProjectType(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Client project type")
        verbose_name_plural = _("Client project types")


class ProjectTypes(dd.Table):
    model = 'projects.ProjectType'
    required = dd.required(user_level='admin')


class Project(mixins.DatePeriod, Certifiable):

    class Meta:
        verbose_name = _("Client Project")
        verbose_name_plural = _("Client Projects")

    client = dd.ForeignKey('pcsw.Client')
    project_type = dd.ForeignKey('projects.ProjectType')
    origin = dd.RichTextField(_("Initial situation"), blank=True)
    target = dd.RichTextField(_("Aimed target"), blank=True)
    remark = models.CharField(_("Remark"), blank=True, max_length=200)
    result = models.CharField(_("Result"), blank=True, max_length=200)


class Projects(dd.Table):
    model = 'projects.Project'
    required = dd.required(user_level='admin')

    detail_layout = """
    id client project_type start_date end_date
    origin target
    remark result
    """

    insert_layout = """
    client project_type
    start_date end_date
    """


class ProjectsByClient(Projects):
    required = dd.required()
    master_key = 'client'
    column_names = 'start_date project_type result remark'
    auto_fit_column_widths = True

    insert_layout = """
    project_type
    start_date end_date
    """


class ProjectsByType(Projects):
    required = dd.required()
    master_key = 'project_type'
    column_names = 'start_date client result remark'
    auto_fit_column_widths = True


def setup_config_menu(site, ui, profile, m):
    p = dd.apps.projects
    m = m.add_menu(p.app_label, p.verbose_name)
    m.add_action('projects.ProjectTypes')


def setup_explorer_menu(site, ui, profile, m):
    p = dd.apps.projects
    m = m.add_menu(p.app_label, p.verbose_name)
    m.add_action('projects.Projects')


