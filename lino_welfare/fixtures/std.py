# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals


from django.contrib.contenttypes.models import ContentType
from lino.utils.instantiator import Instantiator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from north.dbutils import babelkw, babel_values

from lino import dd

Person = dd.resolve_model('contacts.Person')
Company = dd.resolve_model('contacts.Company')
ExclusionType = dd.resolve_model('pcsw.ExclusionType')

#~ from lino.modlib.properties import models as properties

ContractEnding = dd.resolve_model('isip.ContractEnding')
ExcerptType = dd.resolve_model('excerpts.ExcerptType')


def excerpt_types():  # also used for migration to 1.1.11

    attType = Instantiator(ExcerptType,
                           # build_method='appypdf',
                           email_template='Default.eml.html').build
    ConfirmationTypes = dd.modules.aids.ConfirmationTypes
    for ct in ConfirmationTypes.items():
        kw = dict(
            body_template='aid_certificate.body.html',
            template='Default.odt',
            primary=True,
            # print_directly=False,
            content_type=ContentType.objects.get_for_model(ct.model))
        kw.update(dd.str2kw('name', ct.model._meta.verbose_name))
        ExcerptType.update_for_model(ct.model, **kw)
        # yield attType(**kw)
    yield attType(
        body_template='presence_certificate.body.html',
        template='Default.odt',
        primary=True,
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('cal.Guest')),
        **babelkw('name',
                  de="Anwesenheitsbescheinigung",
                  fr="Attestation de présence",
                  en="Presence certificate"))

    yield attType(
        build_method='appyrtf',
        template='cv.odt',
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('pcsw.Client')),
        **babelkw('name',
                  de="Lebenslauf",
                  fr="Curriculum vitae",
                  en="Curriculum vitae"))

    yield attType(
        template='eid-content.odt',
        primary=True,
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('pcsw.Client')),
        **babelkw('name',
                  de="eID-Inhalt",
                  fr="Contenu carte eID",
                  en="eID sheet"))

    yield attType(
        body_template='pac.body.html',
        template='Default.odt',
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('pcsw.Client')),
        **babelkw('name',
                  de="Aktionsplan",
                  fr="Plan d'action",
                  en="to-do list"))

    ExcerptType.update_for_model(
        'jobs.Contract', certifying=True, backward_compat=True)

    ExcerptType.update_for_model(
        'isip.Contract', certifying=True, backward_compat=True)

    if dd.is_installed('debts'):
        ExcerptType.update_for_model(
            'debts.Budget', certifying=True, backward_compat=True)


def objects():

    noteType = Instantiator(
        'notes.NoteType', "name",
        email_template='Default.eml.html').build

    yield noteType("Beschluss")
    yield noteType(
        "Konvention",
        remark="Einmaliges Dokument in Verbindung mit Arbeitsvertrag")
    yield noteType(
        "Notiz",
        remark="Kontaktversuch, Gesprächsbericht, Telefonnotiz")
    yield noteType("Vorladung", remark="Einladung zu einem persönlichen Gespräch")
    # (--> Datum Eintragung DSBE)
    yield noteType("Übergabeblatt", remark="Übergabeblatt vom allgemeinen Sozialdienst")
    yield noteType("Neuantrag")
    yield noteType("Antragsformular")
    yield noteType("Auswertungsbogen allgemein", build_method='rtf', template='Auswertungsbogen_allgemein.rtf')
    #~ yield noteType("Anwesenheitsbescheinigung",build_method='rtf',template='Anwesenheitsbescheinigung.rtf')
    yield noteType("Erstgespräch")

    yield noteType(
        build_method='appyrtf', template='Letter.odt',
        **babelkw('name',
                  de="Brief oder Einschreiben",
                  fr="Lettre",
                  en="Letter"))

    yield excerpt_types()
        
    eventType = Instantiator('notes.EventType', "name remark").build

    yield eventType("Aktennotiz", remark="Alle Notizen/Ereignisse, die keine andere Form haben")
    yield eventType("Brief", remark="Brief an Kunde, Personen, Organisationen")
    yield eventType("E-Mail", "E-Mail an Kunde, Personen, Organisationen")
    yield eventType("Einschreiben", "Brief, der per Einschreiben an Kunde oder an externe Personen / Dienst verschickt wird	")
    yield eventType("Gespräch EXTERN", "Persönliches Gespräch außerhalb des ÖSHZ, wie z.B. Vorstellungsgespräch im Betrieb, Auswertungsgespräch, gemeinsamer Termin im Arbeitsamt, im Integrationsprojekt, .")
    yield eventType("Gespräch INTERN", "Persönliches Gespräch im ÖSHZ")
    yield eventType("Hausbesuch", "Hausbesuch beim Kunden")
    yield eventType("Kontakt ÖSHZ intern", "Kontakte mit Kollegen oder Diensten im ÖSHZ, z.B. Fallbesprechung mit Allgemeinem Sozialdienst, Energieberatung, Schuldnerberatung, Sekretariat, ...")
    yield eventType("Telefonat", "Telefonischer Kontakt mit dem Kunden, anderen Personen, Diensten oder Organisationen ....")

    #~ projectType = Instantiator('projects.ProjectType',"name").build
    #~ yield projectType(u"VSE Ausbildung")
    #~ yield projectType(u"VSE Arbeitssuche")
    #~ yield projectType(u"VSE Integration")
    #~ yield projectType(u"Hausinterne Arbeitsverträge")
    #~ yield projectType(u"Externe Arbeitsverträge")
    #~ yield projectType(u"Kurse und Zusatzausbildungen")

    #~ yield projectType(u"Sozialhilfe")
    #~ yield projectType(u"EiEi")
    #~ yield projectType(u"Aufenthaltsgenehmigung")

    eduLevel = Instantiator('isip.EducationLevel').build
    yield eduLevel(**babel_values('name',
                                  de="Primär",
                                  fr="Primaire",
                                  en="Primary"))
    yield eduLevel(**babel_values('name',
                                  de="Sekundär",
                                  fr="Secondaire",
                                  en="Secondary"))
    yield eduLevel(**babel_values('name',
                                  de="Hochschule",
                                  fr="Supérieur",
                                  en="Higher"))
    yield eduLevel(**babel_values('name',
                                  de="Bachelor",
                                  fr="Bachelor",
                                  en="Bachelor"))
    yield eduLevel(**babel_values('name',
                                  de="Master",
                                  fr="Master",
                                  en="Master"))

    studyType = Instantiator('isip.StudyType').build
    yield studyType(**babel_values('name',
                                   de=u"Schule",
                                   fr=u"École",
                                   en=u"School",
                                   ))
    yield studyType(**babel_values('name',
                                   de=u"Sonderschule",
                                   fr=u"École spéciale",
                                   en=u"Special school",
                                   ))
    yield studyType(**babel_values('name',
                                   de=u"Ausbildung",
                                   fr=u"Formation",
                                   en=u"Schooling",
                                   ))
    yield studyType(**babel_values('name',
                                   de=u"Lehre",
                                   fr=u"Apprentissage",
                                   en=u"Apprenticeship",
                                   ))
    yield studyType(**babel_values('name',
                                   de=u"Hochschule",
                                   fr=u"École supérieure",
                                   en=u"Highschool",
                                   ))
    yield studyType(**babel_values('name',
                                   de=u"Universität",
                                   fr=u"Université",
                                   en=u"University",
                                   ))
    yield studyType(**babel_values('name',
                                   de=u"Teilzeitunterricht",
                                   fr=u"Cours à temps partiel",
                                   en=u"Part-time study",
                                   ))
    yield studyType(**babel_values('name',
                                   de=u"Fernkurs",
                                   fr=u"Cours à distance",
                                   en=u"Remote study",
                                   ))

    #~ studyContent = Instantiator('pcsw.StudyContent',"name").build
    #~ yield studyContent(u"Grundschule")
    #~ yield studyContent(u"Mittlere Reife")
    #~ yield studyContent(u"Abitur")
    #~ yield studyContent(u"Schlosser")
    #~ yield studyContent(u"Schreiner")
    #~ yield studyContent(u"Biotechnologie")
    #~ yield studyContent(u"Geschichte")
    #~ license = Instantiator('pcsw.DrivingLicense',"id name").build
    #~ yield license('A',u"Motorrad")
    #~ yield license('B',u"PKW")
    #~ yield license('C',u"LKW")
    #~ yield license('CE',u"LKW über X Tonnen")
    #~ yield license('D',u"Bus")
    #~ coachingType = Instantiator('pcsw.CoachingType',"name").build
    #~ yield coachingType(u"DSBE")
    #~ yield coachingType(u"Schuldnerberatung")
    #~ yield coachingType(u"Energieberatung")
    #~ yield coachingType(u"allgemeiner Sozialdienst")
    excltype = Instantiator('pcsw.ExclusionType', 'name').build
    yield excltype(u"Termin nicht eingehalten")
    yield excltype(u"ONEM-Auflagen nicht erfüllt")

    #~ linkType = Instantiator('links.LinkType',"a_type b_type name").build

    #~ yield linkType(
        #~ ContentType.objects.get_for_model(Company),
        #~ ContentType.objects.get_for_model(Person),
        #~ babelitem(de=u"Direktor",fr=u"directeur"))
    #~ yield linkType(
        #~ ContentType.objects.get_for_model(Person),
        #~ ContentType.objects.get_for_model(Person),
        #~ babelitem(de=u"Vater",fr=u"père"))
    #~ yield linkType(
        #~ ContentType.objects.get_for_model(Person),
        #~ ContentType.objects.get_for_model(Person),
        #~ babelitem(de=u"Mutter",fr=u"mère"))
    #~ yield linkType(babelitem(de=u"Private Website",fr=u"Site privé"))
    #~ yield linkType(babelitem(de=u"Firmen-Website",fr=u"Site commercial"))
    #~ yield linkType(babelitem(de=u"Facebook-Profil",fr=u"Profil Facebook"))
    #~ yield linkType(babelitem(de=u"Sonstige",fr=u"Autres"))

    #~ from lino.models import update_site_config

    UploadAreas = dd.modules.uploads.UploadAreas
    uploadType = Instantiator(
        'uploads.UploadType',
        upload_area=UploadAreas.job_search, max_number=1, wanted=True).build
    yield uploadType(**dd.babelkw(
        'name',
        de=u"Personalausweis", fr=u"Carte d'identité", en="ID card"))
    yield uploadType(**dd.babelkw(
        'name', de=u"Aufenthaltserlaubnis",
        fr=u"Permis de séjour", en="Residence permit"))
    yield uploadType(**dd.babelkw(
        'name', de=u"Arbeitserlaubnis",
        fr=u"Permis de travail", en="Work permit"))
    yield uploadType(**dd.babelkw(
        'name', de=u"Führerschein",
        fr=u"Permis de conduire", en="Diving licence"))
    uploadType = Instantiator(
        'uploads.UploadType',
        upload_area=UploadAreas.job_search).build
    yield uploadType(**dd.str2kw('name', _("Contract")))
    # settings.SITE.site_config.driving_licence_upload_type = p
    uploadType = Instantiator(
        'uploads.UploadType', upload_area=UploadAreas.medical).build
    yield uploadType(
        **dd.babelkw(
            'name',
            de="Ärztliche Bescheinigung",
            fr="Certificat médical",
            en="Medical certificate"))
    yield uploadType(
        **dd.babelkw(
            'name',
            de="Behindertenausweis",
            fr="Certificat de handicap",
            en="Handicap certificate"))

    uploadType = Instantiator(
        'uploads.UploadType',
        upload_area=UploadAreas.career).build
    yield uploadType(wanted=True, **dd.str2kw('name', _("Diploma")))

    yield settings.SITE.site_config

    #~ from lino.modlib.cal.utils import DurationUnits
    #~ from lino.modlib.cal.models import EventType
    #~ from lino.modlib.cal.models import Calendar
    #~ yield Calendar(**babel_values('name',
          #~ de=u"Erstgespräch",
          #~ fr=u"Première rencontre",
          #~ en=u"First meeting",
      #~ ))
    #~ yield et
    #~ calendar = Instantiator('cal.Calendar').build
    #~ et = calendar(invite_client=True,**babel_values('name',
          #~ de="Privat",
          #~ fr="Privé",
          #~ en="Private",
          #~ ))
    #~ yield et
    #~ et = Calendar(**babel_values('name',
      #~ de=u'Auswertungen',
      #~ fr=u"Evaluations",
      #~ en=u"Evaluations",
      #~ ))
    #~ def create_dsbe_aidtype(id,name,name_fr):
        #~ return AidType(id=id,name=name,name_fr=name_fr)
    # aidtype = Instantiator('pcsw.AidType').build
    # yield aidtype(**babel_values(
    #     'name',
    #     de=u'Eingliederungseinkommen Kat 1 (Zusammenlebend)',
    #     fr=u"Revenu d'intégration cat. 1 (couple)",
    #     en=u"Revenu d'intégration cat. 1 (couple)",
    # ))
    # yield aidtype(**babel_values(
    #     'name',
    #     de=u'Eingliederungseinkommen Kat 2 (Alleinlebend)',
    #     fr=u"Revenu d'intégration cat. 2 (célibataire)",
    #     en=u"Revenu d'intégration cat. 2 (célibataire)",
    # ))
    # yield aidtype(**babel_values(
    #     'name',
    #     de=u'Eingliederungseinkommen Kat 3 (Familie zu Lasten)',
    #     fr=u"Revenu d'intégration cat. 3 (famille à charge)",
    #     en=u"Revenu d'intégration cat. 3 (famille à charge)",
    # ))
    # yield aidtype(**babel_values(
    #     'name',
    #     de=u'Ausl\xe4nderbeihilfe Kat 1 (Zusammenlebend)',
    #     fr=u"Aide aux immigrants cat. 1 (couple)",
    #     en=u"Aide aux immigrants cat. 1 (couple)",
    # ))
    # yield aidtype(**babel_values(
    #     'name',
    #     de=u'Ausl\xe4nderbeihilfe Kat 2 (Alleinlebend)',
    #     fr=u"Aide aux immigrants cat. 2 (célibataire)",
    #     en=u"Aide aux immigrants cat. 2 (célibataire)",
    # ))
    # yield aidtype(**babel_values(
    #     'name',
    #     de=u'Ausl\xe4nderbeihilfe Kat 3 (Familie zu Lasten)',
    #     fr=u"Aide aux immigrants cat. 3 (famille à charge)",
    #     en=u"Aide aux immigrants cat. 3 (famille à charge)",
    # ))
    # yield aidtype(**babel_values(
    #     'name',
    #     de=u'Sonstige Sozialhilfe',
    #     fr=u"Autre aide sociale",
    #     en=u"Autre aide sociale",
    # ))

    yield ContractEnding(name=_("Normal"))
    yield ContractEnding(name=_("Alcohol"), needs_date_ended=True)
    yield ContractEnding(name=_("Health"), needs_date_ended=True)
    yield ContractEnding(name=_("Force majeure"), needs_date_ended=True)

    I = Instantiator('system.HelpText', 'content_type field help_text').build

    Client = dd.resolve_model('pcsw.Client')
    t = ContentType.objects.get_for_model(Client)
    yield I(t, 'in_belgium_since', u"""\
Since when this person in Belgium lives.
<b>Important:</b> help_text can be formatted.""")
    yield I(t, 'noble_condition', u"""\
The eventual noble condition of this person. Imported from TIM.
""")
    #~ t = ContentType.objects.get_for_model(Person)
    #~ yield I(t,'birth_date',u"""\
#~ Unkomplette Geburtsdaten sind erlaubt, z.B.
#~ <ul>
#~ <li>00.00.1980 : irgendwann in 1980</li>
#~ <li>00.07.1980 : im Juli 1980</li>
#~ <li>23.07.0000 : Geburtstag am 23. Juli, Alter unbekannt</li>
#~ </ul>
#~ """)

    Partner = dd.resolve_model('contacts.Partner')
    t = ContentType.objects.get_for_model(Partner)
    yield I(t, 'language', u"""\
    Die Sprache, in der Dokumente ausgestellt werden sollen.
""")


