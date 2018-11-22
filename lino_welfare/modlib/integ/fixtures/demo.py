# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Rumma & Ko Ltd
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
Adds PCSW-specific demo data.
"""

from __future__ import unicode_literals

import datetime

from django.conf import settings

from lino.api import dd, rt
from lino.utils import Cycler

aids = dd.resolve_app('aids')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
art61 = dd.resolve_app('art61')
immersion = dd.resolve_app('immersion')
pcsw = dd.resolve_app('pcsw')
cv = dd.resolve_app('cv')

ONE_DAY = datetime.timedelta(days=1)


def objects():
    
    DSBE = rt.models.coachings.CoachingType.objects.get(
        id=isip.COACHINGTYPE_DSBE)

    # isip (VSE)
    ISIP_DURATIONS = Cycler(312, 480, 312, 480, 30)

    JOBS = Cycler(jobs.Job.objects.all())

    STUDY_TYPES = Cycler(cv.StudyType.objects.all())

    COMPANIES = Cycler(rt.models.contacts.Company.objects.all()[:5])
    NORMAL_CONTRACT_ENDINGS = Cycler(
        isip.ContractEnding.objects.filter(needs_date_ended=False))
    PREMATURE_CONTRACT_ENDINGS = Cycler(
        isip.ContractEnding.objects.filter(needs_date_ended=True))
    JOBS_CONTRACT_DURATIONS = Cycler(312, 480, 624)

    if dd.is_installed('aids'):
        Granting = rt.models.aids.Granting
        AidType = rt.models.aids.AidType
        INTEG_DUTIES = Cycler(AidType.objects.filter(is_integ_duty=True))

    ar = rt.login('alicia')

    def finish_contract(ctr):
        # print 20150711, ctr, ctr.type
        ctr.full_clean()
        ctr.save()
        ctr.after_ui_save(ar, None)
        ctr.update_reminders(ar)
        return ctr

    # for i, coaching in enumerate(pcsw.Coaching.objects.filter(type=DSBE)):
    #     af = settings.SITE.demo_date(-600 + i * 20)
    #     kw, ctr = make_contract(i, coaching, af)

    qs = pcsw.Client.objects.filter(coachings_by_client__type=DSBE).distinct()
    # dd.logger.info("20141122 generating %d integ contracts", qs.count())

    factories = []

    JOBS_CONTRACT_TYPES = Cycler(jobs.ContractType.objects.all())

    def jobs_contract(**kw):
        kw.update(
            type=JOBS_CONTRACT_TYPES.pop(),
            duration=JOBS_CONTRACT_DURATIONS.pop(),
            job=JOBS.pop())
        if not 'type' in kw:
            raise Exception("20150711, %s" % kw)
        return jobs.Contract(**kw)

    ISIP_CONTRACT_TYPES = Cycler(isip.ContractType.objects.all())
    # print "20150711b", isip.ContractType.objects.all()

    def isip_contract(**kw):
        ct = ISIP_CONTRACT_TYPES.pop()
        if ct.needs_study_type:
            kw.update(study_type=STUDY_TYPES.pop())
        kw.update(
            type=ct,
            applies_until=af + datetime.timedelta(
                days=ISIP_DURATIONS.pop()))
        if not 'type' in kw:
            raise Exception("20150711, %s" % kw)
        return isip.Contract(**kw)

    factories.append(isip_contract)
    factories.append(jobs_contract)
    factories.append(isip_contract)
    factories.append(jobs_contract)
    factories.append(isip_contract)

    if dd.is_installed('art61'):
        Subsidizations = art61.Subsidizations
        SUBS_STORIES = Cycler([
            [Subsidizations.activa],
            [Subsidizations.tutorat],
            [Subsidizations.activa, Subsidizations.tutorat],
            [Subsidizations.region]
        ])

        ART61_CONTRACT_TYPES = Cycler(art61.ContractType.objects.all())

        def f(**kw):
            kw.update(
                type=ART61_CONTRACT_TYPES.pop(),
                company=COMPANIES.pop(),
                duration=JOBS_CONTRACT_DURATIONS.pop())
            ss = SUBS_STORIES.pop()
            for sub in ss:
                kw[sub.contract_field_name()] = True
            if not 'type' in kw:
                raise Exception("20150711, %s" % kw)
            return art61.Contract(**kw)
        factories.append(f)

    if dd.is_installed('immersion'):
        IMMERSION_CONTRACT_TYPES = Cycler(
            immersion.ContractType.objects.all())
        GOALS = Cycler(immersion.Goal.objects.all())

        def f(**kw):
            kw.update(
                company=COMPANIES.pop(),
                type=IMMERSION_CONTRACT_TYPES.pop())
            kw.update(
                applies_until=af + datetime.timedelta(
                    days=ISIP_DURATIONS.pop()))
            kw.update(goal=GOALS.pop())
            if not 'type' in kw:
                raise Exception("20150711, %s" % kw)
            return immersion.Contract(**kw)
        factories.append(f)

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

        cf = factories[i % len(factories)]
        ctr = cf(**kw)

        # if i % 2:
        #     ctr = jobs_contract()
        # else:
        #     ctr = isip_contract()

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
                    # ctr = ctr.__class__(**kw)
                    ctr = cf(**kw)
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
            g.after_ui_save(None, None)
            yield g
        
    if dd.is_installed('immersion'):
        # Extra loop on immersion trainings to print one of every type
        ExcerptType = rt.models.excerpts.ExcerptType
        CT = rt.models.immersion.ContractType
        Contract = rt.models.immersion.Contract
        ses = rt.login("alicia")
        for ct in CT.objects.all():
            # There must be at least one contract per type
            ctr = Contract.objects.filter(type=ct)[0]
            et = ExcerptType.get_for_model(Contract)
            ses.selected_rows = [ctr]
            yield et.get_or_create_excerpt(ses)
