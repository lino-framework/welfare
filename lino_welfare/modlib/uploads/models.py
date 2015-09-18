# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
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
Database model overrides for :mod:`lino_welfare.modlib.uploads`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino.modlib.uploads.models import *
from lino.modlib.contacts.mixins import ContactRelated
from lino.modlib.cal.utils import update_reminder, Recurrencies


# add = UploadAreas.add_item
# add('10', _("Job search uploads"), 'job_search')
# add('20', _("Medical uploads"), 'medical')
# add('30', _("Career uploads"), 'career')


class UploadType(UploadType):
    """Extends the library model by adding `warn_expiry` info.

    """
    warn_expiry_unit = Recurrencies.field(
        _("Expiry warning (unit)"),
        default=Recurrencies.monthly,
        blank=True)  # iCal:DURATION
    warn_expiry_value = models.IntegerField(
        _("Expiry warning (value)"),
        default=2)

# dd.update_field(
#     'uploads.UploadType', 'upload_area', default=UploadAreas.job_search)


class UploadTypes(UploadTypes):
    column_names = "id name wanted max_number \
    warn_expiry_unit warn_expiry_value shortcut"

    detail_layout = """
    id upload_area shortcut
    name
    warn_expiry_unit warn_expiry_value wanted max_number
    uploads.UploadsByType
    """

    insert_layout = """
    upload_area
    name
    warn_expiry_unit warn_expiry_value
    # company contact_person contact_role
    """


class Upload(Upload, mixins.ProjectRelated, ContactRelated,
             mixins.DatePeriod):
    """Extends the library model by adding the `ContactRelated`,
    `ProjectRelated` and `DatePeriod` mixins and two fields.

    .. attribute:: remark
    
        A remark about this document.

    .. attribute:: needed
    
        Whether this particular upload is a needed document. Default value
        is `True` if the new Upload has an UploadType with a nonempty
        `warn_expiry_unit`.

    """
    # valid_from = models.DateField(_("Valid from"), blank=True, null=True)
    # valid_until = models.DateField(_("Valid until"), blank=True, null=True)

    remark = models.TextField(_("Remark"), blank=True)
    needed = models.BooleanField(_("Needed"), default=True)

    def on_create(self, ar):
        super(Upload, self).on_create(ar)
        if self.type and self.type.warn_expiry_unit:
            self.needed = True
        else:
            self.needed = False

    def save(self, *args, **kw):
        super(Upload, self).save(*args, **kw)
        self.update_reminders()

    def update_reminders(self):
        """Overrides :meth:`lino.core.model.Model.update_reminders`.

        """
        ut = self.type
        if not ut or not ut.warn_expiry_unit:
            return
        if not self.needed:
            return
        update_reminder(
            1, self, self.user,
            self.end_date,
            _("%s expires") % unicode(ut),
            ut.warn_expiry_value,
            ut.warn_expiry_unit)


dd.update_field(
    Upload, 'company', verbose_name=_("Issued by (Organization)"))
dd.update_field(
    Upload, 'contact_person',
    verbose_name=_("Issued by (Person)"))
dd.update_field(Upload, 'start_date', verbose_name=_("Valid from"))
dd.update_field(Upload, 'end_date', verbose_name=_("Valid until"))
# dd.update_field(
#     Upload, 'upload_area', default=UploadAreas.job_search)


class UploadDetail(dd.FormLayout):
    "The Detail layout for Upload"

    main = """
    user project id
    type description start_date end_date needed
    company contact_person contact_role
    file owner
    remark cal.TasksByController
    """

LibraryUploads = Uploads


class Uploads(Uploads):
    column_names = 'user project type file start_date end_date ' \
                   'description *'

    detail_layout = UploadDetail()

    insert_layout = """
    type file
    start_date end_date
    description
    """

    parameters = mixins.ObservedPeriod(
        # puser=models.ForeignKey(
        #     'users.User', blank=True, null=True,
        #     verbose_name=_("Uploaded by")),
        upload_type=models.ForeignKey(
            'uploads.UploadType', blank=True, null=True),
        coached_by=models.ForeignKey(
            'users.User',
            blank=True, null=True,
            verbose_name=_("Coached by"),
            help_text=_(
                "Show only uploads for clients coached by this user.")),
        observed_event=dd.PeriodEvents.field(
            _("Validity"),
            blank=True, default=dd.PeriodEvents.active))
    params_layout = "observed_event:20 start_date end_date \
    coached_by user upload_type"

    auto_fit_column_widths = True

    @classmethod
    def get_request_queryset(cls, ar):
        # (why was this?) use inherited method from grandparent (not
        # direct parent)
        # qs = super(LibraryUploads, cls).get_request_queryset(ar)
        qs = super(Uploads, cls).get_request_queryset(ar)
        pv = ar.param_values

        ce = pv.observed_event
        if ce is not None:
            qs = ce.add_filter(qs, pv)

        # if pv.puser:
        #     qs = qs.filter(user=pv.puser)

        if pv.coached_by:
            qs = qs.filter(project__coachings_by_client__user=pv.coached_by)
            qs = qs.filter(needed=True)
            
        # if pv.pupload_type:
        #     qs = qs.filter(type=pv.pupload_type)

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Uploads, self).get_title_tags(ar):
            yield t

        pv = ar.param_values

        if pv.observed_event:
            yield unicode(pv.observed_event)

        if pv.coached_by:
            yield unicode(self.parameters['coached_by'].verbose_name) + \
                ' ' + unicode(pv.coached_by)

        if pv.user:
            yield unicode(self.parameters['user'].verbose_name) + \
                ' ' + unicode(pv.user)


class UploadsByType(Uploads, UploadsByType):
    pass


class MyUploads(My, Uploads):
    required_roles = dd.required((OfficeUser, OfficeOperator))
    column_names = "id project type start_date end_date \
    needed description file *"


class MyExpiringUploads(MyUploads):
    "Expiring uploads for client coached by me"
    required_roles = dd.required((OfficeUser, OfficeOperator))
    label = _("My expiring uploads")
    help_text = _("Show needed uploads whose validity expires soon")
    column_names = "project type user start_date end_date needed *"
    order_by = ['end_date']

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyExpiringUploads, self).param_defaults(ar, **kw)
        kw.update(coached_by=ar.get_user())
        kw.update(observed_event=dd.PeriodEvents.ended)
        kw.update(start_date=dd.today())
        kw.update(end_date=dd.today(365))
        return kw


class AreaUploads(Uploads, AreaUploads):
    pass


class UploadsByController(Uploads, UploadsByController):
    insert_layout = """
    file
    type end_date
    description
    """


class UploadsByClient(AreaUploads, UploadsByController):
    "Uploads by Client"
    master = 'pcsw.Client'
    master_key = 'project'
    column_names = "type end_date needed description user file *"
    # auto_fit_column_widths = True
    # debug_sql = "20140519"

    insert_layout = """
    file
    type end_date
    description
    """

    @classmethod
    def create_instance(self, ar, **kw):
        obj = super(UploadsByClient, self).create_instance(ar, **kw)
        obj.owner = obj.project
        return obj

    @classmethod
    def format_row_in_slave_summary(self, ar, obj):
        if obj.end_date and obj.end_date < settings.SITE.today():
            return None
        return super(UploadsByClient, self).format_row_in_slave_summary(
            ar, obj)

# class JobSearchUploadsByClient(UploadsByClient):
#     _upload_area = UploadAreas.job_search


# class MedicalUploadsByClient(UploadsByClient):
#     _upload_area = UploadAreas.medical


# class CareerUploadsByClient(UploadsByClient):
#     _upload_area = UploadAreas.career


def unused_site_setup(site):
    uploads = site.modules.uploads
    uploads.Uploads.set_detail_layout(UploadDetail())
    # uploads.Uploads.set_insert_layout("""
    # type file
    # start_date end_date
    # description
    # """)
    uploads.UploadsByController.set_insert_layout("""
    file
    type
    start_date end_date
    description
    """)
