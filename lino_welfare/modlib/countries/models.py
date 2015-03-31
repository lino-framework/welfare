# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` module for `lino_welfare.modlib.countries`.

"""

from __future__ import unicode_literals

from lino.modlib.countries.models import *

Places.detail_layout = """
name country inscode zip_code
parent type id
PlacesByPlace
contacts.PartnersByCity cv.StudiesByPlace
"""

Countries.detail_layout = """
isocode name short_code inscode
# nationalities
countries.PlacesByCountry cv.StudiesByCountry
"""

Countries.insert_layout = """
isocode inscode
name
"""
