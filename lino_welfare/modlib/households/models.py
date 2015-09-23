# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
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
This module extends :mod:`lino.modlib.households.models`
"""

from __future__ import unicode_literals

import datetime
from decimal import Decimal

from lino.modlib.households.models import *

from lino.modlib.households.choicelists import child_roles, parent_roles

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

# There is a Partner model imported from lino.modlib.households, but
# we override it because we want to inherit also from lino_welfare's
# Partner
from lino_welfare.modlib.contacts.models import Partner


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

    def disable_delete(self, ar=None):
        # skip the is_imported_partner test
        return super(Partner, self).disable_delete(ar)

    def after_ui_create(self, ar):
        super(Household, self).after_ui_create(ar)
        self.populate_members.run_from_code(ar)


class Member(Member, mixins.Human, mixins.Born):

    dependency = MemberDependencies.field(default=MemberDependencies.none)

    def full_clean(self):
        """Copy data fields from child"""
        if self.person_id:
            for k in person_fields:
                setattr(self, k, getattr(self.person, k))
        elif not settings.SITE.loading_from_dump:
            # create Person row if all fields are filled
            has_all_fields = True
            kw = dict()
            for k in person_fields:
                if getattr(self, k):
                    kw[k] = getattr(self, k)
                else:
                    has_all_fields = False
            if has_all_fields:
                M = rt.modules.pcsw.Client
                try:
                    obj = M.objects.get(**kw)
                except M.DoesNotExist:
                    obj = M(**kw)
                    obj.full_clean()
                    obj.save()
                self.person = obj
    
        super(Member, self).full_clean()

        if not settings.SITE.loading_from_dump:
            # Auto-create human links between this member and other
            # household members.
            if self.person_id and self.role and self.household_id:
                if dd.is_installed('humanlinks'):
                    Link = rt.modules.humanlinks.Link
                    if self.role in child_roles:
                        for pm in Member.objects.filter(
                                household=self.household,
                                role__in=parent_roles):
                            Link.check_autocreate(pm.person, self.person)
                    elif self.role in parent_roles:
                        for cm in Member.objects.filter(
                                household=self.household,
                                role__in=child_roles):
                            Link.check_autocreate(self.person, cm.person)

    def disabled_fields(self, ar):
        rv = super(Member, self).disabled_fields(ar)
        if self.person_id:
            rv = rv | person_fields
        #~ logger.info("20130808 pcsw %s", rv)
        return rv

dd.update_field(Member, 'person', null=True, blank=True)

person_fields = dd.fields_list(
    Member, 'first_name last_name gender birth_date')


class HouseholdDetail(dd.FormLayout):

    # window_size = (90, 20)

    main = """
    type prefix name id
    # overview box3 box4
    # bottom_box
    households.MembersByHousehold
    """

    box3 = """
    phone
    gsm
    language
    # email
    # url
    """

    box4 = """
    # activity
    sepa.AccountsByPartner
    """

    bottom_box = "remarks households.MembersByHousehold"


class Households(Households):
    detail_layout = HouseholdDetail()


class SiblingsByPerson(SiblingsByPerson):
    column_names = "age:10 role dependency person \
    first_name last_name birth_date gender *"
    order_by = ['birth_date']

MembersByHousehold.column_names = SiblingsByPerson.column_names
MembersByHousehold.order_by = SiblingsByPerson.order_by
MembersByHousehold.auto_fit_column_widths = True


class RefundsByPerson(SiblingsByPerson):
    column_names = "age:10 gender person_info amount"
    child_tariff = Decimal(10)
    adult_tariff = Decimal(20)

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self, obj, ar):
        age = obj.get_age(dd.today())
        if age is None or age <= dd.plugins.households.adult_age:
            return self.child_tariff
        return self.adult_tariff

    @dd.displayfield(_("Person"))
    def person_info(self, obj, ar):
        elems = [obj.get_full_name(salutation=False)]
        # elems += [obj.first_name]
        # if obj.person_id:
        #     elems += obj.person.get_name_elems(ar)
        return E.p(*elems)

    @classmethod
    def get_adults_and_children(cls, person, today):
        """Return a tuble with two integers: number of adults and number of
        children in the primary household of the given person on the
        given date `today`.

        Used by
        :class:`lino_welfare.modlib.aids.models.Confirmations`.

        """
        children = adults = 0
        for obj in cls.request(master_instance=person):
            age = obj.get_age(today)
            if age is None or age <= dd.plugins.households.adult_age:
                children += 1
            else:
                adults += 1
        return (adults, children)


class PopulateMembers(dd.Action):
    # populate household members from data in humanlinks
    # show_in_bbar = False
    custom_handler = True
    label = _("Populate")
    icon_name = 'lightning'

    def run_from_ui(self, ar, **kw):
        if not dd.is_installed('humanlinks'):
            return
        today = dd.today()
        n = 0
        for hh in ar.selected_rows:
            known_children = set()
            for mbr in hh.member_set.filter(role__in=child_roles):
                if mbr.person:
                    known_children.add(mbr.person.id)

            new_children = dict()
            for parent in hh.member_set.filter(role__in=parent_roles):
                for childlnk in parent.person.humanlinks_children.all():
                    child = childlnk.child
                    if not child.id in known_children:
                        age = child.get_age(today)
                        if age is None or age <= dd.plugins.households.adult_age:
                            childmbr = new_children.get(child.id, None)
                            if childmbr is None:
                                cr = MemberRoles.child
                                # if parent.role == MemberRoles.head:
                                #     cr = MemberRoles.child_of_head
                                # else:
                                #     cr = MemberRoles.child_of_partner
                                childmbr = Member(
                                    household=hh,
                                    person=child,
                                    dependency=MemberDependencies.full,
                                    role=cr)
                                new_children[child.id] = childmbr
                                n += 1
                            else:
                                childmbr.role = MemberRoles.child
                            # if parent.role == MemberRoles.head:
                            #     childmbr.dependency = MemberDependencies.full
                            childmbr.full_clean()
                            childmbr.save()

        ar.success(
            _("Added %d children.") % n, refresh_all=True)


dd.inject_action(
    'households.Household',
    populate_members=PopulateMembers())


def get_household_summary(person, today=None, adult_age=None):
    """
    Note that members without `birth_date` are considered as children.
    """
    if adult_age is None:
        adult_age = dd.plugins.households.adult_age
    ar = SiblingsByPerson.request(master_instance=person)
    if ar.get_total_count() == 0:
        return ar.no_data_text
    if today is None:
        today = dd.today()
    adults = children = 0
    for m in ar:
        if m.birth_date is not None and (
                m.birth_date.get_age(today) >= adult_age):
            adults += 1
        else:
            children += 1
    l = []
    if adults:
        l.append(
            ungettext(
                "%(count)d adult", "%(count)d adults", adults) % dict(
                count=adults))
    if children:
        l.append(
            ungettext(
                "%(count)d child", "%(count)d children", children) % dict(
                count=children))
    return _(" and ").join(l)



