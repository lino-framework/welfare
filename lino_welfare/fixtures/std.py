# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals


from django.contrib.contenttypes.models import ContentType
from lino.utils.instantiator import Instantiator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from lino import dd, rt

Person = dd.resolve_model('contacts.Person')
Company = dd.resolve_model('contacts.Company')
ExclusionType = dd.resolve_model('pcsw.ExclusionType')

#~ from lino.modlib.properties import models as properties

ExcerptType = dd.resolve_model('excerpts.ExcerptType')


def excerpt_types():  # also used for migration to 1.1.11

    attType = Instantiator(ExcerptType,
                           # build_method='appypdf',
                           email_template='Default.eml.html').build
    
    Shortcuts = rt.modules.excerpts.Shortcuts
    if dd.is_installed('aids'):
        ConfirmationTypes = rt.modules.aids.ConfirmationTypes
        for ct in ConfirmationTypes.items():
            kw = dict(
                body_template='certificate.body.html',
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
        **dd.babelkw('name',
                  de="Anwesenheitsbescheinigung",
                  fr="Attestation de présence",
                  en="Presence certificate"))

    yield attType(
        build_method='appyrtf',
        template='cv.odt',
        shortcut=Shortcuts.cvs_emitted,
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('pcsw.Client')),
        **dd.babelkw('name',
                  de="Lebenslauf",
                  fr="Curriculum vitae",
                  en="Curriculum vitae"))

    yield attType(
        template='eid-content.odt',
        primary=True,
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('pcsw.Client')),
        **dd.babelkw('name',
                  de="eID-Inhalt",
                  fr="Contenu carte eID",
                  en="eID sheet"))

    yield attType(
        body_template='pac.body.html',
        template='Default.odt',
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('pcsw.Client')),
        **dd.babelkw('name',
                  de="Aktionsplan",
                  fr="Plan d'action",
                  en="to-do list"))

    ExcerptType.update_for_model(
        'jobs.Contract', certifying=True, backward_compat=True)

    ExcerptType.update_for_model(
        'isip.Contract', certifying=True, backward_compat=True)

    if dd.is_installed('debts'):

        kw = dict(
            template='Default.odt',
            certifying=True)
        kw.update(dd.str2kw('name', _("Financial situation")))
        ExcerptType.update_for_model('debts.Budget', **kw)

        # ExcerptType.update_for_model(
        #     'debts.Budget', certifying=True, backward_compat=True)


def objects():

    ClientContactType = rt.modules.pcsw.ClientContactType
    kw = dd.str2kw('name', _("Pharmacy"))  # Apotheke
    cct = ClientContactType(**kw)
    yield cct

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
        **dd.babelkw('name',
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

    excltype = Instantiator('pcsw.ExclusionType', 'name').build
    yield excltype(u"Termin nicht eingehalten")
    yield excltype(u"ONEM-Auflagen nicht erfüllt")

    ContractEnding = dd.resolve_model('isip.ContractEnding')
    yield ContractEnding(name=_("Normal"))
    yield ContractEnding(name=_("Alcohol"), needs_date_ended=True)
    yield ContractEnding(name=_("Health"), needs_date_ended=True)
    yield ContractEnding(name=_("Force majeure"), needs_date_ended=True)

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

    UploadAreas = rt.modules.uploads.UploadAreas
    uploadType = Instantiator(
        'uploads.UploadType',
        # upload_area=UploadAreas.job_search, 
        max_number=1, wanted=True).build
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
        'uploads.UploadType'  # , upload_area=UploadAreas.job_search
    ).build
    yield uploadType(**dd.str2kw('name', _("Contract")))
    # settings.SITE.site_config.driving_licence_upload_type = p
    uploadType = Instantiator(
        'uploads.UploadType'  # , upload_area=UploadAreas.medical
    ).build
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

    uploadType = Instantiator('uploads.UploadType').build
    # upload_area=UploadAreas.career
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

    I = Instantiator(
        'contenttypes.HelpText', 'content_type field help_text').build

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


