# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the :mod:`lino_welfare` app.

Contains PCSW-specific models and tables that have not yet been 
moved into a separate module because they are really very PCSW specific.

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.core.roles import SiteStaff
from lino_xl.lib.contacts.roles import ContactsStaff

households = dd.resolve_app('households')
#~ cal = dd.resolve_app('cal')
properties = dd.resolve_app('properties')
countries = dd.resolve_app('countries')
contacts = dd.resolve_app('contacts')
cv = dd.resolve_app('cv')
# uploads = dd.resolve_app('uploads')
# auth = dd.resolve_app('auth')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
pcsw = dd.resolve_app('pcsw')
courses = dd.resolve_app('courses')
#~ from lino_welfare.modlib.isip import models as isip
#~ newcomers = dd.resolve_app('newcomers')


@dd.receiver(dd.pre_analyze)
def customize_siteconfig(sender, **kw):
    """
    Injects application-specific fields to
    :class:`SiteConfig <lino.models.SiteConfig>`.
    """

    dd.inject_field('system.SiteConfig',
                    'job_office',
                    dd.ForeignKey('contacts.Company',
                                      blank=True, null=True,
                                      verbose_name=_("Local job office"),
                                      related_name='job_office_sites',
            help_text="""The Company whose contact persons 
            will be choices for `Person.job_office_contact`."""))

    dd.inject_field('system.SiteConfig',
                    'residence_permit_upload_type',
                    dd.ForeignKey("uploads.UploadType",
                                      blank=True, null=True,
                                      verbose_name=_(
                                          "Upload Type for residence permit"),
                                      related_name='residence_permit_sites'))

    dd.inject_field('system.SiteConfig',
                    'work_permit_upload_type',
                    #~ UploadType.objects.get(pk=2)
                    dd.ForeignKey("uploads.UploadType",
                                      blank=True, null=True,
                                      verbose_name=_(
                                          "Upload Type for work permit"),
                                      related_name='work_permit_sites'))

    dd.inject_field('system.SiteConfig',
                    'driving_licence_upload_type',
                    dd.ForeignKey("uploads.UploadType",
                                      blank=True, null=True,
                                      verbose_name=_(
                                          "Upload Type for driving licence"),
                                      related_name='driving_licence_sites'))


@dd.receiver(dd.pre_analyze)
def customize_contacts(sender, **kw):
    """
    Injects application-specific fields to :mod:`contacts <lino_xl.lib.contacts>`.
    """
    dd.inject_field(
        contacts.RoleType,
        'use_in_contracts',
        models.BooleanField(
            verbose_name=_("usable in contracts"),
            default=True,
            help_text=_(
                "Whether Links of this type can be used "
                "as contact person of a job contract.")))


@dd.receiver(dd.auto_create)
def on_auto_create(sender, **kw):
    #~ raise Warning("auto_create is not permitted here")
    logger.info("auto_create %s %s", dd.obj2str(sender), kw)
    from django.core.mail import mail_admins
    body = 'Record %s has been automatically created using %s' % (
        dd.obj2str(sender), kw)
    mail_admins('auto_create', body, fail_silently=True)

#~ dd.auto_create.connect(on_auto_create)


@dd.receiver(dd.pre_analyze)
def customize_sqlite(sender, **kw):
    """
    Here is how we install case-insensitive sorting in sqlite3.
    Note that this caused noticeable performance degradation...

    Thanks to 
    - http://efreedom.com/Question/1-3763838/Sort-Order-SQLite3-Umlauts
    - http://docs.python.org/library/sqlite3.html#sqlite3.Connection.create_collation
    - http://www.sqlite.org/lang_createindex.html
    """
    from django.db.backends.signals import connection_created

    def belgian(s):

        s = s.decode('utf-8').lower()

        s = s.replace(u'ä', u'a')
        s = s.replace(u'à', u'a')
        s = s.replace(u'â', u'a')

        s = s.replace(u'ç', u'c')

        s = s.replace(u'é', u'e')
        s = s.replace(u'è', u'e')
        s = s.replace(u'ê', u'e')
        s = s.replace(u'ë', u'e')

        s = s.replace(u'ö', u'o')
        s = s.replace(u'õ', u'o')
        s = s.replace(u'ô', u'o')

        s = s.replace(u'ß', u'ss')

        s = s.replace(u'ù', u'u')
        s = s.replace(u'ü', u'u')
        s = s.replace(u'û', u'u')

        return s

    def stricmp(str1, str2):
        return cmp(belgian(str1), belgian(str2))

    def my_callback(sender, **kw):
        from django.db.backends.sqlite3.base import DatabaseWrapper
        if sender is DatabaseWrapper:
            db = kw['connection']
            db.connection.create_collation('BINARY', stricmp)

    connection_created.connect(my_callback)


# moved to user_types_module    
# @dd.receiver(dd.pre_analyze)
# def set_merge_actions(sender, **kw):
#     #~ logger.info("20130409 %s.set_merge_actions()",__name__)
#     lib = sender.modules
#     for m in (lib.pcsw.Client, lib.contacts.Company, lib.countries.Place):
#         #~ print repr(m)
#         m.define_action(merge_row=dd.MergeAction(
#             m, required_roles=set([(SiteStaff, ContactsStaff)])))
#         #~ m.merge_row = dd.MergeAction(m)



@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    site = sender
    site.modules.countries.Places.set_detail_layout("""
    name country inscode zip_code
    parent type id
    PlacesByPlace
    contacts.PartnersByCity cv.StudiesByPlace
    """)

    site.modules.countries.Countries.set_detail_layout("""
    isocode name short_code:10 inscode actual_country
    # nationalities
    countries.PlacesByCountry cv.StudiesByCountry
    """)

