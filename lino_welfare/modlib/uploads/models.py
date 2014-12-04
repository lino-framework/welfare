# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The `models` module for :mod:`lino_welfare.modlib.uploads`.

"""

from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import string_concat

from lino import dd, rt

from lino.modlib.uploads.models import *

cal = dd.resolve_app('cal')
contacts = dd.resolve_app('contacts')


# add = UploadAreas.add_item
# add('10', _("Job search uploads"), 'job_search')
# add('20', _("Medical uploads"), 'medical')
# add('30', _("Career uploads"), 'career')


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

# dd.update_field(
#     'uploads.UploadType', 'upload_area', default=UploadAreas.job_search)


class UploadTypes(UploadTypes):

    detail_layout = """
    id upload_area
    name
    warn_expiry_value warn_expiry_unit wanted max_number
    # company contact_person contact_role
    uploads.UploadsByType
    """

    insert_layout = """
    upload_area
    name
    warn_expiry_value warn_expiry_unit
    # company contact_person contact_role
    """


class Upload(Upload, mixins.ProjectRelated, contacts.ContactRelated):
    """Extends the library model by adding:

- ContactRelated
- ProjectRelated
- `valid_from` and `valid_until`
    """
    valid_from = models.DateField(
        blank=True, null=True,
        verbose_name=_("Valid from"))

    valid_until = models.DateField(
        blank=True, null=True,
        verbose_name=_("Valid until"))

    remark = models.TextField(_("Remark"), blank=True)

    def save(self, *args, **kw):
        super(Upload, self).save(*args, **kw)
        self.update_reminders()

    def update_reminders(self):
        """Overrides :meth:`dd.Model.update_reminders`.

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
    #     if isinstance(controllable, rt.modules.pcsw.Client):
    #         self.client = controllable


dd.update_field(
    Upload, 'company', verbose_name=_("Issued by (Organization)"))
dd.update_field(
    Upload, 'contact_person',
    verbose_name=_("Issued by (Person)"))
# dd.update_field(
#     Upload, 'upload_area', default=UploadAreas.job_search)


class UploadDetail(dd.FormLayout):
    "The Detail layout for Upload"

    main = """
    user project id
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
    column_names = 'user project type file valid_from valid_until ' \
                   'description *'


class UploadsByClient(AreaUploads):
    "Uploads by Client"
    master = 'pcsw.Client'
    master_key = 'project'
    column_names = "type valid_until description user file *"
    # auto_fit_column_widths = True
    # debug_sql = "20140519"

    insert_layout = """
    type valid_until
    file
    description
    """

    @classmethod
    def create_instance(self, ar, **kw):
        obj = super(UploadsByClient, self).create_instance(ar, **kw)
        obj.owner = obj.project
        return obj

    @classmethod
    def format_row_in_slave_summary(self, ar, obj):
        if obj.valid_until and obj.valid_until < settings.SITE.today():
            return None
        return super(UploadsByClient, self).format_row_in_slave_summary(
            ar, obj)


# class JobSearchUploadsByClient(UploadsByClient):
#     _upload_area = UploadAreas.job_search


# class MedicalUploadsByClient(UploadsByClient):
#     _upload_area = UploadAreas.medical


# class CareerUploadsByClient(UploadsByClient):
#     _upload_area = UploadAreas.career


def site_setup(site):
    site.modules.uploads.Uploads.set_detail_layout(UploadDetail())
    site.modules.uploads.Uploads.set_insert_layout("""
    type file
    valid_from valid_until
    description
    """)


