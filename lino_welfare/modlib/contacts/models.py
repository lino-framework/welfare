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
The `models` module for :mod:`lino_welfare.modlib.contacts`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino import dd

from lino.modlib.contacts.models import *
from lino_welfare.modlib.contacts import Plugin


class Partner(Partner, mixins.CreatedModified, dd.ImportedFields):

    """
    :ref:`welfare` defines a `vat_id` field on Partner but doesn't
    need :mod:`lino.modlib.vat`

    """

    #~ class Meta(contacts.Partner.Meta):
        #~ app_label = 'contacts'

    is_obsolete = models.BooleanField(
        verbose_name=_("obsolete"), default=False, help_text=u"""\
Altfälle sind Partner, deren Stammdaten nicht mehr gepflegt werden und 
für neue Operationen nicht benutzt werden können.""")

    activity = models.ForeignKey("pcsw.Activity",
                                 blank=True, null=True)

    # bank_account1 = models.CharField(max_length=40,
    #                                  blank=True,  # null=True,
    #                                  verbose_name=_("Bank account 1"))

    # bank_account2 = models.CharField(max_length=40,
    #                                  blank=True,  # null=True,
    #                                  verbose_name=_("Bank account 2"))

    hidden_columns = 'created modified activity'
    # bank_account1 bank_account2'

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
        # not e.g. on JobProvider who has no own site_setup()
        if cls is Partner:
            cls.declare_imported_fields('''
            is_person is_company
            ''')

    def disabled_fields(self, ar):
        rv = super(Partner, self).disabled_fields(ar)
        #~ logger.info("20120731 CpasPartner.disabled_fields()")
        #~ raise Exception("20120731 CpasPartner.disabled_fields()")
        if settings.SITE.is_imported_partner(self):
            rv |= self._imported_fields
        return rv

    def disable_delete(self, ar):
        if ar is not None and settings.SITE.is_imported_partner(self):
            return _("Cannot delete companies and persons imported from TIM")
        return super(Partner, self).disable_delete(ar)

    #~ def get_row_permission(self,ar,state,ba):
        #~ if isinstance(ba.action,dd.MergeAction) and settings.SITE.is_imported_partner(self):
            #~ return False
        #~ return super(Partner,self).get_row_permission(ar,state,ba)

    def __unicode__(self):
        if self.is_obsolete:
            return "%s (%s*)" % (self.get_full_name(), self.pk)
        return "%s (%s)" % (self.get_full_name(), self.pk)


class PartnerDetail(PartnerDetail):
    bottom_box = """
    remarks
    activity is_obsolete
    is_person is_company is_household created modified
    """


#~ class Partners(contacts.Partners):
    #~ """
    #~ Base class for Companies and Persons tables,
    #~ *and* for households.Households.
    #~ """
    #~ detail_layout = PartnerDetail()

#~ class AllPartners(contacts.AllPartners,Partners):
    #~ app_label = 'contacts'

#~ from lino.modlib.families import models as families
#~ class Person(Partner,Person,mixins.Born,families.Child):
class Person(Partner, Person, mixins.Born):

    """
    Represents a physical person.
    
    """

    class Meta(Person.Meta):
        #~ app_label = 'contacts'
        verbose_name = _("Person")  # :doc:`/tickets/14`
        verbose_name_plural = _("Persons")  # :doc:`/tickets/14`
        #~ ordering = ['last_name','first_name']

    is_client = mti.EnableChild('pcsw.Client', verbose_name=_("is Client"),
                                help_text=_("Whether this Person is a Client."))

    def get_queryset(self):
        return self.model.objects.select_related('country', 'city')

    def get_print_language(self):
        "Used by DirectPrintAction"
        return self.language

    @classmethod
    def on_analyze(cls, site):
        super(Person, cls).on_analyze(site)
        cls.declare_imported_fields(
          '''name first_name last_name title birth_date gender is_client
          ''')


dd.update_field(Person, 'first_name', blank=False)
dd.update_field(Person, 'last_name', blank=False)


class PersonDetail(PersonDetail):
    bottom_box = """
    activity is_obsolete
    is_client created modified #father #mother
    remarks contacts.RolesByPerson households.MembersByPerson
    """


class Persons(Persons):
    #~ app_label = 'contacts'
    detail_layout = PersonDetail()

    params_panel_hidden = True
    parameters = dict(
        gender=mixins.Genders.field(blank=True, help_text=u"""\
Nur Personen, deren Feld "Geschlecht" ausgefüllt ist und dem angegebenen Wert entspricht."""),
        also_obsolete=models.BooleanField(
            _("Also obsolete data"),
            default=False, help_text=u"""\
Auch Datensätze anzeigen, die als veraltet markiert sind."""))

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

    client_contact_type = dd.ForeignKey(
        'pcsw.ClientContactType', blank=True, null=True)

    vat_id = models.CharField(_("VAT id"), max_length=200, blank=True)

    @classmethod
    def on_analyze(cls, site):
        #~ if cls.model is None:
            #~ raise Exception("%r.model is None" % cls)
        super(Company, cls).on_analyze(site)
        cls.declare_imported_fields(
            '''name vat_id prefix phone fax email activity''')


class CompanyDetail(CompanyDetail):

    box3 = """
    country region city zip_code:10
    addr1:40
    street:25 street_no street_box
    addr2:40
    """

    box4 = """
    email:40
    url
    phone
    gsm
    """

    address_box = "box3 box4"

    box5 = dd.Panel("""
    remarks
    is_courseprovider is_jobprovider client_contact_type
    """)

    bottom_box = "box5 contacts.RolesByCompany"

    intro_box = """
    prefix name id language
    vat_id:12 activity:20 type:20
    is_obsolete
    """

    general = dd.Panel("""
    intro_box
    address_box
    bottom_box
    """, label=_("General"))

    notes = "notes.NotesByCompany"

    main = "general notes"

# TODO: find a more elegant way to do this.
if not dd.is_installed('courses'):
    CompanyDetail.box5.replace('is_courseprovider', '')


class Companies(Companies):
    detail_layout = CompanyDetail()


def setup_main_menu(self, ui, profile, main):
    m = main.add_menu("contacts", Plugin.verbose_name)
    #~ m.clear()
    m.add_action(Persons)
    m.add_action(self.modules.pcsw.Clients,
                 label=string_concat(u' \u25b6 ', self.modules.pcsw.Clients.label))
    #~ m.add_action(self.modules.pcsw.Clients,'find_by_beid')
    m.add_action(self.modules.contacts.Companies)
    #~ m.add_action(self.modules.households.Households)
    m.add_separator('-')
    m.add_action(self.modules.contacts.Partners, label=_("Partners (all)"))
