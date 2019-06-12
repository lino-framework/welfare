# -*- coding: UTF-8 -*-
# Copyright 2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Desktop UI for this plugin.

"""

from lino.modlib.users.desktop import *

from lino.api import dd, _

from lino_xl.lib.cal.ui import UserDetailMixin

class UserDetail(UserDetail, UserDetailMixin):
    """Layout of User Detail in Lino Welfare."""

    main = "general cal coaching dashboard.WidgetsByUser"

    general = dd.Panel("""
    box1:40 #MembershipsByUser:20 AuthoritiesGiven:20
    remarks:40 AuthoritiesTaken:20
    """, label=_("General"))

    box1 = """
    username user_type:20 partner
    first_name last_name initials
    email language mail_mode
    id created modified
    """

    coaching_a = """
    newcomer_quota
    coaching_type
    coaching_supervisor
    newcomer_consultations
    newcomer_appointments
    newcomers.CompetencesByUser
    """

    coaching = dd.Panel("""
    coaching_a:20 coachings.CoachingsByUser:40
    """, label=_("Coaching"))


Users.detail_layout = UserDetail()
