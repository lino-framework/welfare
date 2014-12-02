# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds PCSW-specific demo data.
"""

from __future__ import unicode_literals

import datetime

from django.conf import settings

from lino import dd, rt
from lino.utils import Cycler

aids = dd.resolve_app('aids')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
pcsw = dd.resolve_app('pcsw')
cv = dd.resolve_app('cv')

ONE_DAY = datetime.timedelta(days=1)


def objects():
    
    DSBE = pcsw.CoachingType.objects.get(id=isip.COACHINGTYPE_DSBE)

    # isip (VSE)
    ISIP_DURATIONS = Cycler(312, 480, 312, 480, 30)
    ISIP_CONTRACT_TYPES = Cycler(isip.ContractType.objects.all())

    JOBS = Cycler(jobs.Job.objects.all())

    JOBS_CONTRACT_TYPES = Cycler(jobs.ContractType.objects.all())
    STUDY_TYPES = Cycler(cv.StudyType.objects.all())

    COMPANIES = Cycler(rt.modules.contacts.Company.objects.all()[:5])
    NORMAL_CONTRACT_ENDINGS = Cycler(
        isip.ContractEnding.objects.filter(needs_date_ended=False))
    PREMATURE_CONTRACT_ENDINGS = Cycler(
        isip.ContractEnding.objects.filter(needs_date_ended=True))
    JOBS_CONTRACT_DURATIONS = Cycler(312, 480, 624)

    if dd.is_installed('aids'):
        Granting = rt.modules.aids.Granting
        AidType = rt.modules.aids.AidType
        INTEG_DUTIES = Cycler(AidType.objects.filter(is_integ_duty=True))

    ar = rt.login('alicia')

    def finish_contract(ctr):
        ctr.full_clean()
        ctr.save()
        ctr.after_ui_save(ar)
        ctr.update_reminders(ar)
        return ctr

    # for i, coaching in enumerate(pcsw.Coaching.objects.filter(type=DSBE)):
    #     af = settings.SITE.demo_date(-600 + i * 20)
    #     kw, ctr = make_contract(i, coaching, af)

    qs = pcsw.Client.objects.filter(coachings_by_client__type=DSBE).distinct()
    # dd.logger.info("20141122 generating %d integ contracts", qs.count())
    for i, client in enumerate(qs):
        # af = coaching.start_date or settings.SITE.demo_date(-600 + i * 40)
        # oldest contract started 200 days ago.
        af = settings.SITE.demo_date(-600 + i * 5)

        kw = dict(applies_from=af, client=client)

        qs = client.get_coachings((af, af), type=DSBE)
        if qs.count() > 0:
            coaching = qs[0]
            kw.update(user=coaching.user)
        else:
            kw.update(user=ar.user)
        if i % 2:
            kw.update(
                type=JOBS_CONTRACT_TYPES.pop(),
                duration=JOBS_CONTRACT_DURATIONS.pop(),
                job=JOBS.pop())
            ctr = jobs.Contract(**kw)
        else:
            ct = ISIP_CONTRACT_TYPES.pop()
            if ct.needs_study_type:
                kw.update(study_type=STUDY_TYPES.pop())
            kw.update(
                type=ct,
                applies_until=af + datetime.timedelta(
                    days=ISIP_DURATIONS.pop()))
            ctr = isip.Contract(**kw)
        if af is not None and af > settings.SITE.demo_date(-14):
            # every fifth contract ends prematuredly
            if i % 5 == 0:
                ctr.ending = PREMATURE_CONTRACT_ENDINGS.pop()
                ctr.date_ended = af + datetime.timedelta(days=14)
            else:
                if ctr.applies_until is None or \
                   ctr.applies_until < settings.SITE.demo_date():
                    ctr.ending = NORMAL_CONTRACT_ENDINGS.pop()
        yield finish_contract(ctr)

        # 90% of the clients whose contract ended more than 20 days
        # ago (and who are being coached) will get a second contract
        if True:  # i % 10:
            while ctr.update_cal_until() < settings.SITE.demo_date(100):
                af = ctr.update_cal_until() + ONE_DAY
                qs = client.get_coachings((af, af), type=DSBE)
                if qs.count() == 0:
                    break
                else:
                    coaching = qs[0]
                    kw.update(user=coaching.user)
                    kw.update(applies_from=af)
                    kw.update(applies_until=af+datetime.timedelta(days=365))
                    ctr = ctr.__class__(**kw)
                    yield finish_contract(ctr)

    # additional loop over isip contracts to add related objects
    for i, ctr in enumerate(isip.Contract.objects.all()):
        # create contract partners for some contracts
        if i % 3:
            yield isip.ContractPartner(
                contract=ctr, company=COMPANIES.pop())
            if i % 4:
                yield isip.ContractPartner(
                    contract=ctr, company=COMPANIES.pop())

        if dd.is_installed('aids'):
            # create an income Granting for each isip contract:
            kw = dict(start_date=ctr.applies_from,
                      aid_type=INTEG_DUTIES.pop())
            kw.update(client=ctr.client)
            g = Granting(**kw)
            g.after_ui_create(None)
            yield g
        
