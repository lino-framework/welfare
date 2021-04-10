# -*- coding: UTF-8 -*-
# Copyright 2012-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Fills in a suite of fictive CBSS requests using simulated responses
in order to avoid live requests to the CBSS.


.. rubric:: Files

.. xfile:: garble_tx25.py

    A utility file used to garble the content of real Tx25 responses so
    that they can be used as test samples without disclosing any
    confidential data.



"""

import os
from django.conf import settings
from lino.utils import IncompleteDate
from lino.api import rt
from io import open

def objects():

    cbss = rt.models.cbss

    DEMO_REQUESTS = [
        [cbss.IdentifyPersonRequest,
         dict(last_name="MUSTERMANN", birth_date=IncompleteDate(1938, 6, 1)),
         'demo_ipr_1.xml'],
        [cbss.IdentifyPersonRequest,
         dict(last_name="MUSTERMANN", birth_date=IncompleteDate(1938, 6, 0)),
         'demo_ipr_2.xml'],
        [cbss.IdentifyPersonRequest,
         dict(last_name="MUSTERMANN", birth_date=IncompleteDate(1938, 6, 1)),
         'demo_ipr_3.xml'],
        [cbss.IdentifyPersonRequest,
         dict(last_name="MUSTERMANN", birth_date=IncompleteDate(1968, 3, 7)),
         'demo_ipr_4.xml'],
        [cbss.IdentifyPersonRequest,
         dict(last_name="MUSTERMANN", birth_date=IncompleteDate(1968, 3, 7)),
         'demo_ipr_5.xml'],
        [cbss.ManageAccessRequest, dict(
            national_id='680601 053-29',
            birth_date=IncompleteDate(1968, 6, 1),
            start_date=settings.SITE.demo_date(),
            end_date=settings.SITE.demo_date(15),
            sector=cbss.Sector.objects.get(code=17, subcode=1),
            purpose=cbss.Purpose.objects.get(code=902),
            action=cbss.ManageActions.REGISTER,
            query_register=cbss.QueryRegisters.ALL,
        ), ''],
        [cbss.RetrieveTIGroupsRequest,
         dict(national_id='680601 053-29', history=False,
              language=cbss.RequestLanguages.de),
         'demo_tx25_1.xml'],
        [cbss.RetrieveTIGroupsRequest,
         dict(national_id='680307 001-74', history=True),
         'demo_tx25_2.xml'],
        [cbss.RetrieveTIGroupsRequest,
         dict(national_id='680307 001-74', history=True),
         'demo_tx25_3.xml'],
        [cbss.RetrieveTIGroupsRequest,
         dict(national_id='980526 001-51', history=True),
         'tx25_1107.xml'], # Type not found: 'r:CourtName'
        [cbss.RetrieveTIGroupsRequest,
         dict(national_id='980526 001-51', history=True),
         'tx25_1358.xml'],  # No handler for ParentalAuthorities
        [cbss.RetrieveTIGroupsRequest,
         dict(national_id='980526 001-51', history=True),
         'tx25_1373.xml'],  # DeliveryType206 instance has no attribute 'Place'
    ]

    User = settings.SITE.user_model
    root = User.objects.get(username='hubert')
    Client = rt.models.pcsw.Client
    mustermann = Client.objects.get(pk=116)
    for model, kw, fn in DEMO_REQUESTS:
        kw.update(person=mustermann)
        kw.update(user=root)
        obj = model(**kw)
        if fn:
            fn = os.path.join(os.path.dirname(__file__), fn)
            xml = open(fn).read()
            obj.execute_request(simulate_response=xml)
            #~ print obj.debug_messages
        yield obj
