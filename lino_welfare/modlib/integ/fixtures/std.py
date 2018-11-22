# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Rumma & Ko Ltd
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

"""
Demo data for `lino_welfare.modlib.integ`.
"""

from __future__ import unicode_literals

import datetime
ONE_DAY = datetime.timedelta(days=1)

from django.conf import settings

from lino.api import dd, _
from lino.utils.instantiator import Instantiator

from lino_xl.lib.cal.choicelists import DurationUnits, WORKDAYS


def objects():
    """
    Lino Welfare does not use time slots when generating evaluation
    meetings because the exact planning is done by the user. But we
    define a limit of 4 client meetings per day per user.
    """
    event_type = Instantiator('cal.EventType').build
    kw = dict()
    kw.update(dd.str2kw('name', _("Internal meetings with client")))
    kw.update(dd.str2kw('event_label', _("Appointment")))
    kw.update(max_conflicting=4)
    client_calendar = event_type(invite_client=True, **kw)
    yield client_calendar
    settings.SITE.site_config.update(client_calendar=client_calendar)

    kw = dict()
    kw.update(dd.str2kw('name', _("Evaluation")))
    kw.update(max_conflicting=4)
    client_calendar = event_type(invite_client=True, **kw)
    yield client_calendar

    kw = dict()
    for wd in WORKDAYS:
        kw[wd.name] = True
    exam_policy = Instantiator(
        'isip.ExamPolicy', 'every',
        every_unit=DurationUnits.months, **kw).build
    yield exam_policy(
        1, event_type=client_calendar, start_time="9:00",
        **dd.str2kw('name', _("Every month")))
    yield exam_policy(
        2, event_type=client_calendar, start_time="9:00",
        **dd.str2kw('name', _("Every 2 months")))
    yield exam_policy(
        3, event_type=client_calendar,
        **dd.str2kw('name', _("Every 3 months")))
    exam_policy = Instantiator(
        'isip.ExamPolicy', 'every',
        every_unit=DurationUnits.weeks, **kw).build
    yield exam_policy(
        2,
        event_type=client_calendar, start_time="9:00",
        **dd.str2kw('name', _("Every 2 weeks")))
    exam_policy = Instantiator(
        'isip.ExamPolicy', 'every',
        every_unit=DurationUnits.days, **kw).build
    yield exam_policy(
        10, max_events=1,
        event_type=client_calendar, start_time="9:00",
        **dd.str2kw('name', _("Once after 10 days")))

    exam_policy = Instantiator('isip.ExamPolicy').build
    yield exam_policy(**dd.str2kw('name', _("Other")))

