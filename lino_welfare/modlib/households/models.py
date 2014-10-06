# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This module extends :mod:`lino.modlib.households.models`
"""

from __future__ import unicode_literals

import datetime

from lino.modlib.households.models import *

from django.conf import settings
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

    def after_ui_create(self, ar):
        super(Household, self).after_ui_create(ar)
        self.populate_members.run_from_code(ar)


class Member(Member, dd.Human, dd.Born):

    dependency = MemberDependencies.field(default=MemberDependencies.none)

    def full_clean(self):
        """Copy data fields from child"""
        if self.person_id:
            for k in person_fields:
                setattr(self, k, getattr(self.person, k))
        elif not settings.SITE.loading_from_dump:
            # create Client if appropriate
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
            if self.person_id and self.role and self.household_id:
                Link = rt.modules.humanlinks.Link
                if self.role in child_roles:
                    for pm in Member.objects.filter(
                            household=self.household, role__in=parent_roles):
                        Link.check_autocreate(pm.person, self.person)
                elif self.role in parent_roles:
                    for cm in Member.objects.filter(
                            household=self.household, role__in=child_roles):
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


ADULT_AGE = datetime.timedelta(days=18*365)


class PopulateMembers(dd.Action):
    # show_in_bbar = False
    custom_handler = True
    label = _("Populate")
    icon_name = 'lightning'

    def run_from_ui(self, ar, **kw):
        n = 0
        for hh in ar.selected_rows:
            known_children = set()
            for mbr in hh.member_set.filter(role__in=child_roles):
                if mbr.person:
                    known_children.add(mbr.person.id)

            new_children = dict()
            for parent in hh.member_set.filter(role__in=parent_roles):
                for childlnk in parent.person.children.all():
                    child = childlnk.child
                    if not child.id in known_children:
                        age = child.get_age()
                        if age is not None and age <= ADULT_AGE:
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


# class CreateHousehold(CreateHousehold):
#     def run_from_ui(self, ar, **kw):
#         Member = rt.modules.households.Member
#         super(CreateHousehold, self).run_from_ui(ar, **kw)
#         def add_children(p):
#             for child in Link(parent=p, type=LinkTypes.child)
        

dd.inject_action(
    'households.Household',
    populate_members=PopulateMembers())


def get_household_summary(person, today=None, adult_age=18):
    """
    Note that members without `birth_date` are considered as children.
    """
    ar = SiblingsByPerson.request(master_instance=person)
    if ar.get_total_count() == 0:
        return ar.no_data_text
    if today is None:
        today = dd.today()
    adults = children = 0
    for m in ar:
        # if m.dependency == MemberDependencies.none:
        #     adults += 1
        # else:
        #     children += 1
        if m.birth_date and m.birth_date.get_age(today) >= adult_age:
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



