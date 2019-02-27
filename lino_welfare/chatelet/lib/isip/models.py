# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import print_function
from __future__ import unicode_literals

from lino.api import dd, _

from lino_welfare.modlib.isip.models import *


class unused_ContractDetail(dd.DetailLayout):
    main = "general duties evaluations PartnersByContract"

    general = dd.Panel("""
    id:8 client:25 type user:15 user_asd:15
    study_type applies_from applies_until exam_policy language:8
    date_decided date_issued printed date_ended ending:20
    uploads.UploadsByController cal.TasksByController
    """, label=_("General"))

    # partners = dd.Panel("""
    # PartnersByContract
    # """, label=_("Contract partners"))

    evaluations = dd.Panel("""
    cal.EntriesByController
    """, label=_("Evaluations"))

    duties = dd.Panel("""
    stages  goals
    duties_asd  duties_dsbe  duties_person
    """, label=_("Duties"))

    #~ def setup_handle(self,dh):
        #~ dh.general.label = _("General")
        #~ dh.isip.label = _("ISIP")

class ContractDetail(dd.DetailLayout):
    main = "general #duties evaluations PartnersByContract"

    general = dd.Panel("""
    id:8 client:25 type user:15 user_asd:15
    study_type applies_from applies_until exam_policy language:8
    date_decided date_issued printed date_ended ending:20
    uploads.UploadsByController cal.TasksByController
    """, label=_("General"))

    # partners = dd.Panel("""
    # PartnersByContract
    # """, label=_("Contract partners"))

    evaluations = dd.Panel("""
    cal.EntriesByController
    """, label=_("Evaluations"))

    # duties = dd.Panel("""
    # stages  goals
    # duties_asd  duties_dsbe  duties_person
    # """, label=_("Duties"))


Contracts.detail_layout = ContractDetail()
# Contracts.detail_layout = None
ContractsByClient.column_names = "applies_from applies_until type user #study_type date_ended ending uploads.UploadsByController *"


