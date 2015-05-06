# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for lino_welfare.modlib.cbss`.

"""

from lino.api import dd, _


class RequestStates(dd.Workflow):

    """
    The status of a :class:`CBSSRequest`.
    """
    #~ label = _("State")

add = RequestStates.add_item
#~ add('0',_("New"),'new')
add('10', _("Sent"), 'sent')
# sending failed. no ticket yet. can execute again.
add('20', _("Failed"), 'failed')
add('25', _("Validated"), 'validated')  # only when cbss_live_tests
add('30', _("OK"), 'ok')
add('40', _("Warnings"), 'warnings')  # OK and useable
# there's a ticket, but no usable result. cannot print.
add('50', _("Errors"), 'errors')
#~ add('6',_("Invalid reply"),'invalid')
#~ add('9',_("Fictive"),'fictive')

#~ class Environment(ChoiceList):
    #~ """
    #~ The environment where a :class:`CBSSRequest` is being executed.
    #~ """
    #~ label = _("Environment")
#~ add = Environment.add_item
#~ add('t',_("Test"),'test')
#~ add('a',_("Acceptance"),'acpt')
#~ add('p',_("Production"),'prod')

OK_STATES = (RequestStates.ok, RequestStates.warnings)


