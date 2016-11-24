# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
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

"""Database models for :mod:`lino_welfare.modlib.users`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino.modlib.users.models import *

from lino_welfare.modlib.pcsw.roles import SocialAgent
from lino.modlib.office.roles import OfficeUser

cal = dd.resolve_app('cal')


class User(User):
    """The `users.User` model used in Lino Welfare.  We add a few fields
    to the standard models (:class:`lino.modlib.users.models.User`).

    """

    coaching_type = dd.ForeignKey(
        'pcsw.CoachingType',
        blank=True, null=True,
        help_text=_(
            "The default CoachingType used when "
            "creating Coachings."))
    coaching_supervisor = models.BooleanField(
        _("Notify me when a coach has been assigned"),
        default=False,
        help_text="""Wenn ein Neuantrag einem Begleiter zugewiesen \
        wurde, wird außer dem Begleiter auch dieser Benutzer \
        benachrichtigt.""")

    newcomer_consultations = models.BooleanField(
        _("Newcomer consultations"),
        default=False,
        help_text=_("Accepts prompt consultations for newcomers."))

    newcomer_appointments = models.BooleanField(
        _("Newcomer appointments"),
        default=False,
        help_text=_("Accepts appointments for newcomers."))

    def save(self, *args, **kwargs):
        """For a user with a office_level, create a default calendar.  If
        that user also has a coaching_level, create a default set of
        subscriptions.

        """
        super(User, self). save(*args, **kwargs)

        if not self.profile:
            return

        if not isinstance(self.profile.role, OfficeUser):
            return

        if not self.calendar:
            return

        if not settings.SITE.loading_from_dump:
            cal.check_subscription(self, self.calendar)

    def check_all_subscriptions(self):

        if not isinstance(self.profile.role, SocialAgent):
            return

        coaching_profiles = set()
        for p in UserTypes.items():
            if isinstance(p.role, SocialAgent):
                coaching_profiles.add(p)
        for u in User.objects.filter(
                profile__in=coaching_profiles).exclude(id=self.id):
            cal.check_subscription(self, u.calendar)
            cal.check_subscription(u, self.calendar)
        # logger.info("20140403 wrote subscriptions for %s", self)


class UserDetail(UserDetail, cal.UserDetailMixin):
    """Layout of User Detail in Lino Welfare."""

    main = "general cal coaching"

    general = dd.Panel("""
    box1 #MembershipsByUser:20
    remarks:40 AuthoritiesGiven:20
    """, label=_("General"))

    box1 = """
    username profile:20 partner
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
    coaching_a:20 pcsw.CoachingsByUser:40
    """, label=_("Coaching"))


def site_setup(site):
    site.modules.users.Users.set_detail_layout(UserDetail())
