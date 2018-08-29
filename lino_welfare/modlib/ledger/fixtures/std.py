# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
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

"""Defines a default accounts chart for social accounting.

Also loads :mod:`lino_xl.lib.ledger.fixtures.std`
and :mod:`lino_welfare.modlib.ledger.fixtures.std_journals`


Purchase invoices go to 4400 (suppliers). Unlike default ledger, 4400
is to be matched by a *disbursement instruction* (Zahlungsanweisung)
which moves them to 4450 (instructions to execute). And then we write
a *payment order* which satisfies the *disbursement instruction*.

Classic accounting:

#. Purchase invoice -> 4400
#. (4400 ->) Payment order -> 5800
#. Bank Statement -> 5500

Lino Welfare accounting:

#. Purchase invoice -> 4400
#. (4400 ->) Disbursement order -> 4450
#. (4450 ->) Payment order -> 5800
#. (5800 ->) Bank Statement -> 5500
#. (4450 ->) Bank Statement -> 5500

"""

from __future__ import unicode_literals

from lino.api import dd, rt, _

def objects():

    from lino_xl.lib.ledger.fixtures import std
    yield std.objects()

    Account = rt.models.ledger.Account

    def account(ref, sheet_item, name, **kw):
        kw.update(dd.str2kw('name', name))
        if dd.is_installed('sheets'):
            Items = rt.models.sheets.Items
            kw.update(sheet_item=Items.get_by_name(sheet_item))
        return Account(
            ref=ref, **kw)

    for ref, name in (
            ('832/3331/01', _("Eingliederungseinkommen")),
            ('832/330/01', _("Allgemeine Beihilfen")),
            ('832/330/03F', _("Fonds Gas und Elektrizität")),
            ('832/330/03', _("Heizkosten- u. Energiebeihilfe")),
            ('832/3343/21', _("Beihilfe für Ausländer")),
            ('832/334/27', _("Sozialhilfe")),
            ('832/333/22', _("Mietbeihilfe")),
            ('832/330/04', _("Mietkaution")),
            ('820/333/01', _("Vorschuss auf Vergütungen o.ä.")),
            ('821/333/01', _("Vorschuss auf Pensionen")),
            ('822/333/01', _("Vorsch. Entsch. Arbeitsunfälle")),
            ('823/333/01', _("Vor. Kranken- u. Invalidengeld")),
            ('825/333/01', _("Vorschuss auf Familienzulage")),
            ('826/333/01', _("Vorschuss auf Arbeitslosengeld")),
            ('827/333/01', _("Vorschuss auf Behindertenzulag")),
            ('P87/000/00', _("Abhebung von pers. Guthaben")),
            ('P82/000/00', _("Einn. Dritter: Weiterleitung")),
            ('P83/000/00', _("Unber. erh. Beträge + Erstatt.")),
            ('832/330/02', _("Gesundheitsbeihilfe")),
            ):
        yield account(
            ref, 'expenses', name,
            purchases_allowed=True, clearable=False, needs_partner=False)

    from lino_welfare.modlib.ledger.fixtures import std_journals
    yield std_journals.objects()
