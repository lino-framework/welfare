# Copyright 2014-2015 Luc Saffre
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import gettext_lazy as _

from lino.api import dd
from lino import mixins

from lino_xl.lib.excerpts.mixins import Certifiable
from lino.modlib.users.choicelists import SiteStaff


class ProjectType(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Client project type")
        verbose_name_plural = _("Client project types")


class ProjectTypes(dd.Table):
    model = 'projects.ProjectType'
    required_roles = dd.login_required(SiteStaff)


class Project(mixins.DateRange, Certifiable):

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
    required_roles = dd.login_required(SiteStaff)

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
    required_roles = dd.login_required()
    master_key = 'client'
    column_names = 'start_date project_type result remark'
    auto_fit_column_widths = True

    insert_layout = """
    project_type
    start_date end_date
    """


class ProjectsByType(Projects):
    required_roles = dd.login_required()
    master_key = 'project_type'
    column_names = 'start_date client result remark'
    auto_fit_column_widths = True


