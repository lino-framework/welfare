# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines application workflows.
"""

from lino.api import dd, _

from lino_xl.lib.reception.workflows import *
from lino_xl.lib.excerpts.choicelists import Shortcuts

# self.actors.cal.EntryStates.published.text = _("Notified")

Shortcuts.add_item('pcsw.Client', 'cvs_emitted', _("CVs emitted"))

# from lino.modlib.uploads.choicelists import add_shortcut as add
# add('pcsw.Client', 'id_document', _("Identifying document"),
#     target='uploads.UploadsByProject')
# from lino.modlib.uploads.choicelists import Shortcuts
# Shortcuts.add_item(
#     'pcsw.Client', 'id_document', _("Identifying document"),
#     target='uploads.UploadsByProject')

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
