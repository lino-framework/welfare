# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Fills CBSS demo settings to SiteConfig
"""

from django.conf import settings
from lino.api import dd, rt


def objects():

    Sector = rt.models.cbss.Sector
    sc = settings.SITE.site_config
    sc.sector = Sector.objects.get(code=17, subcode=1)
    sc.cbss_org_unit = '0123456789'
    sc.ssdn_email = 'info@example.com'
    sc.ssdn_user_id = '00901234567'
    sc.cbss_http_username = 'E0123456789'
    sc.cbss_http_password = 'p1234567890123456789012345678'
    yield sc
