# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

"""
The `models` module for :mod:`lino_welfare.modlib.users`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino import dd

from lino.modlib.users.models import *

cal = dd.resolve_app('cal')


def check_subscription(user, calendar):
    if calendar is None:
        return
    try:
        cal.Subscription.objects.get(user=user, calendar=calendar)
    except cal.Subscription.DoesNotExist:
        sub = cal.Subscription(user=user, calendar=calendar)
        sub.full_clean()
        sub.save()


class User(User):

    def save(self, *args, **kwargs):
        """For a user with a office_level, create a default calendar.  If
        that user also has a coaching_level, create a default set of
        subscription.

        """
        super(User, self). save(*args, **kwargs)

        if not self.profile:
            return

        if not self.profile.office_level:
            return

        if not self.calendar:
            return

        # if not self.calendar:
        #     i = cal.Calendar.objects.all().count()
        #     i = i % len(cal.Calendar.COLOR_CHOICES)
        #     obj = cal.Calendar(
        #         name=unicode(self),
        #         color=cal.Calendar.COLOR_CHOICES[i])
        #     obj.full_clean()
        #     obj.save()
        #     self.calendar = obj
        #     super(User, self). save(*args, **kwargs)

        check_subscription(self, self.calendar)

        if not self.profile.coaching_level:
            return

        coaching_profiles = set()
        for p in dd.UserProfiles.items():
            if p.coaching_level:
                coaching_profiles.add(p)
        for u in User.objects.filter(
                profile__in=coaching_profiles).exclude(id=self.id):
            check_subscription(self, u.calendar)
            check_subscription(u, self.calendar)
        # logger.info("20140403 wrote subscriptions for %s", self)


class UserDetail(UserDetail, cal.UserDetailMixin):

    main = "general cal coaching"

    general = dd.Panel("""
    box1 #MembershipsByUser:20
    remarks:40 AuthoritiesGiven:20
    """, label=_("General"))

    coaching_a = """
    newcomer_quota
    coaching_type
    coaching_supervisor
    newcomers.CompetencesByUser
    """

    coaching = dd.Panel("""
    coaching_a:20 pcsw.CoachingsByUser:40
    """, label=_("Coaching"))


def site_setup(site):
    site.modules.users.Users.set_detail_layout(UserDetail())
