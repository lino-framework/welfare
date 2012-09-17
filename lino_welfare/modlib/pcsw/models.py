# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Contains PCSW-specific models and tables that have not yet been 
moved into a separate module because they are really very PCSW specific.

See also :doc:`/pcsw/models`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation


#~ from lino import reports
from lino import dd
#~ from lino import layouts
#~ from lino.core import perms
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
from lino.modlib.cal import models as cal
from lino.modlib.users import models as users
from lino.utils.choicelists import HowWell, Gender
from lino.utils.choicelists import ChoiceList, Choice
from lino.modlib.users.models import UserLevels
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
#~ from lino.models import get_site_config
from lino.core.modeltools import get_field
from lino.core.modeltools import resolve_field
from lino.core.modeltools import range_filter
from lino.utils.babel import DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils.babel import language_choices
#~ from lino.utils.babel import add_babel_field, DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.utils.ranges import isrange

from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.core.modeltools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.cal.models import DurationUnits, update_reminder
from lino.modlib.properties import models as properties
from lino_welfare.modlib.cv import models as cv
#~ from lino.modlib.contacts.models import Contact
from lino.core.modeltools import resolve_model, UnresolvedModel

#~ # not used here, but these modules are required in INSTALLED_APPS, 
#~ # and other code may import them using 
#~ # ``from lino.apps.pcsw.models import Property``

#~ from lino.modlib.properties.models import Property
#~ # from lino.modlib.notes.models import NoteType
#~ from lino.modlib.countries.models import Country, City

#~ if settings.LINO.user_model:
    #~ User = resolve_model(settings.LINO.user_model,strict=True)

households = dd.resolve_app('households')

def is_valid_niss(national_id):
    try:
        niss_validator(national_id)
        return True
    except ValidationError:
        return False
        
def niss_validator(national_id):
    """
    Checks whether the specified `national_id` is a valid 
    Belgian NISS (No. d'identification de sécurité sociale).
    
    Official format is ``YYMMDDx123-97``, where ``YYMMDD`` is the birth date, 
    ``x`` indicates the century (``*`` for the 19th, `` `` (space) for the 20th
    and ``=`` for the 21st century), ``123`` is a sequential number for persons 
    born the same day (odd numbers for men and even numbers for women), 
    and ``97`` is a check digit (remainder of previous digits divided by 97).
    
    """
    national_id = national_id.strip()
    if not national_id:
        return
    if len(national_id) != 13:
        raise ValidationError(
          force_unicode(_('Invalid Belgian SSIN %s : ') % national_id) 
          + force_unicode(_('An SSIN has always 13 positions'))
          ) 
    xtest = national_id[:6] + national_id[7:10]
    if national_id[6] == "=":
        xtest = "2" + xtest
    try:
        xtest = int(xtest)
    except ValueError,e:
        raise ValidationError(
          _('Invalid Belgian SSIN %s : ') % national_id + str(e)
          )
    xtest = abs((xtest-97*(int(xtest/97)))-97)
    if xtest == 0:
        xtest = 97
    found = int(national_id[11:13])
    if xtest != found:
        raise ValidationError(
            force_unicode(_("Invalid Belgian SSIN %s :") % national_id)
            + _("Check digit is %(found)d but should be %(expected)d") % dict(
              expected=xtest, found=found)
            )



#~ CIVIL_STATE_CHOICES = [
  #~ ('1', _("single")   ),
  #~ ('2', _("married")  ),
  #~ ('3', _("divorced") ),
  #~ ('4', _("widowed")  ),
  #~ ('5', _("separated")  ), # Getrennt von Tisch und Bett / 
#~ ]

class CivilState(ChoiceList):
    """
    Civil states, using Belgian codes.
    
    """
    label = _("Civil state")
    
    @classmethod
    def old2new(cls,old):
        if old == '1': return cls.single
        if old == '2': return cls.married
        if old == '3': return cls.divorced
        if old == '4': return cls.widowed
        if old == '5': return cls.separated
        return ''

add = CivilState.add_item
add('10', _("Single"),'single')
add('13', _("Single cohabitating"))
add('18', _("Single with child"))
add('20', _("Married"),'married')
add('21', _("Married (living alone)"))
add('22', _("Married (living with another partner)"))
add('30', _("Widowed"),'widowed')
add('33', _("Widow cohabitating"))
add('40', _("Divorced"),'divorced')
add('50', _("Separated"),'separated')


#~ '10', 'Célibataire', 'Ongehuwd', 'ledig'
#~ '13', 'Célibataire cohab.', NULL, 'ledig mit zus.', 
#~ '18', 'Célibataire avec enf', NULL, 'ledig mit kind', 
#~ '20', 'Marié', 'Gehuwd', 'verheiratet', 
#~ '21', 'Séparé de fait', NULL, 'verheiratet alleine', 
#~ '22', 'Séparé de fait cohab', NULL, 'verheiratet zus.', 
#~ '30', 'Veuf(ve)', NULL, 'Witwe(r)', 
#~ '33', 'Veuf(ve) cohab.', NULL, 'Witwe(r) zus.', 
#~ '40', 'Divorcé', NULL, 'geschieden', 
#~ '50', 'séparé(e) de corps', NULL, 'von Tisch & Bet get.', 








# http://en.wikipedia.org/wiki/European_driving_licence

class ResidenceType(ChoiceList):
    """
    Types of registries for the Belgian residence.
    
    """
    label = _("Residence type")
    
add = ResidenceType.add_item
add('1', _("Registry of citizens"))    # Bevölkerungsregister registre de la population
add('2', _("Registry of foreigners"))  # Fremdenregister        Registre des étrangers      vreemdelingenregister 
add('3', _("Waiting for registry"))    # Warteregister


class BeIdCardType(ChoiceList):
    """
    List of Belgian Identification Card Types.
    
    """
    label = _("eID card type")
    
add = BeIdCardType.add_item
add('1',_("Belgian citizen")) 
# ,de=u"Belgischer Staatsbürger",fr=u"Citoyen belge"),
add('6', _("Kids card (< 12 year)")) 
#,de=u"Kind unter 12 Jahren"),
add('8', _("Habilitation")) 
#,fr=u"Habilitation",nl=u"Machtiging")
add('11', _("Foreigner card A"))
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister - Tijdelijk verblijf",
        #~ fr=u"Certificat d'inscription au registre des étrangers - Séjour temporaire",
        #~ de=u"Ausländerkarte A Bescheinigung der Eintragung im Ausländerregister - Vorübergehender Aufenthalt",
add('12', _("Foreigner card B"))
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister",
        #~ fr=u"Certificat d'inscription au registre des étrangers",
        #~ de=u"Ausländerkarte B (Bescheinigung der Eintragung im Ausländerregister)",
add('13', _("Foreigner card C"))
        #~ nl=u"Identiteitskaart voor vreemdeling",
        #~ fr=u"Carte d'identité d'étranger",
        #~ de=u"C (Personalausweis für Ausländer)",
add('14', _("Foreigner card D"))
        #~ nl=u"EG - langdurig ingezetene",
        #~ fr=u"Résident de longue durée - CE",
        #~ de=u"Daueraufenthalt - EG",
add('15', _("Foreigner card E"))
        #~ nl=u"Verklaring van inschrijving",
        #~ fr=u"Attestation d’enregistrement",
        #~ de=u"Anmeldebescheinigung",
add('16', _("Foreigner card E+"))
add('17', _("Foreigner card F"))
        #~ nl=u"Verblijfskaart van een familielid van een burger van de Unie",
        #~ fr=u"Carte de séjour de membre de la famille d’un citoyen de l’Union",
        #~ de=u"Aufenthaltskarte für Familienangehörige eines Unionsbürgers",
add('18', _("Foreigner card F+"))


#~ class CpasPartner(dd.Model,mixins.DiffingMixin):
class Partner(contacts.Partner,mixins.DiffingMixin,mixins.CreatedModified):
    """
    """
    
    class Meta:
        #~ abstract = True
        app_label = 'contacts'
  
    #~ is_active = models.BooleanField(
        #~ verbose_name=_("is active"),default=True,
        #~ help_text = "Only active Persons may be used when creating new operations.")
    
    #~ newcomer = models.BooleanField(
        #~ verbose_name=_("newcomer"),default=False)
    #~ """Means that there's no responsible user for this partner yet. 
    #~ New partners may not be used when creating new operations."""
    
    is_deprecated = models.BooleanField(
        verbose_name=_("deprecated"),default=False)
    """Means that data of this partner may be obsolete because 
    there were no confirmations recently. 
    Deprecated partners may not be used when creating new operations."""
    
    activity = models.ForeignKey("pcsw.Activity",
        blank=True,null=True)
    "Pointer to :class:`pcsw.Activity`. May be empty."
    
    bank_account1 = models.CharField(max_length=40,
        blank=True,# null=True,
        verbose_name=_("Bank account 1"))
        
    bank_account2 = models.CharField(max_length=40,
        blank=True,# null=True,
        verbose_name=_("Bank account 2"))
        
        
    _imported_fields = set()
    
    @classmethod
    def declare_imported_fields(cls,names):
        cls._imported_fields = cls._imported_fields | set(dd.fields_list(cls,names))
        #~ logger.info('20120801 %s.declare_imported_fields() --> %s' % (
            #~ cls,cls._imported_fields))
        
    @classmethod
    def site_setup(cls,site):
        super(Partner,cls).site_setup(site)
        cls.declare_imported_fields('''
          created modified
          name remarks region zip_code city country 
          street_prefix street street_no street_box 
          addr2
          language 
          phone fax email url
          bank_account1 bank_account2 activity 
          is_deprecated 
          ''')
        if cls is contacts.Partner: # not e.g. on JobProvider who has no own site_setup()
            cls.declare_imported_fields('''
            is_person is_company
              ''')
        
    def disabled_fields(self,ar):
        #~ logger.info("20120731 CpasPartner.disabled_fields()")
        #~ raise Exception("20120731 CpasPartner.disabled_fields()")
        if settings.LINO.is_imported_partner(self):
            return self._imported_fields
        return []
        
    def disable_delete(self,ar):
        if ar is not None and settings.LINO.is_imported_partner(self):
            return _("Cannot delete companies and persons imported from TIM")
        return super(Partner,self).disable_delete(ar)


class Person(Partner,contacts.Person,contacts.Born,Printable):
    """
    Represents a physical person.
    
    """
    
    class Meta(contacts.PersonMixin.Meta):
        app_label = 'contacts'
        verbose_name = _("Person") # :doc:`/tickets/14`
        verbose_name_plural = _("Persons") # :doc:`/tickets/14`
        
    is_client = mti.EnableChild('pcsw.Client',verbose_name=_("is Client"),
        help_text=_("Whether this Person is a Client."))
        
        
    def get_queryset(self):
        return self.model.objects.select_related('country','city')
        
    def update_owned_instance(self,owned):
        owned.project = self
        super(Person,self).update_owned_instance(owned)

    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return self.language
        
    @classmethod
    def site_setup(cls,site):
        super(Person,cls).site_setup(site)
        cls.declare_imported_fields(
          '''name first_name last_name title birth_date gender is_client
          ''')
        
    
class ClientStates(ChoiceList):
    label = _("Client state")
add = ClientStates.add_item
add('10', _("Newcomer"),'newcomer')       # "N" in PAR->Attrib
add('20', _("Active"),'active')           # neither newcomer nor former, IdPrt != "I"
add('30', _("Official"),'official')       # the client is "integrated"
add('40', _("Former"),'former')           # IdPrt == "I"
add('50', _("Invalid"),'invalid')         # duplicate or doesn't correspond to a real person

    
class Client(Person):
  
    class Meta:
        verbose_name = _("Client") 
        verbose_name_plural = _("Clients") 
        
    workflow_state_field = 'client_state'
        
    remarks2 = models.TextField(_("Remarks (Social Office)"),blank=True) # ,null=True)
    gesdos_id = models.CharField(max_length=40,blank=True,
        #null=True,
        verbose_name=_("Gesdos ID"))
        
    is_cpas = models.BooleanField(verbose_name=_("receives social help"))
    is_senior = models.BooleanField(verbose_name=_("is senior"))
    #~ is_minor = models.BooleanField(verbose_name=_("is minor"))
    group = models.ForeignKey("pcsw.PersonGroup",blank=True,null=True,
        verbose_name=_("Integration phase"))
    #~ is_dsbe = models.BooleanField(verbose_name=_("is coached"),default=False)
    #~ "Indicates whether this Person is coached."
    
    coached_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("Coached from"))
    coached_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
    
    coach1 = dd.ForeignKey(settings.LINO.user_model,
        blank=True,null=True,
        verbose_name=_("Coach 1"),related_name='coached1')
    coach2 = dd.ForeignKey(settings.LINO.user_model,
        blank=True,null=True,
        verbose_name=_("Coach 2"),related_name='coached2')
        
    birth_place = models.CharField(_("Birth place"),
        max_length=200,
        blank=True,
        #null=True
        )
    birth_country = models.ForeignKey("countries.Country",
        blank=True,null=True,
        verbose_name=_("Birth country"),related_name='by_birth_place')
    #~ civil_state = models.CharField(max_length=1,
        #~ blank=True,# null=True,
        #~ verbose_name=_("Civil state"),
        #~ choices=CIVIL_STATE_CHOICES) 
    civil_state = CivilState.field(blank=True) 
    national_id = models.CharField(max_length=200,
        unique=True,
        verbose_name=_("National ID")
        #~ blank=True,verbose_name=_("National ID")
        #~ ,validators=[niss_validator]
        )
        
    health_insurance = dd.ForeignKey(settings.LINO.company_model,blank=True,null=True,
        verbose_name=_("Health insurance"),related_name='health_insurance_for')
    pharmacy = dd.ForeignKey(settings.LINO.company_model,blank=True,null=True,
        verbose_name=_("Pharmacy"),related_name='pharmacy_for')
    
    nationality = dd.ForeignKey('countries.Country',
        blank=True,null=True,
        related_name='by_nationality',
        verbose_name=_("Nationality"))
    #~ tim_nr = models.CharField(max_length=10,blank=True,null=True,unique=True,
        #~ verbose_name=_("TIM ID"))
    card_number = models.CharField(max_length=20,
        blank=True,#null=True,
        verbose_name=_("eID card number"))
    card_valid_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("ID card valid from"))
    card_valid_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
        
    #~ card_type = models.CharField(max_length=20,
        #~ blank=True,# null=True,
        #~ verbose_name=_("eID card type"))
    #~ "The type of the electronic ID card. Imported from TIM."
    
    card_type = BeIdCardType.field(blank=True)
    
    card_issuer = models.CharField(max_length=50,
        blank=True,# null=True,
        verbose_name=_("eID card issuer"))
    "The administration who issued this ID card. Imported from TIM."
    
    #~ eid_panel = dd.FieldSet(_("eID card"),
        #~ "card_number card_valid_from card_valid_until card_issuer card_type:20",
        #~ card_number=_("number"),
        #~ card_valid_from=_("valid from"),
        #~ card_valid_until=_("until"),
        #~ card_issuer=_("issued by"),
        #~ card_type=_("eID card type"),
        #~ )
    
    noble_condition = models.CharField(max_length=50,
        blank=True,#null=True,
        verbose_name=_("noble condition"))
    "The eventual noble condition of this person. Imported from TIM."
        
    
    #~ residence_type = models.SmallIntegerField(blank=True,null=True,
        #~ verbose_name=_("Residence type"),
        #~ choices=RESIDENCE_TYPE_CHOICES,
        #~ max_length=1,
        #~ )
    residence_type = ResidenceType.field(blank=True) 
        
    in_belgium_since = models.DateField(_("Lives in Belgium since"),
        blank=True,null=True)
    unemployed_since = models.DateField(_("Seeking work since"),blank=True,null=True)
    #~ work_permit_exempt = models.BooleanField(verbose_name=_("Work permit exemption"))
    needs_residence_permit = models.BooleanField(verbose_name=_("Needs residence permit"))
    needs_work_permit = models.BooleanField(verbose_name=_("Needs work permit"))
    #~ work_permit_valid_until = models.DateField(blank=True,null=True,verbose_name=_("Work permit valid until"))
    work_permit_suspended_until = models.DateField(blank=True,null=True,verbose_name=_("suspended until"))
    aid_type = models.ForeignKey("pcsw.AidType",blank=True,null=True)
        #~ verbose_name=_("aid type"))
        
    income_ag    = models.BooleanField(verbose_name=_("unemployment benefit")) # Arbeitslosengeld
    income_wg    = models.BooleanField(verbose_name=_("waiting pay")) # Wartegeld
    income_kg    = models.BooleanField(verbose_name=_("sickness benefit")) # Krankengeld
    income_rente = models.BooleanField(verbose_name=_("retirement pension")) # Rente
    income_misc  = models.BooleanField(verbose_name=_("other incomes")) # Andere Einkommen
    
    is_seeking = models.BooleanField(_("is seeking work"))
    unavailable_until = models.DateField(blank=True,null=True,verbose_name=_("Unavailable until"))
    unavailable_why = models.CharField(max_length=100,
        blank=True,# null=True,
        verbose_name=_("reason"))
    
    obstacles = models.TextField(_("Obstacles"),blank=True,null=True)
    skills = models.TextField(_("Other skills"),blank=True,null=True)
    job_agents = models.CharField(max_length=100,
        blank=True,# null=True,
        verbose_name=_("Job agents"))
    
    #~ job_office_contact = models.ForeignKey("contacts.Contact",
    #~ job_office_contact = models.ForeignKey("links.Link",
    job_office_contact = models.ForeignKey("contacts.Role",
      blank=True,null=True,
      verbose_name=_("Contact person at local job office"),
      related_name='persons_job_office')
      
    client_state = ClientStates.field()
    
    print_eid_content = DirectPrintAction(_("eID sheet"),'eid-content')
    




    @classmethod
    def site_setup(cls,site):
        super(Client,cls).site_setup(site)
        cls.declare_imported_fields(
          '''remarks2
          zip_code city country street street_no street_box 
          birth_place coach1 language 
          phone fax email 
          card_type card_number card_valid_from card_valid_until
          noble_condition card_issuer
          national_id health_insurance pharmacy 
          is_cpas is_senior 
          gesdos_id 
          nationality
          ''')

    def get_queryset(self):
        return self.model.objects.select_related(
            'country','city','coach1','coach2','nationality')
        
    
    
    @chooser()
    def job_office_contact_choices(cls):
        sc = settings.LINO.site_config # get_site_config()
        if sc.job_office is not None:
            #~ return sc.job_office.contact_set.all()
            #~ return sc.job_office.rolesbyparent.all()
            return sc.job_office.rolesbycompany.all()
            #~ return links.Link.objects.filter(a=sc.job_office)
        return []
        
    def __unicode__(self):
        #~ return u"%s (%s)" % (self.get_full_name(salutation=False),self.pk)
        return u"%s %s (%s)" % (self.last_name.upper(),self.first_name,self.pk)
        
    def get_active_contract(self):
        """
        Return the one and only active contract on this client.
        If there are more than 1 active contracts, return None.
        """
        v = datetime.date.today()
        q1 = Q(applies_from__isnull=True) | Q(applies_from__lte=v)
        q2 = Q(applies_until__isnull=True) | Q(applies_until__gte=v)
        q3 = Q(date_ended__isnull=True) | Q(date_ended__gte=v)
        flt = Q(q1,q2,q3)
        #~ flt = range_filter(datetime.date.today(),'applies_from','applies_until')
        qs1 = self.isip_contract_set_by_person.filter(flt)
        qs2 = self.jobs_contract_set_by_person.filter(flt)
        if qs1.count() + qs2.count() == 1:
            if qs1.count() == 1: return qs1[0]
            if qs2.count() == 1: return qs2[0]
        
    def full_clean(self,*args,**kw):
        if not isrange(self.coached_from,self.coached_until):
            raise ValidationError(u'Coaching period ends before it started.')
        super(Client,self).full_clean(*args,**kw)
            
    #~ def clean(self):
        #~ if self.job_office_contact: 
            #~ if self.job_office_contact.b == self:
                #~ raise ValidationError(_("Circular reference"))
        #~ super(Person,self).clean()
        
    #~ def card_type_text(self,request):
        #~ if self.card_type:
            #~ s = babeldict_getitem(BEID_CARD_TYPES,self.card_type)
            #~ if s:
                #~ return s
            #~ return _("Unknown card type %r") % self.card_type
        #~ return _("Not specified") # self.card_type
    #~ card_type_text.return_type = dd.DisplayField(_("eID card type"))
        
        
    def save(self,*args,**kw):
        if self.job_office_contact: 
            if self.job_office_contact.person == self:
                raise ValidationError(_("Circular reference"))
        super(Client,self).save(*args,**kw)
        self.update_reminders()
        
    def update_reminders(self):
        """
        Creates or updates automatic tasks controlled directly by this Person.
        """
        user = self.coach2 or self.coach1
        if user:
            def f():
                M = DurationUnits.months
                update_reminder(1,self,user,
                  self.card_valid_until,
                  _("eID card expires in 2 months"),2,M)
                update_reminder(2,self,user,
                  self.unavailable_until,
                  _("becomes available again in 1 month"),1,M)
                update_reminder(3,self,user,
                  self.work_permit_suspended_until,
                  _("work permit suspension ends in 1 month"),1,M)
                update_reminder(4,self,user,
                  self.coached_until,
                  _("coaching ends in 1 month"),1,M)
            babel.run_with_language(user.language,f)
              
          


    @classmethod
    def get_reminders(model,ui,user,today,back_until):
        q = Q(coach1__exact=user) | Q(coach2__exact=user)
        
        def find_them(fieldname,today,delta,msg,**linkkw):
            filterkw = { fieldname+'__lte' : today + delta }
            if back_until is not None:
                filterkw.update({ 
                    fieldname+'__gte' : back_until
                })
            for obj in model.objects.filter(q,**filterkw).order_by(fieldname):
                linkkw.update(fmt='detail')
                url = ui.get_detail_url(obj,**linkkw)
                html = '<a href="%s">%s</a>&nbsp;: %s' % (url,unicode(obj),cgi.escape(msg))
                yield ReminderEntry(getattr(obj,fieldname),html)
            
        #~ delay = 30
        #~ for obj in model.objects.filter(q,
              #~ card_valid_until__lte=date+datetime.timedelta(days=delay)).order_by('card_valid_until'):
            #~ yield ReminderEntry(obj,obj.card_valid_until,_("eID card expires in %d days") % delay,fmt='detail',tab=3)
        for o in find_them('card_valid_until', today, datetime.timedelta(days=30),
            _("eID card expires"),tab=0):
            yield o
        for o in find_them('unavailable_until', today, datetime.timedelta(days=30),
            _("becomes available again"),tab=1):
            yield o
        for o in find_them('work_permit_suspended_until', today, datetime.timedelta(days=30),
              _("work permit suspension ends"),tab=1):
            yield o
        for o in find_them('coached_until', today, datetime.timedelta(days=30),
            _("coaching ends"),tab=1):
            yield o
        
    @dd.displayfield(_("Actions"))
    def read_beid_card(self,ar):
        return '[<a href="javascript:Lino.read_beid_card(%r)">%s</a>]' % (
          str(ar.requesting_panel),unicode(_("Read eID card")))
      
    @dd.virtualfield(dd.HtmlBox())
    def image(self,request):
        url = self.get_image_url(request)
        #~ s = '<img src="%s" width="100%%" onclick="window.open(\'%s\')"/>' % (url,url)
        s = '<img src="%s" width="100%%"/>' % url
        s = '<a href="%s" target="_blank">%s</a>' % (url,s)
        return s
        #~ return '<img src="%s" width="120px"/>' % self.get_image_url()
    #~ image.return_type = dd.HtmlBox()

    def get_image_parts(self):
        if self.card_number:
            return ("beid",self.card_number+".jpg")
        return ("pictures","contacts.Person.jpg")
        
    def get_image_url(self,request):
        #~ return settings.MEDIA_URL + "/".join(self.get_image_parts())
        return request.ui.media_url(*self.get_image_parts())
        
    def get_image_path(self):
        return os.path.join(settings.MEDIA_ROOT,*self.get_image_parts())
        
    def get_skills_set(self):
        return self.personproperty_set.filter(
          group=settings.LINO.site_config.propgroup_skills)
    skills_set = property(get_skills_set)
    
    def properties_list(self,*prop_ids):
        """
        Yields a list of the :class:`PersonProperty <lino_welfare.modlib.cv.models.PersonProperty>` 
        properties of this person in the specified order.
        If this person has no entry for a 
        requested :class:`Property`, it is simply skipped.
        Used in notes/Note/cv.odt"""
        for pk in prop_ids:
            try:
                yield self.personproperty_set.get(property__id=pk)
            except cv.PersonProperty.DoesNotExist,e:
                pass
        
    def unused_get_property(self,prop_id):
        """used in notes/Note/cv.odt"""
        return self.personproperty_set.get(property__id=prop_id)
        #~ return PersonProperty.objects.get(property_id=prop_id,person=self)
        
        
            
    def overview(self,request):
        def qsfmt(qs):
            s = qs.model._meta.verbose_name_plural + ': '
            if qs.count():
                s += ', '.join([unicode(lk) for lk in qs])
            else:
                s += '<b>%s</b>' % force_unicode(_("not filled in"))
            return force_unicode(s)
        
        lines = []
        #~ lines.append('<div>')
        lines.append(qsfmt(self.languageknowledge_set.all()))
        lines.append(qsfmt(self.study_set.all()))
        lines.append(qsfmt(self.contract_set.all()))
        #~ from django.utils.translation import string_concat
        #~ lines.append('</div>')
        return '<br/>'.join(lines)
    overview.return_type = dd.HtmlBox(_("Overview"))
    
    @dd.displayfield(_("Residence permit"))
    def residence_permit(self,rr):
        kv = dict(type=settings.LINO.site_config.residence_permit_upload_type)
        r = rr.spawn(uploads.UploadsByController,
              master_instance=self,
              known_values=kv)
        return rr.renderer.quick_upload_buttons(r)
        #~ rrr = uploads.UploadsByPerson().request(rr.ui,master_instance=self,known_values=kv)
        #~ return rr.ui.quick_upload_buttons(rrr)
    #~ residence_permit.return_type = dd.DisplayField(_("Residence permit"))
    
    @dd.displayfield(_("Work permit"))
    def work_permit(self,rr):
        kv = dict(type=settings.LINO.site_config.work_permit_upload_type)
        r = rr.spawn(uploads.UploadsByController,
              master_instance=self,
              known_values=kv)
        return rr.renderer.quick_upload_buttons(r)
    #~ work_permit.return_type = dd.DisplayField(_("Work permit"))
    
    @dd.displayfield(_("driving licence"))
    #~ @dd.virtualfield(dd.DisplayField(_("driving licence")))
    def driving_licence(self,rr):
        kv = dict(type=settings.LINO.site_config.driving_licence_upload_type)
        r = rr.spawn(uploads.UploadsByController,
              master_instance=self,known_values=kv)
        return rr.renderer.quick_upload_buttons(r)
    #~ driving_licence.return_type = dd.DisplayField(_("driving licence"))
    
    #~ @dd.displayfield(_("CBSS Identify Person"))
    #~ def cbss_identify_person(self,rr):
        #~ r = rr.spawn(
              #~ settings.LINO.modules.cbss.IdentifyRequestsByPerson,
              #~ master_instance=self)
        #~ return rr.renderer.quick_add_buttons(r)

    #~ @dd.displayfield(_("CBSS Retrieve TI Groups"))
    #~ def cbss_retrieve_ti_groups(self,rr):
        #~ r = rr.spawn(
              #~ settings.LINO.modules.cbss.RetrieveTIGroupsRequestsByPerson,
              #~ master_instance=self)
        #~ return rr.renderer.quick_add_buttons(r)


    @dd.virtualfield(models.DateField(_("Contract starts")))
    def applies_from(obj,ar):
        c = obj.get_active_contract()
        if c is not None:
            return c.applies_from
            
    @dd.virtualfield(models.DateField(_("Contract ends")))
    def applies_until(obj,ar):
        c = obj.get_active_contract()
        if c is not None:
            return c.applies_until



class PartnerDetail(contacts.PartnerDetail):
    #~ general = contacts.PartnerDetail.main
    #~ main = "general debts.BudgetsByPartner"
    bottom_box = """
    remarks 
    is_person is_company #is_user is_household created modified
    """
    #~ def setup_handle(self,h):
        #~ h.general.label = _("General")
    

class Partners(contacts.Partners):
    """
    Base class for Companies and Persons tables,
    *and* for households.Households.
    """
    detail_layout = PartnerDetail()
    

class PersonDetail(contacts.PersonDetail):
    bottom_box = """remarks contacts.RolesByPerson
    is_client created modified
    """
  
    

class AllPartners(contacts.AllPartners,Partners):
    app_label = 'contacts'
    #~ pass



class Household(Partner,households.Household):
    """
    for lino_welfare we want to inherit also from Partner
    """
    class Meta(households.Household.Meta):
        app_label = 'households'
        
    #~ @classmethod
    #~ def site_setup(cls,site):
        #~ super(Household,cls).site_setup(site)
        #~ cls.declare_imported_fields('type')
          
    def disable_delete(self,ar):
        # skip the is_imported_partner test
        return super(Partner,self).disable_delete(ar)
        

class Company(Partner,contacts.Company):
  
    
    class Meta(contacts.Company.Meta):
        abstract = False
        app_label = 'contacts'
        
    #~ # to be maintaned with ClientContactTypes
    #~ dd.inject_field(Company,'is_health_insurance',models.BooleanField(verbose_name=_("Health insurance"),default=False))
    #~ dd.inject_field(Company,'is_pharmacy',models.BooleanField(verbose_name=_("Pharmacy"),default=False))
    #~ dd.inject_field(Company,'is_attorney',models.BooleanField(verbose_name=_("Attorney"),default=False))
    #~ dd.inject_field(Company,'is_job_office',models.BooleanField(verbose_name=_("Job office"),default=False))
    
    # to be maintaned with ClientContactTypes
    is_health_insurance = models.BooleanField(verbose_name=_("Health insurance"),default=False)
    is_pharmacy = models.BooleanField(verbose_name=_("Pharmacy"),default=False)
    is_attorney = models.BooleanField(verbose_name=_("Attorney"),default=False)
    is_job_office = models.BooleanField(verbose_name=_("Job office"),default=False)
        
        
        
    @classmethod
    def site_setup(cls,site):
        #~ if cls.model is None:
            #~ raise Exception("%r.model is None" % cls)
        super(Company,cls).site_setup(site)
        cls.declare_imported_fields(
            '''name 
            vat_id prefix
            phone fax email 
            bank_account1 bank_account2 activity''')

    # todo: remove hourly_rate after data migration. this is now in Job
    #~ hourly_rate = dd.PriceField(_("hourly rate"),blank=True,null=True)
    
  
    

class CompanyDetail(dd.FormLayout):
  
    box3 = """
    country region
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    """

    box4 = """
    email:40 
    url
    phone
    gsm
    """

    address_box = "box3 box4"

    box5 = """
    remarks 
    is_courseprovider is_jobprovider is_health_insurance is_pharmacy is_attorney is_job_office
    """

    bottom_box = "box5 contacts.RolesByCompany"

    intro_box = """
    prefix name id language 
    vat_id:12 activity:20 type:20 #hourly_rate
    """

    general = """
    intro_box
    address_box
    bottom_box
    """
    
    notes = "pcsw.NotesByCompany"
    
    main = "general notes"

    def setup_handle(self,lh):
      
        lh.general.label = _("General")
        lh.notes.label = _("Notes")


#~ if settings.LINO.company_model is None:
    #~ raise Exception("settings.LINO.company_model is None")

#~ class Companies(reports.Report):
#~ class Companies(contacts.Contacts):
class Companies(Partners):
    #~ hide_details = [Contact]
    model = settings.LINO.company_model
    detail_layout = CompanyDetail()
        
    order_by = ["name"]
    app_label = 'contacts'
    #~ column_names = ''
    




class ClientDetail(dd.FormLayout):
    
    #~ actor = 'contacts.Person'
    
    main = "general tab2 coaching tab3 tab4 tab5 tab5b history contracts calendar misc "
    
    general = """
    box1 box2
    box4 image:15 #overview 
    """
    
    box1 = """
    last_name first_name:15 title:10
    country city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    """
    
    box2 = """
    id:12 language
    email
    phone fax
    gsm
    """
    
    box3 = """
    gender:10 birth_date age:10 civil_state:15 noble_condition 
    birth_country birth_place nationality:15 national_id:15 
    """
    
    eid_panel = """
    read_beid_card:12 card_number:12 card_valid_from:12 card_valid_until:12 card_issuer:10 card_type:12
    """

    box4 = """
    box3
    eid_panel
    """


    status = """
    in_belgium_since:15 residence_type gesdos_id 
    bank_account1:12 bank_account2:12 
    """
    
      
    income = """
    aid_type   
    income_ag  income_wg    
    income_kg   income_rente  
    income_misc  
    """
      
    suche = """
    is_seeking unemployed_since work_permit_suspended_until
    unavailable_until:15 unavailable_why:30
    # job_office_contact job_agents
    pcsw.ExclusionsByPerson:50x5
    """
    
    coaching = dd.Panel("""
    broker:12 faculty:12
    group:16 client_state
    # coach1:12 coach2:12 coached_from:12 coached_until:12 
    # health_insurance pharmacy job_office_contact 
    job_agents
    ContactsByClient:40 CoachingsByProject:40
    """,label=_("Coaching"))
    
    
    
      
    papers = """
    needs_residence_permit needs_work_permit 
    residence_permit work_permit driving_licence
    uploads.UploadsByController
    """
    
      
    #~ t2left = """
    #~ status:50
    #~ suche:50 
    #~ """
    
    #~ t2right = """
    #~ income:30
    #~ papers:30
    #~ """
    
    #~ tab2 = "t2left t2right"
    
    tab2 = """
    status:55 income:25
    suche:40  papers:40
    """
    
    
    tab3 = """
    jobs.StudiesByPerson 
    jobs.ExperiencesByPerson:40
    """
    
    tab4 = """
    cv.LanguageKnowledgesByPerson 
    courses.CourseRequestsByPerson  
    # skills obstacles
    """
    
    tab5 = """
    cv.SkillsByPerson cv.SoftSkillsByPerson  skills
    cv.ObstaclesByPerson obstacles 
    """

    tab5b = """
    jobs.CandidaturesByPerson
    """
      
    history = """
    pcsw.NotesByPerson #:60 #pcsw.LinksByPerson:20
    outbox.MailsByProject:60 postings.PostingsByProject:40
    """
    
    contracts = """
    isip.ContractsByPerson
    jobs.ContractsByPerson
    """
    
    calendar = """
    cal.EventsByProject
    cal.TasksByProject
    """
    
    misc = """
    activity 
    is_cpas is_senior is_deprecated 
    remarks:30 remarks2:30 contacts.RolesByPerson:30 households.MembersByPerson:30
    # links.LinksToThis:30 links.LinksFromThis:30 
    """
    
    def setup_handle(self,lh):
      
        lh.general.label = _("Person")
        lh.tab2.label = _("Status")
        lh.tab3.label = _("Education")
        lh.tab4.label = _("Languages")
        lh.tab5.label = _("Competences")
        lh.tab5b.label = _("Job Requests")
        lh.history.label = _("History")
        lh.contracts.label = _("Contracts")
        lh.calendar.label = _("Calendar")
        lh.misc.label = _("Miscellaneous")
        #~ lh.cbss.label = _("CBSS")
        
      
        lh.box1.label = _("Address")
        lh.box2.label = _("Contact")
        lh.box3.label = _("Birth")
        lh.eid_panel.label = _("eID card")
        
        lh.papers.label = _("Papers")
        #~ lh.income.label = _("Income")
        lh.suche.label = _("Job search")
        
        # override default field labels
        #~ lh.eid_panel.card_number.label = _("number")
        #~ lh.eid_panel.card_valid_from.label = _("valid from")
        #~ lh.eid_panel.card_valid_until.label = _("valid until")
        #~ lh.eid_panel.card_issuer.label = _("issued by")
        #~ lh.eid_panel.card_type.label = _("eID card type")
        
        lh.card_number.label = _("number")
        lh.card_valid_from.label = _("valid from")
        lh.card_valid_until.label = _("valid until")
        lh.card_issuer.label = _("issued by")
        lh.card_type.label = _("eID card type")

if not settings.LINO.use_beid_jslib:
    ClientDetail.eid_panel = ClientDetail.eid_panel.replace('read_beid_card:12 ')
            

#~ class AllClients(contacts.Persons):
#~ class AllClients(Partners):
    #~ """
    #~ List of all Persons.
    #~ """
    #~ model = Client # settings.LINO.person_model
    #~ detail_layout = ClientDetail()
    #~ insert_layout = dd.FormLayout("""
    #~ title first_name last_name
    #~ gender language
    #~ """,window_size=(60,'auto'))
    
    #~ order_by = "last_name first_name id".split()
    #~ column_names = "name_column:20 national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10"
    
    
    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return string_concat(
          #~ self.model._meta.verbose_name_plural,' ',_("(all)"))
    


def unused_only_coached_persons(qs,*args,**kw):
    return qs.filter(only_coached_persons_filter(*args,**kw))
    

def unused_only_coached_persons_filter(today,
      d1field='coached_from',
      d2field='coached_until'):
    """
    coached_from and coached_until
    """
    # Person with both fields empty is not considered coached:
    q1 = Q(**{d2field+'__isnull':False}) | Q(**{d1field+'__isnull':False})
    return Q(q1,range_filter(today,d1field,d2field))
    
  
def only_coached_by(qs,user):
    #~ return qs.filter(Q(coach1=user) | Q(coach2=user))
    return qs.filter(pcsw_coaching_set_by_project__user=user).distinct()
    
def only_coached_since(qs,since):
    #~ return qs.filter(coached_from__isnull=False,coached_from__gte=ar.param_values.since) 
    return qs.filter(pcsw_coaching_set_by_project__end_date__gte=since) 
            
def only_coached_on(qs,today,join=None):
    """
    Add a filter to the Queryset `qs` (on model Client) 
    which leaves only the clients that are (or were or will be) coached 
    on the specified date.
    """
    #~ return qs.filter(coached_from__isnull=False,coached_from__gte=ar.param_values.since) 
    n = 'pcsw_coaching_set_by_project'
    if join: 
        n = join + '__' + n
    return qs.filter(
        Q(**{n+'__end_date__isnull':False})
          |Q(**{n+'__start_date__isnull':False}),
        Q(**{n+'__end_date__isnull':True})
          |Q(**{n+'__end_date__gte':today}),
        Q(**{n+'__start_date__isnull':True})
          |Q(**{n+'__start_date__lte':today})).distinct()
            
    
#~ from lino.modlib.cal.utils import amonthago

#~ class Clients(AllClients):
class Clients(Partners):
    """
    All Persons except newcomers and inactive persons.
    """
    #~ app_label = 'contacts'
    #~ use_as_default_table = False 
    #~ known_values = dict(is_active=True,newcomer=False)
    #~ known_values = dict(is_deprecated=False)
    #~ known_values = dict(client_state=ClientStates.active)
    #~ filter = dict(is_active=True,newcomer=False)
    #~ label = Person.Meta.verbose_name_plural + ' ' + _("(unfiltered)")
    
    model = Client # settings.LINO.person_model
    detail_layout = ClientDetail()
    insert_layout = dd.FormLayout("""
    title first_name last_name
    gender language
    """,window_size=(60,'auto'))
    
    order_by = "last_name first_name id".split()
    column_names = "name_column:20 client_state national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10"
    
    parameters = dict(
      only_coached_on = models.DateField(_("Only coached on"),blank=True,default=datetime.date.today),
      only_primary = models.BooleanField(_("Only primary clients"),default=False),
      show_deprecated = models.BooleanField(_("Show deprecated"),default=False),
      client_state = ClientStates.field(blank=True),
      group = models.ForeignKey("pcsw.PersonGroup",blank=True,null=True,
          verbose_name=_("Integration phase")),
      coached_by = models.ForeignKey(users.User,blank=True,null=True,
          verbose_name=_("Coached by")),
      coached_since = models.DateField(_("Coached since"),blank=True),
      #~ coached_since = models.DateField(_("Coached since"),blank=True,default=amonthago),
      only_active = models.BooleanField(_("Only active clients"),default=False,
        help_text=_("Show only clients in 'active' integration phases")),
      )
    params_layout = 'coached_by group client_state only_coached_on only_primary show_deprecated'
    
    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return self.model._meta.verbose_name_plural
    
    @classmethod
    def get_request_queryset(self,ar):
        qs = super(Clients,self).get_request_queryset(ar)
        if ar.param_values.coached_since:
            qs = only_coached_since(qs,ar.param_values.coached_since)
        
        if not ar.param_values.show_deprecated:
            qs = qs.filter(is_deprecated=False)
        if ar.param_values.group:
            qs = qs.filter(group=ar.param_values.group)
        if ar.param_values.only_coached_on:
            qs = only_coached_on(qs,ar.param_values.only_coached_on)
        if ar.param_values.only_active:
            qs = qs.filter(group__active=True)
        if ar.param_values.coached_by:
            qs = only_coached_by(qs,ar.param_values.coached_by)
            #~ qs = qs.filter(pcsw_coaching_set_by_project__user=ar.param_values.coached_by)
        if ar.param_values.only_primary:
            #~ qs = qs.filter(pcsw_coaching_set_by_project__primary=True).distinct()
            qs = qs.filter(
              pcsw_coaching_set_by_project__primary=True,
              pcsw_coaching_set_by_project__user=ar.param_values.coached_by)
            #~ qs = qs.filter(
              #~ pcsw_coaching_set_by_project__primary=True,
              #~ pcsw_coaching_set_by_project__user=ar.get_user())
            #~ qs = qs.filter(pcsw_coaching_set_by_project__primary=True)
        if ar.param_values.client_state:
            qs = qs.filter(client_state=ar.param_values.client_state)
        #~ logger.info('20120914 Clients.get_request_queryset --> %d',qs.count())
        return qs

#~ Client._lino_choices_table = Clients

class ClientsByNationality(Clients):
    #~ app_label = 'contacts'
    master_key = 'nationality'
    order_by = "city name".split()
    column_names = "city street street_no street_box addr2 name country language *"



class MyClients(Clients):
    u"""
    Show only Clients attended 
    by the requesting user (or another user, 
    specified via :attr:`lino.ui.requests.URL_PARAMS_SUBST_USER`),
    either as primary or as secondary attendant.
    
    Damit jemand als begleitet gilt, muss mindestens eines der 
    beiden Daten coached_from und coached_until ausgefüllt sein.
    
    """
    required = dict(user_groups = ['integ'])
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    
    #~ app_label = 'contacts'
    use_as_default_table = False
    label = _("My clients")
    #~ order_by = ['last_name','first_name']
    #~ column_names = "name_column:20 coached_from coached_until national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10 *"
    column_names = "name_column:20 client_state applies_from applies_until national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10"
    
    @classmethod
    def get_title(self,rr):
        return _("Clients of %s") % rr.get_user()
        
    @classmethod
    def get_request_queryset(self,ar):
        qs = super(MyClients,self).get_request_queryset(ar)
        u = ar.get_user()
        qs = only_coached_by(qs,u)
        #~ if u is not None and u.username == 'root':
        #~ logger.info('20120914 MyClients.get_request_queryset %s',ar)
        #~ qs = only_coached_on(qs,datetime.date.today())
        #~ print 20111118, 'get_request_queryset', rr.user, qs.count()
        return qs
        #~ today = datetime.date.today()
        #~ Q = models.Q
        #~ q1 = Q(coach1__exact=rr.user) | Q(coach2__exact=rr.user)
        #~ q2 = Q(coached_from__isnull=False) | Q(coached_until__isnull=False,coached_until__gte=today)
        #~ return qs.filter(q1,q2)
        
    #~ @dd.virtualfield(models.DateField(_("Contract starts")))
    #~ def applies_from(self,obj,ar):
        #~ c = obj.get_active_contract()
        #~ if c is not None:
            #~ return c.applies_from
            
    #~ @dd.virtualfield(models.DateField(_("Contract ends")))
    #~ def applies_until(self,obj,ar):
        #~ c = obj.get_active_contract()
        #~ if c is not None:
            #~ return c.applies_until

#~ class MyClientsByGroup(MyClients):
    #~ master_key = 'group'
    
    #~ @classmethod
    #~ def get_title(self,rr):
        #~ return _("%(phase)s clients of %(user)s") % dict(
          #~ phase=rr.master_instance, user=rr.get_user())
    
#~ class MyPrimaryClients(MyClients): # "Komplette Akten"
    #~ label = _("Primary clients by coach")
    
    #~ @classmethod
    #~ def get_title(self,rr):
        #~ return _("Primary clients of %s") % rr.master_instance
        
    #~ @classmethod
    #~ def get_request_queryset(self,ar):
        #~ qs = super(MyPrimaryClients,self).get_request_queryset(ar)
        #~ qs = qs.filter(pcsw_coaching_set_by_project__primary=True).distinct()
        #~ return qs


#~ class MyActiveClients(MyClients):
  
    #~ @classmethod
    #~ def get_title(self,rr):
        #~ return _("Active clients of %s") % rr.get_user()
        
    #~ @classmethod
    #~ def get_request_queryset(self,rr):
        #~ qs = super(MyActiveClients,self).get_request_queryset(rr)
        #~ qs = qs.filter(group__active=True)
        #~ return qs
  

#~ if True: # dd.is_installed('pcsw'):

#~ from lino.core.modeltools import models_by_abc


  
#~ class InvalidClients(Clients):
class ClientsTest(Clients):
    """
    Table of Clients whose data seems unlogical or inconsistent.
    """
    required = dict(user_level='manager')
    use_as_default_table = False
    #~ required_user_level = UserLevels.manager
    label = _("Data Test Clients")
    parameters = dict(
      #~ user = dd.ForeignKey(settings.LINO.user_model,blank=True,verbose_name=_("Coached by")),
      #~ only_coached_on = models.DateField(_("Only coached on"),blank=True,default=datetime.date.today),
      #~ today = models.DateField(_("only active on"),blank=True,default=datetime.date.today),
      invalid_niss = models.BooleanField(_("Check NISS validity"),default=True),
      overlapping_contracts = models.BooleanField(_("Check for overlapping contracts"),default=True),
      **Clients.parameters
      #~ coached_period = models.BooleanField(_("Check coaching period"),default=True),
      #~ only_my_persons = models.BooleanField(_("Only my persons"),default=True),
    )
    params_template = """invalid_niss overlapping_contracts coached_by"""
    #~ params_panel_hidden = False
    column_names = "name_column error_message national_id id"
    
    @classmethod
    def get_data_rows(self,ar):
        """
        """
        from lino_welfare.modlib.isip.models import OverlappingContractsTest
        #~ qs = Person.objects.all()
        qs = self.get_request_queryset(ar)
        
        #~ if ar.param_values.user:
            #~ qs = only_coached_by(qs,ar.param_values.user)
        
        #~ if ar.param_values.today:
            #~ qs = only_coached_persons(qs,ar.param_values.today)
            
        #~ logger.info("Building ClientsTest data rows...")
        #~ for p in qs.order_by('name'):
        for person in qs:
            messages = []
            if ar.param_values.overlapping_contracts:
                messages += OverlappingContractsTest(person).check_all()
              
            if ar.param_values.invalid_niss:
                try:
                    niss_validator(person.national_id)
                except ValidationError,e:
                    messages += e.messages
          
            if messages:
                #~ person.error_message = ';<br/>'.join([cgi.escape(m) for m in messages])
                person.error_message = ';\n'.join(messages)
                #~ logger.info("%s : %s", p, p.error_message)
                yield person
        logger.info("Building ClientsTest data rows: done")
                
        
    @dd.displayfield(_('Error message'))
    def error_message(self,obj,ar):
        #~ return obj.error_message.replace('\n','<br/>')
        return obj.error_message
        
    
#~ class OverviewClientsByUser(dd.VirtualTable):
class UsersWithClients(dd.VirtualTable):
    """
    New implementation of persons_by_user
    A customized overview report.
    """
    required = dict(user_groups='integ newcomers')
    #~ label = _("Overview Clients By User")
    label = _("Users with their Clients")
    #~ column_defaults = dict(width=8)
    
    slave_grid_format = 'html'    
    
    @classmethod
    def setup_columns(self):
        """
        Builds columns dynamically from the :class:`PersonGroup` database table.
        Called when kernel setup is done, 
        before the UI handle is being instantiated.
        """
        self.column_names = 'user:10'
        try:
            for pg in PersonGroup.objects.filter(ref_name__isnull=False).order_by('ref_name'):
                def w(pg):
                    def func(self,obj,ar):
                        #~ return MyClientsByGroup.request(
                          #~ ar.ui,master_instance=pg,subst_user=obj)
                        #~ return MyClients.request(
                          #~ ar.ui,subst_user=obj,param_values=dict(group=pg))
                        return Clients.request(ar.ui,
                            param_values=dict(group=pg,coached_by=obj))
                    return func
                vf = dd.RequestField(w(pg),verbose_name=pg.name)
                self.add_virtual_field('G'+pg.ref_name,vf)
                self.column_names += ' ' + vf.name 
        except DatabaseError:
            # happens during `make appdocs`
            pass
            
        self.column_names += ' primary_clients active_clients row_total'
    

    @classmethod
    def get_data_rows(self,ar):
        """
        We only want the users who actually have at least one client.
        We store the corresponding request in the user object 
        under the name `my_persons`.
        
        The list displays only integration agents, i.e. users with a nonempty `integ_level`.
        With one subtility: system admins also have a nonempty `integ_level`, 
        but normal users don't want to see them. 
        So we add the rule that only system admins see other system admins.
        
        """
        profiles = [p for p in dd.UserProfiles.items() if p.integ_level]
        qs = users.User.objects.filter(profile__in=profiles)
        if ar.get_user().profile.level < UserLevels.admin:
            qs = qs.exclude(profile__gte=UserLevels.admin)
        for user in qs.order_by('username'):
            #~ r = MyClients.request(ar.ui,subst_user=user)
            r = Clients.request(ar.ui,param_values=dict(coached_by=user))
            if r.get_total_count():
                user.my_persons = r
                #~ user._detail_action = users.MySettings.default_action
                yield user
                
    @dd.virtualfield('pcsw.Client.coach1')
    #~ @dd.virtualfield(dd.ForeignKey(User))
    def user(self,obj,ar):
        return obj
        
    @dd.requestfield(_("Total"))
    def row_total(self,obj,ar):
        return obj.my_persons
        
    @dd.requestfield(_("Primary clients"))
    def primary_clients(self,obj,ar):
        #~ return MyPrimaryClients.request(ar.ui,subst_user=obj)
        #~ return MyClients.request(ar.ui,subst_user=obj,param_values=dict(only_primary=True))
        return Clients.request(ar.ui,param_values=dict(only_primary=True,coached_by=obj))
        
    @dd.requestfield(_("Active clients"))
    def active_clients(self,obj,ar):
        #~ return MyActiveClients.request(ar.ui,subst_user=obj)
        return Clients.request(ar.ui,param_values=dict(only_active=True,coached_by=obj))


#
# PERSON GROUP
#
class PersonGroup(dd.Model):
    """Integration Phase (previously "Person Group")
    """
    name = models.CharField(_("Designation"),max_length=200)
    ref_name = models.CharField(_("Reference name"),max_length=20,blank=True)
    active = models.BooleanField(_("Considered active"),default=True)
    #~ text = models.TextField(_("Description"),blank=True,null=True)
    class Meta:
        verbose_name = _("Integration Phase")
        verbose_name_plural = _("Integration Phases")
    def __unicode__(self):
        return self.name

class PersonGroups(dd.Table):
    """List of Integration Phases"""
    model = PersonGroup
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    required = dict(user_level='manager',user_groups='integ')

    order_by = ["ref_name"]

    
    
    

#
# ACTIVITIY (Berufscode)
#
class Activity(dd.Model):
    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
    name = models.CharField(max_length=80)
    lst104 = models.BooleanField(_("Appears in Listing 104"))
    
    def __unicode__(self):
        return unicode(self.name)

class Activities(dd.Table):
    model = Activity
    #~ required_user_level = UserLevels.manager
    required = dict(user_level='manager')
    #~ label = _('Activities')

#~ class ActivitiesByPerson(Activities):
    #~ master_key = 'activity'

#~ class ActivitiesByCompany(Activities):
    #~ master_key = 'activity'
    
#
# EXCLUSION TYPES (Sperrgründe)
#
class ExclusionType(dd.Model):
    class Meta:
        verbose_name = _("exclusion type")
        verbose_name_plural = _('exclusion types')
        
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)

class ExclusionTypes(dd.Table):
    #~ required_user_groups = ['integ']
    required = dict(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = ExclusionType
    #~ label = _('Exclusion Types')
    
#
# EXCLUSIONS (Arbeitslosengeld-Sperrungen)
#
class Exclusion(dd.Model):
    class Meta:
        verbose_name = _("exclusion")
        verbose_name_plural = _('exclusions')
        
    #~ person = models.ForeignKey("contacts.Person")
    #~ person = models.ForeignKey(settings.LINO.person_model)
    person = models.ForeignKey('pcsw.Client')
    type = models.ForeignKey("pcsw.ExclusionType",verbose_name=_("Reason"))
    excluded_from = models.DateField(blank=True,null=True,verbose_name=_("from"))
    excluded_until = models.DateField(blank=True,null=True,verbose_name=_("until"))
    remark = models.CharField(max_length=200,blank=True,verbose_name=_("Remark"))
    
    def __unicode__(self):
        s = unicode(self.type)
        if self.excluded_from: s += ' ' +unicode(self.excluded_from)
        if self.excluded_until: s += '-'+unicode(self.excluded_until)
        return s

class Exclusions(dd.Table):
    required = dict(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = Exclusion
    #~ label = _('Exclusions')
    
class ExclusionsByPerson(Exclusions):
    required = dict(user_groups='integ')
    #~ required_user_level = None
    master_key = 'person'
    column_names = 'excluded_from excluded_until type remark'



#
# AID TYPES
#
class AidType(babel.BabelNamed):
    class Meta:
        verbose_name = _("aid type")
        verbose_name_plural = _('aid types')

class AidTypes(dd.Table):
    model = AidType
    column_names = 'name *'
    #~ required_user_level = UserLevels.manager
    required = dict(user_level='manager')





#
# SEARCH
#
class PersonSearch(mixins.AutoUser,mixins.Printable):
    """
    Lino creates a new record in this table for each search request.
    """
    class Meta:
        verbose_name = _("Person Search")
        verbose_name_plural = _('Person Searches')
        
    title = models.CharField(max_length=200,
        verbose_name=_("Search Title"))
    aged_from = models.IntegerField(_("Aged from"),
        blank=True,null=True)
    aged_to = models.IntegerField(_("Aged to"),
        blank=True,null=True)
    #~ gender = contacts.GenderField()
    gender = Gender.field(blank=True)

    
    only_my_persons = models.BooleanField(_("Only my clients")) # ,default=True)
    
    coached_by = dd.ForeignKey(settings.LINO.user_model,
        verbose_name=_("Coached by"),
        related_name='persons_coached',
        blank=True,null=True)
    period_from = models.DateField(
        blank=True,null=True,
        verbose_name=_("Period from"))
    period_until = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
    
    def result(self):
        for p in ClientsBySearch().request(master_instance=self):
            yield p
        
    def __unicode__(self):
        return self._meta.verbose_name + ' "%s"' % (self.title or _("Unnamed"))
        
    #~ def get_print_language(self,pm):
        #~ return DEFAULT_LANGUAGE

    print_suchliste = DirectPrintAction(_("Print"),'suchliste')
    
    #~ @classmethod
    #~ def setup_report(model,rpt):
        # rpt.add_action(DirectPrintAction(rpt,'suchliste',_("Print"),'suchliste'))
        #~ rpt.add_action(DirectPrintAction('suchliste',_("Print"),'suchliste'))
        
class PersonSearches(dd.Table):
    required = dict(user_groups='integ')
    model = PersonSearch
    detail_template = """
    id:8 title 
    only_my_persons coached_by period_from period_until aged_from:10 aged_to:10 gender:10
    pcsw.LanguageKnowledgesBySearch pcsw.WantedPropsBySearch pcsw.UnwantedPropsBySearch
    pcsw.ClientsBySearch
    """
    
class MyPersonSearches(PersonSearches,mixins.ByUser):
    #~ model = PersonSearch
    pass
    
class WantedLanguageKnowledge(dd.Model):
    search = models.ForeignKey(PersonSearch)
    language = models.ForeignKey("countries.Language",verbose_name=_("Language"))
    spoken = HowWell.field(blank=True,verbose_name=_("spoken"))
    written = HowWell.field(blank=True,verbose_name=_("written"))

class WantedSkill(properties.PropertyOccurence):
    class Meta:
        app_label = 'properties'
        verbose_name = _("Wanted property")
        verbose_name_plural = _("Wanted properties")
        
    search = models.ForeignKey(PersonSearch)
    
class UnwantedSkill(properties.PropertyOccurence):
    class Meta:
        app_label = 'properties'
        verbose_name = _("Unwanted property")
        verbose_name_plural = _("Unwanted properties")
    search = models.ForeignKey(PersonSearch)
    
    
class LanguageKnowledgesBySearch(dd.Table):
    required = dict(user_groups='integ')
    label = _("Wanted language knowledges")
    master_key = 'search'
    model = WantedLanguageKnowledge

class WantedPropsBySearch(dd.Table):
    required = dict(user_groups = 'integ')
    label = _("Wanted properties")
    master_key = 'search'
    model = WantedSkill

class UnwantedPropsBySearch(dd.Table):
    required = dict(user_groups = 'integ')
    label = _("Unwanted properties")
    master_key = 'search'
    model = UnwantedSkill

#~ class ClientsBySearch(dd.Table):
class ClientsBySearch(Clients):
    """
    This is the slave report of a PersonSearch that shows the 
    Persons matching the search criteria. 
    
    It is a slave report without 
    :attr:`master_key <lino.dd.Table.master_key>`,
    which is allowed only because it also overrides
    :meth:`get_request_queryset`
    """
  
    required = dict(user_groups = 'integ')
    #~ model = Person
    master = PersonSearch
    #~ 20110822 app_label = 'pcsw'
    label = _("Found persons")
    
    #~ can_add = perms.never
    #~ can_change = perms.never
    
    @classmethod
    def get_request_queryset(self,rr):
        """
        Here is the code that builds the query. It can be quite complex.
        See :srcref:`/lino/apps/pcsw/models.py` 
        (search this file for "ClientsBySearch").
        """
        search = rr.master_instance
        if search is None:
            return []
        kw = {}
        qs = self.model.objects.order_by('name')
        today = datetime.date.today()
        if search.gender:
            qs = qs.filter(gender__exact=search.gender)
        if search.aged_from:
            #~ q1 = models.Q(birth_date__isnull=True)
            #~ q2 = models.Q(birth_date__gte=today-datetime.timedelta(days=search.aged_from*365))
            #~ qs = qs.filter(q1|q2)
            min_date = today - datetime.timedelta(days=search.aged_from*365)
            qs = qs.filter(birth_date__lte=min_date.strftime("%Y-%m-%d"))
            #~ qs = qs.filter(birth_date__lte=today-datetime.timedelta(days=search.aged_from*365))
        if search.aged_to:
            #~ q1 = models.Q(birth_date__isnull=True)
            #~ q2 = models.Q(birth_date__lte=today-datetime.timedelta(days=search.aged_to*365))
            #~ qs = qs.filter(q1|q2)
            max_date = today - datetime.timedelta(days=search.aged_to*365)
            qs = qs.filter(birth_date__gte=max_date.strftime("%Y-%m-%d"))
            #~ qs = qs.filter(birth_date__gte=today-datetime.timedelta(days=search.aged_to*365))
            
        if search.only_my_persons:
            qs = only_coached_by(qs,search.user)
        
        if search.coached_by:
            qs = only_coached_by(qs,search.coached_by)
            
        if search.period_from:
            qs = only_coached_since(qs,search.period_from)
            
        if search.period_until:
            qs = only_coached_until(qs,search.period_until)
          
        required_id_sets = []
        
        required_lk = [lk for lk in search.wantedlanguageknowledge_set.all()]
        if required_lk:
            # language requirements are OR'ed
            ids = set()
            for rlk in required_lk:
                fkw = dict(language__exact=rlk.language)
                if rlk.spoken is not None:
                    fkw.update(spoken__gte=rlk.spoken)
                if rlk.written is not None:
                    fkw.update(written__gte=rlk.written)
                q = cv.LanguageKnowledge.objects.filter(**fkw)
                ids.update(q.values_list('person__id',flat=True))
            required_id_sets.append(ids)
            
        rprops = [x for x in search.wantedskill_set.all()]
        if rprops: # required properties
            ids = set()
            for rp in rprops:
                fkw = dict(property__exact=rp.property) # filter keywords
                if rp.value:
                    fkw.update(value__gte=rp.value)
                q = cv.PersonProperty.objects.filter(**fkw)
                ids.update(q.values_list('person__id',flat=True))
            required_id_sets.append(ids)
          
            
        if required_id_sets:
            s = set(required_id_sets[0])
            for i in required_id_sets[1:]:
                s.intersection_update(i)
                # keep only elements found in both s and i.
            qs = qs.filter(id__in=s)
              
        return qs




class OverlappingContracts(dd.Table):
    required = dict(user_groups = 'integ')
    model = Person
    use_as_default_table = False
    #~ base_queryset = only_coached_persons(Person.objects.all())
    label = _("Overlapping Contracts")
    #~ def a(self):
        
    
    #~ def get_title(self,rr):
        #~ return _("Primary clients of %s") % rr.master_instance
        
    @classmethod
    def get_request_queryset(self,rr):
        #~ rr.master_instance = rr.get_user()
        qs = super(OverlappingContracts,self).get_request_queryset(rr)
        #~ only_my_persons(qs,rr.get_user())
        #~ qs = only_coached_persons(qs,datetime.date.today())
        qs = only_coached_at(qs,datetime.date.today())
        #~ qs = qs.filter()
        #~ print 20111118, 'get_request_queryset', rr.user, qs.count()
        return qs

class ClientContactType(Choice):
  
    def __init__(self,choicelist,value,text,name,companies_table,**kw):
        #~ self.company_filter_field = company_filter_field
        self.companies_table = companies_table
        super(ClientContactType,self).__init__(choicelist,value,text,name,**kw)
        
    #~ def company_choices(self):
        #~ if self.company_filter_field:
            #~ return self.company_filter_field.request().data_iterator
        #~ return Company.objects.all()
    
class ClientContactTypes(ChoiceList):
    label = _("Client Contact type")
    item_class = ClientContactType
    
class HealthInsurances(Companies):
    label = _("Health insurances")
    known_values = dict(is_health_insurance=True)
class Pharmacies(Companies):
    label = _("Pharmacies")
    known_values = dict(is_pharmacy=True)
class Attorneys(Companies):
    label = _("Attorneys")
    known_values = dict(is_attorney=True)
class JobOffices(Companies):
    label = _("Job offices")
    known_values = dict(is_job_office=True)
    
add = ClientContactTypes.add_item
#~ add('10', _("Health insurance"),'health_insurance','is_health_insurance')
#~ add('20', _("Pharmacy"),        'pharmacy',        'is_pharmacy')
#~ add('30', _("Attorney"),        'attorney',        'is_attorney')
#~ add('40', _("Job office"),      'job_office',      'is_job_office')
add('10', _("Health insurance"),'health_insurance',HealthInsurances)
add('20', _("Pharmacy"),        'pharmacy',        Pharmacies)
add('30', _("Attorney"),        'attorney',        Attorneys)
add('40', _("Job office"),      'job_office',      JobOffices)
add('90', _("Other"),           'other',           Companies)


#~ class Third(mixins.ProjectRelated,contacts.CompanyContact):
class ClientContact(mixins.ProjectRelated,contacts.CompanyContact):
    """
    project : the Client
    company : the Company
    contact : the Contact person in that Company
    """
    class Meta:
        verbose_name = _("Client Contact")
        verbose_name_plural = _("Client Contacts")
    type = ClientContactTypes.field(blank=True)
    remark = models.TextField(_("Remarks"),blank=True) # ,null=True)
    
    @dd.chooser()
    def company_choices(self,type):
        if not type:  
            return Companies.request().data_iterator
        type = ClientContactTypes.get_by_value(type)
        return type.companies_table.request().data_iterator
        #~ return ClientContactTypes.get_by_value(type).company_choices()
        
dd.update_field(ClientContact,'contact',verbose_name=_("Contact person"))
          
    
class ClientContacts(dd.Table):
    model = ClientContact
    
class ContactsByClient(ClientContacts):
    master_key = 'project'
    column_names = 'type company contact remark *'
    label = _("Contacts")

    
    
#~ class CoachingStates(ChoiceList):
    #~ label = _("Coaching state")
#~ add = CoachingStates.add_item
#~ add('10', _("New"),'new')
#~ add('20', _("Active"),'active')
#~ add('30', _("Standby"),'standby')
#~ add('40', _("Closed"),'closed')

class CoachingType(babel.BabelNamed):
    class Meta:
        verbose_name = _("Coaching type")
        verbose_name_plural = _('Coaching types')

class CoachingTypes(dd.Table):
    model = CoachingType
    column_names = 'name *'
    #~ required_user_level = UserLevels.manager
    required = dict(user_level='manager')

#~ _("Integration"),'integ')     # DSBE
#~ _("General"),'general')       # ASD
#~ _("Debt mediation"),'debts')  # Schuldnerberatung
#~ _("Accounting"),'accounting') # Buchhaltung
#~ _("Human resources"),'human') # Personaldienst
#~ _("Human resources"),'human') # Altenheim
#~ _("Human resources"),'human') # Mosaik
#~ _("Human resources"),'human') # Sekretariat
#~ _("Human resources"),'human') # Häusliche Hilfe
#~ _("Human resources"),'human') # Energiedienst

#~ class CoachingTypes(ChoiceList):
    #~ label = _("Coaching type")
#~ add = CoachingTypes.add_item
#~ add('10', _("Primary coach"),'primary')
#~ add('20', _("Secondary coach"),'secondary')



class Coaching(mixins.UserAuthored,mixins.ProjectRelated):
    """
    A Coaching (Begleitung, accompagnement) 
    is when a Client is being coached by a User (a social assistant) 
    during a given period.
    """
    class Meta:
        verbose_name = _("Coaching")
        verbose_name_plural = _("Coachings")
        
    #~ workflow_state_field = 'state'
    start_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Coached from"))
    end_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("until"))
    #~ state = CoachingStates.field(default=CoachingStates.new)
    #~ type = CoachingTypes.field()
    type = dd.ForeignKey(CoachingType)
    primary = models.BooleanField(_("Primary"))
    
dd.update_field(Coaching,'user',verbose_name=_("Coach"))

class Coachings(dd.Table):
    model = Coaching
    parameters = dict(
        type=dd.ForeignKey(CoachingType,null=True,blank=True),
        group=dd.ForeignKey(PersonGroup,blank=True,null=True),
        today = models.DateField(_("only active on"),blank=True,default=datetime.date.today),
        )
    params_template = "type group today"
    
    @classmethod
    def get_request_queryset(self,ar):
        qs = super(Coachings,self).get_request_queryset(ar)
        if ar.param_values.group:
            qs = qs.filter(project__group=ar.param_values.group)
        if ar.param_values.type:
            qs = qs.filter(type=ar.param_values.type)
        return qs

    
class CoachingsByProject(Coachings):
    master_key = 'project'
    column_names = 'start_date end_date user type *'

class CoachingsByUser(Coachings):
    master_key = 'user'
    column_names = 'start_date end_date project type *'

class MyCoachings(Coachings,mixins.ByUser):
    column_names = 'start_date end_date project type *'



def customize_siteconfig():
    """
    Injects application-specific fields to :class:`SiteConfig <lino.models.SiteConfig>`.
    
    """
    
    from lino.models import SiteConfig
    dd.inject_field(SiteConfig,
        'job_office',
        #~ models.ForeignKey("contacts.Company",
        models.ForeignKey(settings.LINO.company_model,
            blank=True,null=True,
            verbose_name=_("Local job office"),
            related_name='job_office_sites'),
        """The Company whose contact persons will be 
        choices for `Person.job_office_contact`.
        """)
        
    dd.inject_field(SiteConfig,
        'residence_permit_upload_type',
        #~ UploadType.objects.get(pk=2)
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for residence permit"),
            related_name='residence_permit_sites'),
        """The UploadType for `Person.residence_permit`.
        """)
        
    dd.inject_field(SiteConfig,
        'work_permit_upload_type',
        #~ UploadType.objects.get(pk=2)
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for work permit"),
            related_name='work_permit_sites'),
        """The UploadType for `Person.work_permit`.
        """)

    dd.inject_field(SiteConfig,
        'driving_licence_upload_type',
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for driving licence"),
            related_name='driving_licence_sites'))
    


def customize_contacts():
    """
    Injects application-specific fields to :mod:`contacts <lino.modlib.contacts>`.
    """
    dd.inject_field(contacts.RoleType,
        'use_in_contracts',
        models.BooleanField(
            verbose_name=_("usable in contracts"),
            default=True,
            help_text=_("Whether Links of this type can be used as contact person of a job contract.")))
        
        

        

def customize_notes():
    """
    Application-specific changes to :mod:`lino.modlib.notes`.
    """
    from lino.modlib.notes.models import Note, Notes

    dd.inject_field(Note,'company',
        models.ForeignKey(settings.LINO.company_model,
            blank=True,null=True,
            help_text="""\
    An optional third-party Organization that is related to this Note.
    The note will then be visible in that company's history panel.
    """
        ))
        
    def get_person(self):
        return self.project
    Note.person = property(get_person)
        
      
    class NotesByPerson(Notes):
        master_key = 'project'
        column_names = "date event_type type subject body user company *"
        order_by = ["-date"]
      
    class NotesByCompany(Notes):
        master_key = 'company'
        column_names = "date project event_type type subject body user *"
        order_by = ["-date"]
        


def customize_sqlite():
    """
    Here is how we install case-insensitive sorting in sqlite3.
    Note that this caused noticeable performance degradation...

    Thanks to 
    - http://efreedom.com/Question/1-3763838/Sort-Order-SQLite3-Umlauts
    - http://docs.python.org/library/sqlite3.html#sqlite3.Connection.create_collation
    - http://www.sqlite.org/lang_createindex.html
    """
    from django.db.backends.signals import connection_created

    def belgian(s):
      
        s = s.decode('utf-8').lower()
        
        s = s.replace(u'ä',u'a')
        s = s.replace(u'à',u'a')
        s = s.replace(u'â',u'a')
        
        s = s.replace(u'ç',u'c')
        
        s = s.replace(u'é',u'e')
        s = s.replace(u'è',u'e')
        s = s.replace(u'ê',u'e')
        s = s.replace(u'ë',u'e')
        
        s = s.replace(u'ö',u'o')
        s = s.replace(u'õ',u'o')
        s = s.replace(u'ô',u'o')
        
        s = s.replace(u'ß',u'ss')
        
        s = s.replace(u'ù',u'u')
        s = s.replace(u'ü',u'u')
        s = s.replace(u'û',u'u')
        
        return s
        
    def stricmp(str1, str2):
        return cmp(belgian(str1),belgian(str2))
        
    def my_callback(sender,**kw):
        from django.db.backends.sqlite3.base import DatabaseWrapper
        if sender is DatabaseWrapper:
            db = kw['connection']
            db.connection.create_collation('BINARY', stricmp)

    connection_created.connect(my_callback)



class Home(cal.Home):
    label = cal.Home.label
    app_label = 'lino'
    detail_template = """
    quick_links:80x1
    pcsw.UsersWithClients:80x8
    coming_reminders:40x16 missed_reminders:40x16
    """

#~ def setup_master_menu(site,ui,user,m): 
    #~ m.add_action(AllClients)

MODULE_LABEL = _("PCSW")

def setup_explorer_menu(site,ui,user,m): 
    m = m.add_menu("pcsw",MODULE_LABEL)
    m.add_action(Coachings)
    m.add_action(ClientContacts)
    
def setup_my_menu(site,ui,user,m): 
    #~ if user.is_spis:
    if user.profile.integ_level:
        #~ mypersons = m.add_menu("mypersons",MyClients.label)
        #~ mypersons.add_action(MyClients)
        #~ for pg in PersonGroup.objects.order_by('ref_name'):
            #~ mypersons.add_action(
              #~ MyClientsByGroup,
              #~ label=pg.name,
              #~ params=dict(master_instance=pg))
              
        #~ m = m.add_menu("coachings",MyCoachings.label)
        m.add_action(MyClients)
        m.add_action(MyCoachings)
        #~ for pg in PersonGroup.objects.order_by('ref_name'):
            #~ mycoachings.add_action(
              #~ MyCoachingsByGroup,
              #~ label=pg.name,
              #~ params=dict(master_instance=pg))
  


def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("pcsw",MODULE_LABEL)
    #~ config_pcsw     = cfg.add_menu("pcsw",_("SIS"))
    #~ config_pcsw.add_action(self.modules.pcsw.PersonGroups)
    #~ config_pcsw.add_action(self.modules.pcsw.Activities)
    #~ config_pcsw.add_action(self.modules.pcsw.ExclusionTypes)
    #~ config_pcsw.add_action(self.modules.pcsw.AidTypes)
    m.add_action(PersonGroups)
    m.add_action(Activities)
    m.add_action(ExclusionTypes)
    m.add_action(CoachingTypes)
    
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("pcsw",MODULE_LABEL)
    m.add_action(Exclusions)
    m.add_action(PersonSearches)
    

def site_setup(site):
    """
    This is the place where we can override or 
    define application-specific things.
    This includes especially those detail layouts 
    which depend on the *combination* of installed modules.
    """
    
    #~ class HouseholdDetail(households.HouseholdDetail):
        #~ box3 = """
        #~ country region
        #~ city zip_code:10
        #~ street_prefix street:25 street_no street_box
        #~ addr2:40
        #~ activity bank_account1:12 bank_account2:12
        #~ """

    #~ class Households(households.Households):
        #~ model = 'households.Household'
        #~ detail_layout = HouseholdDetail()
        

    site.modules.households.Households.set_detail_layout(box3="""
    country region
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    activity bank_account1:12 bank_account2:12
    """)
    
    
    site.modules.lino.SiteConfigs.set_detail_layout("""
    site_company:20 default_build_method:20 next_partner_id:20 job_office:20
    propgroup_skills propgroup_softskills propgroup_obstacles
    residence_permit_upload_type work_permit_upload_type driving_licence_upload_type
    # lino.ModelsBySite
    """)
    
    site.modules.properties.Properties.set_detail_layout("""
    id group type 
    name
    cv.PersonPropsByProp
    """)
    
    site.modules.countries.Cities.set_detail_layout("""
    name country inscode 
    parent type id
    CitiesByCity
    contacts.PartnersByCity jobs.StudiesByCity
    """)
    
    #~ site.modules.countries.Cities.detail_layout.update(main="""
    #~ name country 
    #~ contacts.PartnersByCity jobs.StudiesByCity
    #~ """)
    
    site.modules.countries.Countries.set_detail_layout("""
    isocode name short_code inscode
    countries.CitiesByCountry jobs.StudiesByCountry
    """)
    
    site.modules.uploads.Uploads.set_detail_layout("""
    file user
    type description valid_until
    # person company
    # reminder_date reminder_text delay_value delay_type reminder_done
    modified created owner
    cal.TasksByController
    # show_date show_time 
    # show_date time timestamp
    """)

    site.modules.uploads.Uploads.set_insert_layout("""
    file user
    type valid_until
    description 
    # owner
    """,window_size=(60,'auto'))


    site.modules.contacts.Persons.set_detail_layout(PersonDetail())

    
    site.modules.cal.Events.set_detail_layout("general more")
    site.modules.cal.Events.add_detail_panel("general","""
    calendar summary user project 
    start end 
    place priority access_class transparent #rset 
    owner state workflow_buttons
    description GuestsByEvent 
    """,_("General"))
    site.modules.cal.Events.add_detail_panel("more","""
    id created:20 modified:20  
    outbox.MailsByController postings.PostingsByController
    """,_("More"))
    
    site.modules.cal.Events.set_insert_layout("""
    summary 
    start end 
    calendar project 
    """,
    start="start_date start_time",
    end="end_date end_time",
    window_size=(60,'auto'))
    
    #~ site.modules.users.Users.set_detail_layout(box2 = """
    #~ level
    #~ integ_level
    #~ cbss_level
    #~ newcomers_level newcomer_quota
    #~ debts_level
    #~ """)
    
    site.modules.users.Users.set_detail_layout("""
    box1:50 box2:25
    remarks AuthoritiesGiven 
    """,
    box2="""
    newcomer_quota
    """)
    
    site.modules.users.Users.add_detail_tab('coaching',"""
    pcsw.CoachingsByUser
    """)
    
        
    site.modules.notes.Notes.set_detail_layout(
        left = """
        date:10 event_type:25 type:25
        subject 
        project company
        id user:10 language:8 build_time
        body
        """,
        
        right = """
        uploads.UploadsByController
        outbox.MailsByController
        postings.PostingsByController
        cal.TasksByController
        """,
        
        main = """
        left:60 right:30
        """
    )
    
    site.modules.notes.Notes.set_insert_layout("""
    event_type:25 type:25
    subject 
    project company
    """,window_size=(50,'auto'))
    
    #~ site.modules.outbox.Mails.set_detail_layout("""
    #~ subject project date 
    #~ user sent #build_time id owner
    #~ RecipientsByMail:50x5 AttachmentsByMail:20x5 uploads.UploadsByOwner:20x5
    #~ body:90x10
    #~ """)
        
    #~ site.modules.courses.CourseProviders.set_detail_layout(CourseProviderDetail())
    
    
dd.add_user_group('integ',_("Integration"))

customize_siteconfig()
customize_contacts()        
customize_notes()
customize_sqlite()
#~ customize_user_groups()
#~ customize_user_profiles()
#~ setup_user_profiles()
  
