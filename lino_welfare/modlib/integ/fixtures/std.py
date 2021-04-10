# -*- coding: UTF-8 -*-
# Copyright 2008-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Demo data for `lino_welfare.modlib.integ`.
"""

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
