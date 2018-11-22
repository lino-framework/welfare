# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
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
"""Defines application workflows. 
"""

from lino.api import dd, _

from lino_xl.lib.reception.workflows import *
from lino_xl.lib.excerpts.choicelists import Shortcuts

# self.actors.cal.EntryStates.published.text = _("Notified")

Shortcuts.add_item('pcsw.Client', 'cvs_emitted', _("CVs emitted"))

from lino.modlib.uploads.choicelists import add_shortcut as add
add('pcsw.Client', 'id_document', _("Identifying document"),
    target='uploads.UploadsByClient')
# from lino.modlib.uploads.choicelists import Shortcuts
# Shortcuts.add_item(
#     'pcsw.Client', 'id_document', _("Identifying document"),
#     target='uploads.UploadsByClient')

from lino_xl.lib.notes.choicelists import SpecialTypes
add = SpecialTypes.add_item
add('100', _("First meeting"), 'first_meeting')

from .user_types import OfficeUser, OfficeOperator, ContactsUser, ContactsStaff

# Excerpts must be visible only to ContactsUser
from lino_xl.lib.excerpts.models import ExcerptsByProject
ExcerptsByProject.required_roles = dd.login_required(
    ContactsUser, (OfficeUser, OfficeOperator))

# from lino.api import dd, rt
# lib = rt.models
# for m in (lib.pcsw.Client, lib.contacts.Company, lib.countries.Place):
#     #~ print repr(m)
#     m.define_action(merge_row=dd.MergeAction(
#         m, required_roles=set([ContactsStaff])))



from lino.modlib.uploads.choicelists import UploadAreas
UploadAreas.clear()
add = UploadAreas.add_item
add('10', _("Contract"), 'contract')
add('90', _("General"), 'general')

