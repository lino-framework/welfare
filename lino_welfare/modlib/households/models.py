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

from django.utils.translation import ugettext_lazy as _

from lino_welfare.modlib.contacts.models import Partner
# we want to inherit also from lino_welfare's Partner


class MemberDependencies(dd.ChoiceList):
    """The list of allowed choices for the `charge` of a household member.
    """
    verbose_name = _("Dependency")
    verbose_name_plural = _("Household Member Dependencies")

add = MemberDependencies.add_item
add('01', _("At full charge"), 'full')
add('02', _("Not at charge"), 'none')
add('03', _("At shared charge"), 'shared')


class Household(Household):
   
    def disable_delete(self, ar):
        # skip the is_imported_partner test
        return super(Partner, self).disable_delete(ar)


class Member(Member, dd.Human, dd.Born):

    dependency = MemberDependencies.field(default=MemberDependencies.none)

    def full_clean(self):
        """Copy data fields from child"""
        if self.person_id:
            for k in person_fields:
                setattr(self, k, getattr(self.person, k))
        super(Member, self).full_clean()

    def disabled_fields(self, ar):
        rv = super(Member, self).disabled_fields(ar)
        if self.person_id:
            rv = rv | person_fields
        #~ logger.info("20130808 pcsw %s", rv)
        return rv

dd.update_field(Member, 'person', null=True, blank=True)

# person_fields = ('first_name', 'last_name', 'gender', 'birth_date')
person_fields = dd.fields_list(
    Member, 'first_name last_name gender birth_date')


class unused_HouseholdDetail(HouseholdDetail):

    box3 = """
    phone
    gsm
    email
    url
    """

    box4 = """
    # activity
    sepa.AccountsByPartner
    """


class HouseholdDetail(dd.FormLayout):

    main = """
    type name language:10 id
    box3 box4
    bottom_box
    """

    box3 = """
    phone
    gsm
    email
    url
    """

    box4 = """
    # activity
    sepa.AccountsByPartner
    """

    bottom_box = "remarks households.MembersByHousehold"


class Households(Households):
    detail_layout = HouseholdDetail()


class SiblingsByPerson(SiblingsByPerson):
    column_names = "age role dependency person \
    first_name last_name birth_date gender *"
    order_by = ['birth_date']
    

