# -*- coding: UTF-8 -*-
# Copyright 2012-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
A minimal demo account chart for debts mediators.
"""


from lino.api import dd, rt

from lino.utils.instantiator import Instantiator


def objects():
    AccountTypes = rt.models.debts.AccountTypes
    TableLayouts = rt.models.debts.TableLayouts
    group = Instantiator('debts.Group').build
    g = group(
        ref="10", account_type=AccountTypes.incomes,
        entries_layout=TableLayouts.get_by_value('11'),
        **dd.babel_values(
            'name',
            de=u"Monatliche Einkünfte",
            fr=u"Revenus mensuels",
            en=u"Monthly incomes"))
    yield g
    account = Instantiator('debts.Account', group=g).build
    yield account(
        ref="1010", required_for_person=True, **dd.babel_values(
            'name',
            de=u"Gehälter",
            fr=u"Salaires",
            en=u"Salaries"))
    yield account(
        ref="1020", required_for_person=True, **dd.babel_values(
            'name',
            de=u"Renten",
            fr=u"Pension",
            en=u"Pension"))
    yield account(
        ref="1030", required_for_person=True, **dd.babel_values(
            'name',
            de=u"Integrationszulage",
            fr=u"Allocation d'intégration",
            en=u"Integration aid"))
    yield account(
        ref="1040", required_for_person=True, **dd.babel_values(
            'name',
            de=u"Ersatzeinkünfte",
            fr=u"Ersatzeinkünfte",
            en=u"Ersatzeinkünfte"))
    yield account(
        ref="1050", required_for_person=True, **dd.babel_values(
            'name',
            de=u"Alimente",
            fr=u"Aliments",
            en=u"Aliments"))
    yield account(ref="1060", required_for_person=True, **dd.babel_values(
        'name',
        de=u"Essen-Schecks",
        fr=u"Chèques-repas",
        en=u"Chèques-repas"))
    yield account(ref="1090", required_for_person=True, **dd.babel_values(
        'name',
        de=u"Andere",
        fr=u"Andere",
        en=u"Andere"
    ))

    g = group(
        ref="20", account_type=AccountTypes.incomes,
        entries_layout=TableLayouts.get_by_value('30'),
        **dd.babel_values(
            'name',
            de=u"Jährliche Einkünfte",
            fr=u"Revenus annuels",
            en=u"Yearly incomes"))
    yield g
    account = Instantiator('debts.Account', group=g, periods=12).build
    yield account(ref="2010", required_for_person=True, **dd.babel_values(
        'name',
        de=u"Urlaubsgeld",
        fr=u"Congé payé",
        en=u"Paid holiday"))
    yield account(ref="2020", required_for_person=True, **dd.babel_values(
        'name',
        de=u"Jahresendzulage",
        fr=u"Prime de fin d'année",
        en=u"Year-end prime"))
    yield account(ref="2030", required_for_person=True, **dd.babel_values(
        'name',
        de=u"Gewerkschaftsprämie",
        fr=u"Gewerkschaftsprämie",
        en=u"Gewerkschaftsprämie"))

    g = group(
        ref="11", account_type=AccountTypes.expenses,
        entries_layout=TableLayouts.get_by_value('10'),
        **dd.babel_values('name',
                          de=u"Monatliche Ausgaben",
                          fr=u"Dépenses mensuelles",
                          en=u"Monthly expenses"))
    yield g
    account = Instantiator('debts.Account', group=g).build
    yield account(
        ref="3010", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Miete",
                                                                fr=u"Loyer",
                                                                en=u"Rent"
                                                                ))
    yield account(
        ref="3011", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Wasser",
                                                                fr=u"Eau",
                                                                en=u"Water"
                                                                ))
    yield account(
        ref="3012", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Strom",
                                                                fr=u"Electricité",
                                                                en=u"Electricity"
                                                                ))
    yield account(
        ref="3020", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Festnetz-Telefon und Internet",
                                                                fr=u"Téléphone fixe et Internet",
                                                                en=u"Telephone & Internet"
                                                                ))
    yield account(
        ref="3021", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Handy",
                                                                fr=u"GSM",
                                                                en=u"Cell phone"
                                                                ))
    yield account(
        ref="3030", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Fahrtkosten",
                                                                fr=u"Frais de transport",
                                                                en=u"Transport costs"
                                                                ))
    yield account(
        ref="3031", required_for_household=True, **dd.babel_values('name',
                                                                de=u"TEC Busabonnement",
                                                                fr=u"Abonnement bus",
                                                                en=u"Public transport"
                                                                ))
    yield account(
        ref="3032", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Benzin",
                                                                fr=u"Essence",
                                                                en=u"Fuel"
                                                                ))
    yield account(
        ref="3033", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Unterhalt Auto",
                                                                fr=u"Maintenance voiture",
                                                                en=u"Car maintenance"
                                                                ))
    yield account(
        ref="3040", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Schulkosten",
                                                                fr=u"École",
                                                                en=u"School"
                                                                ))
    yield account(
        ref="3041", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Tagesmutter & Kleinkindbetreuung",
                                                                fr=u"Garde enfant",
                                                                en=u"Babysitting"
                                                                ))
    yield account(
        ref="3050", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Gesundheit",
                                                                fr=u"Santé",
                                                                en=u"Health"
                                                                ))
    yield account(
        ref="3051", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Kleidung",
                                                                fr=u"Vêtements",
                                                                en=u"Clothes"
                                                                ))
    yield account(
        ref="3052", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Ernährung",
                                                                fr=u"Alimentation",
                                                                en=u"Food"
                                                                ))
    yield account(
        ref="3053", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Hygiene",
                                                                fr=u"Hygiène",
                                                                en=u"Hygiene"
                                                                ))
    yield account(
        ref="3060", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Krankenkassenbeiträge",
                                                                fr=u"Mutuelle",
                                                                en=u"Health insurance"
                                                                ))
    yield account(
        ref="3061", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Gewerkschaftsbeiträge",
                                                                fr=u"Cotisations syndicat",
                                                                en=u"Labour fees"
                                                                ))
    yield account(
        ref="3062", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Unterhaltszahlungen",
                                                                fr=u"Unterhaltszahlungen",
                                                                en=u"Unterhaltszahlungen"
                                                                ))
    yield account(
        ref="3070", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Tabak",
                                                                fr=u"Tabac",
                                                                en=u"Tobacco"
                                                                ))
    yield account(
        ref="3071", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Freizeit & Unterhaltung",
                                                                fr=u"Loisirs",
                                                                en=u"Spare time"
                                                                ))
    yield account(
        ref="3072", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Haustiere",
                                                                fr=u"Animaux domestiques",
                                                                en=u"Pets"
                                                                ))
    yield account(
        ref="3063", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Pensionssparen",
                                                                fr=u"Épargne pension",
                                                                en=u"Retirement savings"
                                                                ))
    yield account(
        ref="3090", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Sonstige",
                                                                fr=u"Autres",
                                                                en=u"Other"
                                                                ))

    g = group(
        ref="40", account_type=AccountTypes.expenses,
        entries_layout=TableLayouts.get_by_value('10'), **dd.babel_values(
            'name',
            de=u"Steuern",
            fr=u"Taxes",
            en=u"Taxes"))
    yield g
    account = Instantiator('debts.Account', group=g, periods=12).build
    yield account(
        ref="4010", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Gemeindesteuer",
                                                                fr=u"Taxe communale",
                                                                en=u"Municipal tax"
                                                                ))
    yield account(
        ref="4020", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Kanalisationssteuer",
                                                                fr=u"Kanalisationssteuer",
                                                                en=u"Kanalisationssteuer"
                                                                ))
    yield account(
        ref="4030", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Müllsteuer",
                                                                fr=u"Taxe déchets",
                                                                en=u"Waste tax"
                                                                ))
    yield account(
        ref="4040", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Autosteuer",
                                                                fr=u"Taxe circulation",
                                                                en=u"Autosteuer"
                                                                ))
    yield account(
        ref="4050", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Immobiliensteuer",
                                                                fr=u"Taxe immobilière",
                                                                en=u"Immobiliensteuer"
                                                                ))
    yield account(
        ref="4090", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Andere",
                                                                fr=u"Autres",
                                                                en=u"Other"
                                                                ))

    g = group(
        ref="50", account_type=AccountTypes.expenses,
        entries_layout=TableLayouts.get_by_value('10'), **dd.babel_values(
            'name',
            de=u"Versicherungen",
            fr=u"Assurances",
            en=u"Insurances"))
    yield g
    account = Instantiator('debts.Account', group=g, periods=12).build
    yield account(
        ref="5010", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Feuer",
                                                                fr=u"Incendie",
                                                                en=u"Fire"
                                                                ))
    yield account(
        ref="5020", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Familienhaftpflicht",
                                                                fr=u"Responsabilité famille",
                                                                en=u"Familienhaftpflicht"
                                                                ))
    yield account(
        ref="5030", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Auto",
                                                                fr=u"Voiture",
                                                                en=u"Car insurance"
                                                                ))
    yield account(
        ref="5040", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Lebensversicherung",
                                                                fr=u"Assurance vie",
                                                                en=u"Life insurance"
                                                                ))
    yield account(
        ref="5090", required_for_household=True, **dd.babel_values('name',
                                                                de=u"Andere Versicherungen",
                                                                fr=u"Autres assurances",
                                                                en=u"Other insurances"
                                                                ))

    g = group(
        ref="60", account_type=AccountTypes.assets,
        entries_layout=TableLayouts.get_by_value('30'), **dd.babel_values(
            'name',
            de=u"Aktiva, Vermögen, Kapital",
            fr=u"Actifs",
            en=u"Assets"))
    yield g
    account = Instantiator('debts.Account', group=g).build
    yield account(ref="6010", **dd.babel_values('name',
                                             de=u"Haus",
                                             fr=u"Maison",
                                             en=u"House"
                                             ))
    yield account(ref="6020", **dd.babel_values('name',
                                             de=u"Auto",
                                             fr=u"Voiture",
                                             en=u"Car"
                                             ))

    g = group(
        ref="70", account_type=AccountTypes.liabilities,
        entries_layout=TableLayouts.get_by_value('20'), **dd.babel_values(
            'name',
            de="Schulden, Zahlungsrückstände, Kredite",
            fr="Dettes, paiements en retard et crédits",
            en="Debts, outsanding payments and credits"))
    yield g
    account = Instantiator('debts.Account', group=g).build
    yield account(ref="7010", **dd.babel_values(
        'name',
        de="Kredite",
        fr="Crédits",
        en="Loans"))
    yield account(ref="7020", **dd.babel_values(
        'name',
        de="Schulden",
        fr="Dettes",
        en="Debts"))
    yield account(ref="7040", **dd.babel_values(
        'name',
        de="Zahlungsrückstände",
        fr="Factures à payer",
        en="Invoices to pay"))

    g = group(
        ref="71", account_type=AccountTypes.liabilities,
        entries_layout=TableLayouts.get_by_value('40'), **dd.babel_values(
            'name',
            de="Gerichtsvollzieher und Inkasso",
            fr="Huissiers et agents d'encaissement",
            en="Bailiffs and cash collectors"))
    yield g
    account = Instantiator('debts.Account', group=g).build
    yield account(ref="7100", **dd.babel_values(
        'name',
        de="Gerichtsvollzieher",
        fr="Huissier",
        en="Bailiff"))
    yield account(ref="7110", **dd.babel_values(
        'name',
        de="Inkasso-Unternehmen",
        fr="Agent d'encaissement",
        en="Cash agency"))
