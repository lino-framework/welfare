# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The `models` module for :mod:`lino_welfare.modlib.users`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino import dd, rt

from lino.modlib.users.models import *

cal = dd.resolve_app('cal')


class User(User):

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

    def save(self, *args, **kwargs):
        """For a user with a office_level, create a default calendar.  If
        that user also has a coaching_level, create a default set of
        subscriptions.

        """
        super(User, self). save(*args, **kwargs)

        if not self.profile:
            return

        if not self.profile.office_level:
            return

        if not self.calendar:
            return

        if not settings.SITE.loading_from_dump:
            cal.check_subscription(self, self.calendar)

    def check_all_subscriptions(self):

        if not self.profile.coaching_level:
            return

        coaching_profiles = set()
        for p in UserProfiles.items():
            if p.coaching_level:
                coaching_profiles.add(p)
        for u in User.objects.filter(
                profile__in=coaching_profiles).exclude(id=self.id):
            cal.check_subscription(self, u.calendar)
            cal.check_subscription(u, self.calendar)
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
