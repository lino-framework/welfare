# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

"""
The `models` module for :mod:`lino_welfare.modlib.uploads`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import string_concat

from lino import dd

from lino.modlib.uploads.models import *

cal = dd.resolve_app('cal')


class Upload(Upload):

    client = dd.ForeignKey(
        'pcsw.Client',
        null=True, blank=True)

    valid_from = models.DateField(
        blank=True, null=True,
        verbose_name=_("Valid from"))

    valid_until = models.DateField(
        blank=True, null=True,
        verbose_name=_("Valid until"))

    def save(self, *args, **kw):
        super(Upload, self).save(*args, **kw)
        if isinstance(self.owner, dd.modules.pcsw.Client):
            self.client = self.owner
        self.update_reminders()

    def update_reminders(self):
        """Overrides :meth:`lino.core.model.Model.update_reminders`.

        """
        cal.update_reminder(
            1, self, self.user,
            self.valid_until,
            _("%s expires") % self.type,
            2, cal.DurationUnits.months)

    # def update_owned_instance(self, controllable):
    #     super(Upload, self).update_owned_instance(controllable)
    #     if isinstance(controllable, pcsw.Client):
    #         self.client = controllable


class UploadDetail(dd.FormLayout):

    main = """
    user client
    type description valid_from valid_until
    file owner
    cal.TasksByController
    """


def site_setup(site):
    site.modules.uploads.Uploads.set_detail_layout(UploadDetail())
    site.modules.uploads.Uploads.set_insert_layout("""
    type file
    valid_from valid_until
    description
    """)


class UploadsByClient(Uploads):
    required = dd.required()
    master_key = 'client'
    column_names = "file type description user * "

