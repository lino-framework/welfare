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
contacts = dd.resolve_app('contacts')


class UploadType(UploadType):
    """Extends the library model by adding warn_expiry info.
    """
    warn_expiry_unit = cal.Recurrencies.field(
        _("Expiry warning (unit)"),
        default=cal.Recurrencies.monthly,
        blank=True)  # iCal:DURATION
    warn_expiry_value = models.IntegerField(
        _("Expiry warning (value)"),
        default=2)


class UploadTypes(UploadTypes):

    detail_layout = """
    id upload_area
    name
    warn_expiry_value warn_expiry_unit
    # company contact_person contact_role
    uploads.UploadsByType
    """

    insert_layout = """
    upload_area
    name
    warn_expiry_value warn_expiry_unit
    # company contact_person contact_role
    """


class Upload(Upload, contacts.ContactRelated):
    """Extends the library model by adding:

- ContactRelated
- client
- valid_from and valid_until
    """
    client = dd.ForeignKey(
        'pcsw.Client',
        null=True, blank=True)

    valid_from = models.DateField(
        blank=True, null=True,
        verbose_name=_("Valid from"))

    valid_until = models.DateField(
        blank=True, null=True,
        verbose_name=_("Valid until"))

    remark = models.TextField(_("Remark"), blank=True)

    # def on_create(self, ar):
    #     super(Upload, self).on_create(ar)
    #     if self.type:
    #         for k in ('company', 'contact_person', 'contact_role'):
    #             setattr(self, k, getattr(self.type, k))

    def save(self, *args, **kw):
        if isinstance(self.owner, dd.modules.pcsw.Client):
            self.client = self.owner
        elif isinstance(self.owner, dd.ProjectRelated):
            self.client = self.owner.project
        super(Upload, self).save(*args, **kw)
        self.update_reminders()

    def update_reminders(self):
        """Overrides :meth:`lino.core.model.Model.update_reminders`.

        """
        ut = self.type
        if not ut or not ut.warn_expiry_unit:
            return
        cal.update_reminder(
            1, self, self.user,
            self.valid_until,
            _("%s expires") % unicode(ut),
            ut.warn_expiry_value,
            ut.warn_expiry_unit)

    # def update_owned_instance(self, controllable):
    #     super(Upload, self).update_owned_instance(controllable)
    #     if isinstance(controllable, pcsw.Client):
    #         self.client = controllable


dd.update_field(
    Upload, 'company', verbose_name=_("Issued by (Organization)"))
dd.update_field(
    Upload, 'contact_person',
    verbose_name=_("Issued by (Person)"))


class UploadDetail(dd.FormLayout):
    "The Detail layout for Upload"

    main = """
    user client id
    type description valid_from valid_until
    company contact_person contact_role
    file owner
    remark cal.TasksByController
    """

# Uploads.detail_layout = UploadDetail()
# Uploads.insert_layout = """
# type file
# valid_from valid_until
# description
# """


class Uploads(Uploads):
    column_names = 'user client type file valid_from valid_until description *'


class UploadsByClient(UploadsByController):
    "Uploads by Client"
    # required = dd.required()
    master_key = 'client'
    column_names = "type valid_until description * "
    # auto_fit_column_widths = True

    insert_layout = """
    type valid_until
    file
    description
    """

    @classmethod
    def create_instance(self, ar, **kw):
        obj = super(UploadsByClient, self).create_instance(ar, **kw)
        obj.owner = obj.client
        return obj


class MedicalUploadsByClient(UploadsByClient):
    _upload_area = UploadAreas.medical


class CareerUploadsByClient(UploadsByClient):
    _upload_area = UploadAreas.cv


class OtherUploadsByClient(UploadsByClient):
    _upload_area = UploadAreas.other


def site_setup(site):
    site.modules.uploads.Uploads.set_detail_layout(UploadDetail())
    site.modules.uploads.Uploads.set_insert_layout("""
    type file
    valid_from valid_until
    description
    """)


