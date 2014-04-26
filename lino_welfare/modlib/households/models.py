# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

"""
This module extends :mod:`lino.modlib.households.models`
"""

from __future__ import unicode_literals

from lino.modlib.households.models import *

from lino_welfare.modlib.contacts.models import Partner
# we want to inherit also from lino_welfare's Partner


class Member(Member, dd.Human, dd.Born):
    def full_clean(self):
        """Copy data fields from child"""
        super(Member, self).full_clean()
        obj = self.person
        if obj is not None:
            for k in ('first_name', 'last_name', 'gender', 'birth_date'):
                setattr(self, k, getattr(obj, k))


class Household(Household):

    def disable_delete(self, ar):
        # skip the is_imported_partner test
        return super(Partner, self).disable_delete(ar)


def site_setup(site):
    site.modules.households.Households.set_detail_layout(box3="""
    country region city zip_code:10
    addr1:40
    street:25 street_no street_box
    addr2:40
    activity
    sepa.AccountsByPartner
    """)
