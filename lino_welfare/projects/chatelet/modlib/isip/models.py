# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino import dd, rt

from lino_welfare.modlib.isip.models import *


class ContractDetail(dd.FormLayout):
    general = dd.Panel("""
    id:8 client:25 type user:15 user_asd:15
    study_type applies_from applies_until exam_policy language:8
    date_decided date_issued printed date_ended ending:20
    stages  goals
    """, label=_("General"))

    # partners = dd.Panel("""
    # PartnersByContract
    # """, label=_("Contract partners"))

    evaluations = dd.Panel("""
    cal.EventsByController
    """, label=_("Evaluations"))

    duties = dd.Panel("""
    duties_asd  duties_dsbe  duties_person
    cal.TasksByController
    """, label=_("Duties"))

    main = "general duties evaluations PartnersByContract"

    #~ def setup_handle(self,dh):
        #~ dh.general.label = _("General")
        #~ dh.isip.label = _("ISIP")


Contracts.detail_layout = ContractDetail()


