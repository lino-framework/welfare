# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from decimal import Decimal

from lino_xl.lib.households.models import *

from lino_xl.lib.households.choicelists import child_roles, parent_roles

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

# There is a Partner model imported from lino_xl.lib.households, but
# we override it because we want to inherit also from lino_welfare's
# Partner
from lino_welfare.modlib.contacts.models import Partner


class Household(Household):

    def disable_delete(self, ar=None):
        # skip the is_imported_partner test
        return super(Partner, self).disable_delete(ar)



class HouseholdDetail(dd.DetailLayout):

    # window_size = (90, 20)

    main = """
    type prefix name id
    overview:30 box3:30 #box4:45
    # bottom_box
    households.MembersByHousehold
    """

    box3 = """
    language
    email
    phone
    gsm
    # url
    """

    # box4 = """
    # # activity
    # sepa.AccountsByPartner
    # """

    bottom_box = "remarks households.MembersByHousehold"


class Households(Households):
    detail_layout = 'households.HouseholdDetail'
    insert_layout = """
    name
    type
    """


#MembersByHousehold.column_names = SiblingsByPerson.column_names
#MembersByHousehold.order_by = SiblingsByPerson.order_by
#MembersByHousehold.auto_fit_column_widths = True


class RefundsByPerson(SiblingsByPerson):
    column_names = "age:10 gender:10 person_info amount"
    child_tariff = Decimal(10)
    adult_tariff = Decimal(20)
    sum_text_column = 2

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self, obj, ar):
        age = obj.get_age(dd.today())
        if age is None or age < dd.plugins.households.adult_age:
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
            if age is None or age < dd.plugins.households.adult_age:
                children += 1
            else:
                adults += 1
        return (adults, children)



# dd.inject_action(
#     'households.Household',
#     populate_members=PopulateMembers())


def get_household_summary(person, today=None, adult_age=None):
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
                (m.get_age(today) or 0) >= adult_age):
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
