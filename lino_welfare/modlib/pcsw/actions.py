# -*- coding: UTF-8 -*-
# Copyright 2008-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Database models for `lino_welfare.modlib.pcsw`.

"""

from __future__ import unicode_literals
from __future__ import print_function
from builtins import str
import six

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino_welfare.modlib.newcomers.roles import NewcomersUser

from lino_xl.lib.clients.choicelists import ClientStates
from .choicelists import RefusalReasons

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
    required_roles = dd.login_required(NewcomersUser)
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
        recipients = list(obj.get_change_observers(ar))

        # obj is a Client instance
        obj.refusal_reason = ar.action_param_values.reason
        obj.client_state = ClientStates.refused
        obj.full_clean()
        obj.save()

        ctx = dict(
            client=obj, user=ar.get_user(), state=self.target_state)
        subject = self.done_msg.format(**ctx)
        ctx.update(client=ar.obj2memo(obj))
        body = self.done_msg.format(**ctx)
        body += '\n{}: {}'.format(
            RefusalReasons.verbose_name, ar.action_param_values.reason)
        if ar.action_param_values.remark:
            body += '\n' + str(ar.action_param_values.remark)
        # dd.logger.info("20170412 %r", ar.action_param_values)
        # 20170412 seems that mysql does not support newstr:
        body = six.text_type(body)
        obj.emit_system_note(ar, subject=subject, body=body)
        mt = rt.models.notify.MessageTypes.coachings
        
        if subject:
            def msg(user, mm):
                return (subject, body)
            rt.models.notify.Message.emit_notification(
                ar, obj, mt, msg, recipients)
            
        kw = dict()
        kw.update(message=subject)
        kw.update(alert=_("Success"))
        ar.success(**kw)


class MarkClientFormer(ChangeStateAction):
    """
    Change client's state to 'former'. This will also end any active
    coachings.
    """
    label = _("Former")
    required_states = 'coached'
    required_roles = dd.login_required(NewcomersUser)
    target_state = ClientStates.former

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        # obj is a Client instance

        # run the query before we end the coachings:
        recipients = list(obj.get_change_observers(ar))

        mt = rt.models.notify.MessageTypes.coachings
        def doit(ar):
            obj.client_state = self.target_state
            obj.full_clean()
            obj.save()
            body = self.done_msg.format(
                client=obj, user=ar.get_user(), state=self.target_state)
            kw = dict()
            kw.update(message=body)
            kw.update(alert=_("Success"))
            obj.emit_system_note(ar, subject=body)
            
            def msg(user, mm):
                return (body, body)
            rt.models.notify.Message.emit_notification(
                ar, obj, mt, msg, recipients)
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
                for co in qs:
                    co.end_date = dd.today()
                    co.save()
                doit(ar)
            return ar.confirm(
                ok,
                _("This will end %(count)d coachings of %(client)s.")
                % dict(count=qs.count(), client=str(obj)))


