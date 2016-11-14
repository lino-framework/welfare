# -*- coding: UTF-8 -*-
# Copyright 2008-2016 Luc Saffre
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

"""Database models for `lino_welfare.modlib.pcsw`.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino_welfare.modlib.newcomers.roles import NewcomersAgent

from .choicelists import RefusalReasons, ClientStates


class ChangeStateAction(dd.Action):
    show_in_bbar = False
    show_in_workflow = True
    confirm_msg = _("This will put {client} "
                    "into state <b>{state}</b>.")
    done_msg = _("{user} marked {client} as <b>{state}</b>.")


class RefuseClient(ChangeStateAction):
    """
    Refuse this newcomer request.
    """
    label = _("Refuse")
    required_states = 'newcomer'
    required_roles = dd.required(NewcomersAgent)
    target_state = ClientStates.refused

    parameters = dict(
        reason=RefusalReasons.field(),
        remark=dd.RichTextField(_("Remark"), blank=True),
    )

    params_layout = dd.Panel("""
    reason
    remark
    """, window_size=(50, 15))

    def run_from_ui(self, ar, **kw):

        obj = ar.selected_rows[0]
        # run the query before we end the coachings:
        recipients = list(obj.get_change_observers())

        # obj is a Client instance
        obj.refusal_reason = ar.action_param_values.reason
        obj.state = ClientStates.refused
        obj.full_clean()
        obj.save()

        subject = self.done_msg.format(
            client=obj, user=ar.get_user(), state=self.target_state)
        body = unicode(ar.action_param_values.reason)
        if ar.action_param_values.remark:
            body += '\n' + ar.action_param_values.remark
        kw = dict()
        kw.update(message=subject)
        kw.update(alert=_("Success"))
        obj.emit_system_note(
            ar, subject=subject, body=body)
        rt.models.notify.Message.emit_message(
            ar, obj, subject, body, recipients)
        ar.success(**kw)


class MarkClientFormer(ChangeStateAction):
    """Change client's state to 'former'. This will also end any active
    coachings.

    """
    label = _("Former")
    required_states = 'coached'
    required_roles = dd.required(NewcomersAgent)
    target_state = ClientStates.former

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        # obj is a Client instance

        # run the query before we end the coachings:
        recipients = list(obj.get_change_observers())

        def doit(ar):
            obj.state = self.target_state
            obj.full_clean()
            obj.save()
            subject = self.done_msg.format(
                client=obj, user=ar.get_user(), state=self.target_state)
            kw = dict()
            kw.update(message=subject)
            kw.update(alert=_("Success"))
            obj.emit_system_note(ar, subject=subject)
            rt.models.notify.Message.emit_message(
                ar, obj, subject, "", recipients)
            ar.success(**kw)
            
        qs = obj.coachings_by_client.filter(end_date__isnull=True)
        if qs.count() == 0:
            return ar.confirm(
                doit,
                self.confirm_msg.format(
                    client=obj, state=self.target_state))

            doit(ar)
        else:
            def ok(ar):
                # subject = _("{0} state set to former")
                # obj.emit_system_note(ar, obj, subject, body)
                for co in qs:
                    # co.state = CoachingStates.ended
                    co.end_date = dd.today()
                    co.save()
                doit(ar)
            return ar.confirm(
                ok,
                _("This will end %(count)d coachings of %(client)s.")
                % dict(count=qs.count(), client=unicode(obj)))


