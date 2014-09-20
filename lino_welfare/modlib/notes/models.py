# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The `models` module for :mod:`lino_welfare.modlib.notes`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd, rt

from lino.modlib.notes.models import *


class Note(Note):

    class Meta:
        verbose_name = _("Event/Note")
        verbose_name_plural = _("Events/Notes")

    def get_person(self):
        return self.project
    Note.person = property(get_person)


class NoteDetail(NoteDetail):

    main = """
    left:60 right:30
    """

    left = """
    date:10 time event_type:25 type:25
    project subject
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
    required = dd.required()
    column_names = ("date:8 time:5 event_type:10 type:10 "
                    "subject:40 user:10 *")
    auto_fit_column_widths = True


class NotesByCompany(NotesByCompany):
    required = dd.required()
    column_names = "date time project event_type type subject user *"


