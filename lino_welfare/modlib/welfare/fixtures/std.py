# -*- coding: UTF-8 -*-
# Copyright 2008-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from django.contrib.contenttypes.models import ContentType
from lino.utils.instantiator import Instantiator
from lino_xl.lib.notes.choicelists import SpecialTypes

from lino.api import dd, rt, _


def objects():

    ClientContactType = rt.models.clients.ClientContactType
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
    yield noteType(
        "Auswertungsbogen allgemein",
        build_method='rtf', template='Auswertungsbogen_allgemein.rtf')

    yield noteType(
        special_type=SpecialTypes.first_meeting,
        **dd.str2kw("name", _("First meeting")))  # "Erstgespräch"

    yield noteType(
        build_method='appyrtf', template='Letter.odt',
        **dd.babelkw('name',
                     de="Brief oder Einschreiben",
                     fr="Lettre",
                     en="Letter"))

    # yield excerpt_types()

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

    I = Instantiator(
        'gfks.HelpText', 'content_type field help_text').build

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
