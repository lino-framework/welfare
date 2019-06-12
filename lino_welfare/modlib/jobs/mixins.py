# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Model mixins for `lino_welfare.modlib.jobs`.

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)
import datetime
ONE_DAY = datetime.timedelta(days=1)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino_xl.lib.cal.choicelists import DurationUnits
from lino_welfare.modlib.isip.mixins import (ContractPartnerBase,
                                             ContractBase)


class JobSupplyment(ContractPartnerBase, ContractBase):
    """Base class for :class:`Contract` and
    :class:`lino_welfare.modlib.art61.models.Contract`.

    .. attribute:: duration

    The duration of this job supplyment (number of working days).

    """

    class Meta:
        abstract = True

    duration = models.IntegerField(
        _("duration (days)"), blank=True, null=True, default=None)
    reference_person = models.CharField(
        _("reference person"), max_length=200, blank=True)
    responsibilities = dd.RichTextField(
        _("responsibilities"), blank=True, null=True, format='html')
    remark = models.TextField(_("Remark"), blank=True)

    @dd.chooser()
    def ending_choices(cls):
        return rt.models.isip.ContractEnding.objects.filter(use_in_jobs=True)

    def full_clean(self, *args, **kw):
        if self.client_id is not None:
            if self.applies_from:
                if self.client.birth_date:
                    def duration(refdate):
                        if type(refdate) != datetime.date:
                            raise Exception("%r is not a date!" % refdate)
                        delta = refdate - self.client.birth_date.as_date()
                        age = delta.days / 365
                        if age < 36:
                            return 312
                        elif age < 50:
                            return 468
                        else:
                            return 624

                    if self.duration is None:
                        if self.applies_until:
                            self.duration = duration(self.applies_until)
                        else:
                            self.duration = duration(self.applies_from)
                            self.applies_until = self.applies_from + \
                                datetime.timedelta(days=self.duration)

                if self.duration and not self.applies_until:
                    # [NOTE1]
                    self.applies_until = DurationUnits.months.add_duration(
                        self.applies_from, int(self.duration/26)) - ONE_DAY

        super(JobSupplyment, self).full_clean(*args, **kw)

JobSupplyment.set_widget_options('duration', width=10)
