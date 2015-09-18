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
Database models for :mod:`lino_welfare.modlib.contacts`.

Lino Welfare defines a `vat_id` field on :class:`Company` but
doesn't need :mod:`lino.modlib.vat`

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.modlib.contacts.models import *

from lino.modlib.addresses.mixins import AddressOwner
from lino.modlib.vatless.mixins import PartnerDetailMixin


class Partner(
        Partner,
        AddressOwner, mixins.CreatedModified, dd.ImportedFields):

    """Extends :class:`lino.modlib.contacts.models.Partner` by adding the
    following fields:

    .. attribute:: is_obsolete

        Marking a partner as obsolete means to stop using this partner
        for new operations. Obsolete partners are hidden in most
        views.

    .. attribute:: activity

    .. attribute:: client_contact_type

    """

    is_obsolete = models.BooleanField(
        verbose_name=_("obsolete"), default=False, help_text=u"""\
Altfälle sind Partner, deren Stammdaten nicht mehr gepflegt werden und
für neue Operationen nicht benutzt werden können.""")

    activity = models.ForeignKey("pcsw.Activity",
                                 blank=True, null=True)

    hidden_columns = 'created modified activity'

    client_contact_type = dd.ForeignKey(
        'pcsw.ClientContactType', blank=True, null=True)

    def get_overview_elems(self, ar):
        # In the base classes, Partner must come first because
        # otherwise Django won't inherit `meta.verbose_name`. OTOH we
        # want to get the `get_overview_elems` from AddressOwner, not
        # from Partner (i.e. AddressLocation).
        elems = super(Partner, self).get_overview_elems(ar)
        elems += AddressOwner.get_overview_elems(self, ar)
        return elems

    @classmethod
    def on_analyze(cls, site):
        super(Partner, cls).on_analyze(site)
        cls.declare_imported_fields('''
          created modified
          name remarks region zip_code city country
          street_prefix street street_no street_box
          addr2
          language
          phone fax email url
          activity is_obsolete
          ''')

    def disabled_fields(self, ar):
        rv = super(Partner, self).disabled_fields(ar)
        #~ logger.info("20120731 CpasPartner.disabled_fields()")
        #~ raise Exception("20120731 CpasPartner.disabled_fields()")
        if settings.SITE.is_imported_partner(self):
            rv |= self._imported_fields
        return rv

    def disable_delete(self, ar=None):
        if ar is not None and settings.SITE.is_imported_partner(self):
            return _("Cannot delete companies and persons imported from TIM")
        return super(Partner, self).disable_delete(ar)

    def __unicode__(self):
        # 20150419 : print partner id only for clients because the
        # numbers become annoying when printing a debts.Budget.
        return self.get_full_name(nominative=True)

    # def __unicode__(self):
    #     s = self.get_full_name(nominative=True)
    #     if self.is_obsolete:
    #         return "%s (%s*)" % (s, self.pk)
    #     return "%s (%s)" % (s, self.pk)


class PartnerDetail(PartnerDetail, PartnerDetailMixin):

    main = "general contact ledger misc"

    general = dd.Panel("""
    overview:30 general2:45 general3:20
    reception.AppointmentsByPartner
    """, label=_("General"))

    general2 = """
    id language
    activity
    client_contact_type
    url
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    address_box
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    misc = dd.Panel("""
    is_obsolete created modified
    changes.ChangesByMaster
    """, label=_("Miscellaneous"))


class Person(Partner, Person):
    """Represents a physical person.

    """

    class Meta(Person.Meta):
        verbose_name = _("Person")  # :doc:`/tickets/14`
        verbose_name_plural = _("Persons")  # :doc:`/tickets/14`
        #~ ordering = ['last_name','first_name']

    def get_queryset(self, ar):
        return self.model.objects.select_related('country', 'city')

    def get_print_language(self):
        "Used by DirectPrintAction"
        return self.language

    @classmethod
    def on_analyze(cls, site):
        super(Person, cls).on_analyze(site)
        cls.declare_imported_fields(
            '''name first_name middle_name last_name title
            birth_date gender''')


#dd.update_field(Person, 'first_name', blank=False)
dd.update_field(Person, 'last_name', blank=False)


class PersonDetail(PersonDetail, PartnerDetailMixin):

    main = "general contact ledger misc"

    general = dd.Panel("""
    overview:30 general2:45 general3:30
    contacts.RolesByPerson:20  \
    """, label=_("General"))

    general2 = """
    title first_name:15 middle_name:15
    last_name
    gender:10 birth_date age:10
    id language
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    households.MembersByPerson:20 households.SiblingsByPerson:60
    humanlinks.LinksByHuman
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    misc = dd.Panel("""
    activity url client_contact_type is_obsolete
    created modified
    reception.AppointmentsByPartner
    """, label=_("Miscellaneous"))


class Persons(Persons):

    detail_layout = PersonDetail()

    params_panel_hidden = True
    parameters = dict(
        gender=dd.Genders.field(
            blank=True, help_text=_(
                "Show only persons with the given gender.")),
        also_obsolete=models.BooleanField(
            _("Also obsolete data"),
            default=False, help_text=_("Show also obsolete records.")))

    params_layout = """
    gender also_obsolete
    """

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Persons, self).get_request_queryset(ar)
        if not ar.param_values.also_obsolete:
            qs = qs.filter(is_obsolete=False)
        if ar.param_values.gender:
            qs = qs.filter(gender__exact=ar.param_values.gender)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Persons, self).get_title_tags(ar):
            yield t
        if ar.param_values.gender:
            yield unicode(ar.param_values.gender)
        if ar.param_values.also_obsolete:
            yield unicode(self.parameters['also_obsolete'].verbose_name)


class Company(Partner, Company):

    class Meta:
        verbose_name = _("Organisation")
        verbose_name_plural = _("Organisations")

    vat_id = models.CharField(_("VAT id"), max_length=200, blank=True)

    @classmethod
    def on_analyze(cls, site):
        #~ if cls.model is None:
            #~ raise Exception("%r.model is None" % cls)
        super(Company, cls).on_analyze(site)
        cls.declare_imported_fields(
            '''name vat_id prefix phone fax email activity''')


class CompanyDetail(CompanyDetail, PartnerDetailMixin):

    main = "general contact notes ledger misc"

    general = dd.Panel("""
    overview:30 general2:45 general3:30
    contacts.RolesByCompany
    """, label=_("General"))

    general2 = """
    prefix:20 name:40
    type vat_id
    client_contact_type
    url
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    #address_box addresses.AddressesByPartner
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    notes = "notes.NotesByCompany"

    misc = dd.Panel("""
    id language activity is_obsolete
    created modified
    reception.AppointmentsByPartner
    """, label=_("Miscellaneous"))


class Companies(Companies):
    detail_layout = CompanyDetail()


class PartnersByClientContactType(Partners):
    master_key = 'client_contact_type'
    column_names = "name address_column phone gsm email *"
    auto_fit_column_widths = True


@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    contacts = sender.modules.contacts
    contacts.Partners.set_detail_layout(contacts.PartnerDetail())
    contacts.Companies.set_detail_layout(contacts.CompanyDetail())


