# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
The `models` module for :mod:`lino_welfare.modlib.notes`.
"""

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _

from django.conf import settings

from lino.api import dd, rt

from lino_xl.lib.notes.models import *
from lino.modlib.office.roles import OfficeUser, OfficeOperator
from lino_xl.lib.contacts.roles import ContactsUser

class Note(Note):
    """Overrides the library model, setting an alternative verbose name,
    adding a real database field :attr:`important` and the
    :attr:`person` property.

    .. attribute:: important

        Checking this will cause this note to appear in the
        :attr:`overview
        <lino_welfare.modlib.pcsw.models.Client.overview>` panel of
        the :attr:`person` linked to this note.

    .. attribute:: person

        An alias to :attr:`lino_xl.lib.notes.models.Note.project`.

    """
    class Meta:
        verbose_name = _("Event/Note")
        verbose_name_plural = _("Events/Notes")

    important = models.BooleanField(_('Important'), default=False)

    def get_person(self):
        return self.project
    
    person = property(get_person)

    def get_notify_message_type(self):
        return rt.models.notify.MessageTypes.coachings
    

class NoteDetail(NoteDetail):

    main = """
    left:60 right:30
    """

    left = """
    date:10 time event_type:25 type:25
    project subject important
    company contact_person #contact_role
    user:10 language:8 build_time id
    body
    """

    right = """
    uploads.UploadsByController
    outbox.MailsByController
    # postings.PostingsByController
    cal.TasksByController
    """


Notes.detail_layout = NoteDetail()
Notes.insert_layout = """
event_type:25 type:25
subject
project #company
"""


class NotesByProject(NotesByProject):
    required_roles = dd.login_required(ContactsUser, (OfficeUser, OfficeOperator))
    # required_roles = dd.login_required()
    column_names = ("date:8 time:5 event_type:10 type:10 "
                    "subject:40 user:10 *")
    auto_fit_column_widths = True


class NotesByCompany(NotesByCompany):
    required_roles = dd.login_required(ContactsUser, (OfficeUser, OfficeOperator))
    # required_roles = dd.login_required()
    column_names = "date time project event_type type subject user *"


