# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Database models for :mod:`lino_welfare.modlib.users`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.modlib.users.models import *

from lino_welfare.modlib.pcsw.roles import SocialUser
from lino.modlib.office.roles import OfficeUser


class User(User):
    """The `users.User` model used in Lino Welfare.  We add a few fields
    to the standard models (:class:`lino.modlib.users.models.User`).

    """

    # coaching_type = dd.ForeignKey(
    #     'coachings.CoachingType',
    #     blank=True, null=True,
    #     help_text=_(
    #         "The default CoachingType used when "
    #         "creating Coachings."))
    
    # coaching_supervisor = models.BooleanField(
    #     _("Notify me when a coach has been assigned"),
    #     default=False,
    #     help_text="""Wenn ein Neuantrag einem Begleiter zugewiesen \
    #     wurde, wird außer dem Begleiter auch dieser Benutzer \
    #     benachrichtigt.""")

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

        if not self.user_type:
            return

        if not self.user_type.has_required_roles([OfficeUser]):
            return

        if not self.calendar:
            return

        if not settings.SITE.loading_from_dump:
            rt.models.cal.check_subscription(self, self.calendar)

    def check_all_subscriptions(self):

        if not self.user_type.has_required_roles([SocialUser]):
            return

        coaching_profiles = set()
        for p in UserTypes.items():
            if p.has_required_roles([SocialUser]):
                coaching_profiles.add(p)
        for u in User.objects.filter(
                user_type__in=coaching_profiles).exclude(id=self.id):
            rt.models.cal.check_subscription(self, u.calendar)
            rt.models.cal.check_subscription(u, self.calendar)
        # logger.info("20140403 wrote subscriptions for %s", self)


