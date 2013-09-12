# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

"""
The `models` module for :mod:`lino_welfare.modlib.notes`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

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
    date:10 event_type:25 type:25
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
project company
"""
    
