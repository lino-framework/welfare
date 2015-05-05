# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The `models` module for :mod:`lino_welfare.modlib.notes`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from lino.api import dd, rt

from lino.modlib.notes.models import *


class Note(Note):

    class Meta:
        verbose_name = _("Event/Note")
        verbose_name_plural = _("Events/Notes")

    def get_person(self):
        return self.project
    Note.person = property(get_person)


@dd.receiver(dd.on_ui_updated, sender=Note)
def myhandler(sender=None, watcher=None, request=None, **kwargs):
    obj = watcher.watched
    if obj.project is None:
        return
    recipients = []
    period = (dd.today(), dd.today())
    for c in obj.project.get_coachings(period, user__email__gt=''):
        if c.user != request.user:
            recipients.append(c.user.email)
    if len(recipients) == 0:
        return
    context = dict(obj=obj, request=request)
    subject = "Modification dans {obj}".format(**context)
    tpl = rt.get_template('notes/note_updated.eml')
    body = tpl.render(**context)
    sender = request.user.email or settings.SERVER_EMAIL
    # dd.logger.info("20150505 %s", recipients)
    rt.send_email(subject, sender, body, recipients)


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


