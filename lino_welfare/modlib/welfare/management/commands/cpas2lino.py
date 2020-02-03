# -*- coding: UTF-8 -*-
# Copyright 2016-2020 Rumma & Ko Ltd.
"""

Defines the :manage:`cpas2lino` management command:

.. management_command:: cpas2lino

.. py2rst::

  from lino_welfare.modlib.welfare.management.commands.cpas2lino \
      import Command
  print(Command.help)

"""

# from optparse import make_option

from clint.textui import puts, progress

from django.conf import settings

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from lino.utils import dpy
from lino.utils import SumCollector
from lino.api import rt

from lino.api import dd

from lino_xl.lib.tim2lino.utils import TimLoader
from lino_xl.lib.sepa.utils import be2iban

User = rt.models.users.User
ledger = rt.models.ledger
vatless = rt.models.vatless
finan = rt.models.finan
contacts = rt.models.contacts
pcsw = rt.models.pcsw
sepa = rt.models.sepa


def get_user_or_none(m, pk):
    pk = pk.strip()
    if not pk:
        return None
    try:
        return m.objects.get(pk=int(pk))
    except m.DoesNotExist:
        return None

WANTED_ACCOUNTS = """
820/333/01        	Vorschüsse Vergütungen u.ä.
821/333/01        	Vorschüsse Pensionen
822/333/01        	Vorschüsse Unfallentschäd./Berufskrankh.
823/333/01        	Vorschüsse Kranken- und Invalidengeld
825/333/01        	Vorschüsse Familienzulagen/Geburtspräm.
826/333/01        	Vorschüsse auf Arbeitslosengeld
827/333/01        	Vorschüsse auf Behindertenzulagen
832/330/01        	Allgemeine Beihilfen
832/330/02        	Beihilfen im Gesundheitsbereich
832/330/03        	Heizkosten- und Energiebeihilfen
832/330/03B       	Heizölzulage (durch Staat bezuschusst)
832/330/03F       	Fonds Gas und Elektrizität
832/330/04        	Mietkautionen
832/330/05        	Sozio-kulturelle Beteiligung (Allgemein)
832/330/06        	Sozio-kulturelle Beteiligung (Kinder)
832/333/22        	Mietbeihilfen
832/3331/01       	EM/Eingliederungseinkommen
832/334/04        	Beihilfen zur Krankenhausunterbringung
832/334/07        	Unterbr. Kinder in eigenen Einricht.
832/334/08        	Unterbr. Kinder in auswärtigen Einricht.
832/334/09        	Unterbringung von Behinderten
832/334/10        	Unterbringung Senioren St. Josef
832/334/11        	Unterbringung Senioren in ausw.Einricht.
832/334/13        	Unterbring.in Aufnahmehäusern
832/334/16        	Unterbringung Krippen/Tagesmütterdienste
832/334/18        	Interv.zu Leistungen Familienhilfsdienst
832/334/26        	Beihilfen Beerdigungskosten
832/334/27        	LBA-Schecks
832/334/28        	Förderung sozialer Zusammenhalt
832/334/29        	Neuansiedlung Flüchtlinge
832/3341/21       	Hospital.von Belgiern mit Unterstütz.ws.
832/3342/03       	Transportbeihilfen
832/3342/21       	Hospit.Ausl./Belgier ohne Unterstütz.ws.
832/3343/21       	Ausländerbeihilfen (f. Rechnung Staat)
832/3344/21       	Rückführung belg. Bedürftiger aus Ausl.
832/3345/21       	Sozialh. f.Kinder <18 J.ohne Unterst.ws.
832-380/04        	Erst. Interv. Energieversorgungssektor
832/435/02        	Zahl.an hilfeleist.Zentr.f.gel.Sozialh.
832-465/01        	Erst. Staatsinterv. EM/Einglied.einkomm.
832-465/08        	Erst. Heizölzulagen Föderalstaat
832-465/11        	Erst. soziokultur. Beteilig.Staat
832-4652/03       	Erstatt. an Staat von Einn. 832/-3342/21
832-4653/03       	Erstatt. an Staat von Einn. 832/-3343/21
"""


def wanted_accounts():
    Account = rt.models.ledger.Account
    AccountTypes = rt.models.ledger.AccountTypes
    # Group = rt.models.accounts.Group
    # grp = Group.objects.all()
    for ln in WANTED_ACCOUNTS.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        ref, name = ln.split(None, 1)
        obj = Account.get_by_ref(ref, None)
        if obj is None:
            obj = Account(
                ref=ref, name=name,
                # group=grp,
                clearable=True,
                type=AccountTypes.expenses)
            yield obj


class TimLoader(TimLoader):

    archive_name = 'LFD'

    archived_tables = set('IMP IML'.split())

    def unused_load_jnl_alias(self, row, **kw):
        if row.alias == 'IMP':
            finan = rt.models.finan
            ledger = rt.models.ledger
            # accounts = rt.models.accounts
            # idgen = row.idgen.strip()
            idgrj = row.idgrj.strip()
            if idgrj == "AAW":
                vcl = finan.DisbursementOrder
            elif row.idgrj == "ZAU":
                vcl = finan.PaymentOrder
                kw.update(trade_type=ledger.TradeTypes.purchases)
            elif idgrj == "TRE":
                if row.compte.strip():
                    vcl = finan.BankStatement
                else:
                    vcl = finan.JournalEntry
            elif idgrj == "REG":
                vcl = vatless.AccountInvoice
            else:
                return None, kw
            kw.update(
                journal_group=ledger.JournalGroups.get_by_name(
                    idgrj.lower()))
            return vcl, kw
        return super(TimLoader, self).load_jnl_alias(row, **kw)

    def row2idbudref(self, row):
        # return row.dc + ' ' + '/'.join(row.idbud.strip().split())
        return '/'.join(row.idbud.strip().split())

    def row2account(self, row):
        ref = self.row2idbudref(row)
        acc = ledger.Account.get_by_ref(ref, None)
        if acc is None:
            if ref not in self.ignored_accounts:
                self.ignored_accounts.add(ref)
                dd.logger.warning("Ignored %s : no such account", ref)
        return acc

    def unused_load_bud(self, row, **kw):
        idbud = row.idbud.strip()
        if not idbud:
            return
        kw.update(ref=self.row2account(row))
        kw.update(seqno=row.recno())
        kw.update(group=self.group)
        if row.dc == "A":
            kw.update(type=ledger.AccountTypes.expenses)
        else:
            kw.update(type=ledger.AccountTypes.incomes)
        self.babel2kw('name', 'name', row, kw)
        obj = ledger.Account(**kw)
        # dd.logger.info("20160302 %s", dd.obj2str(obj))
        yield obj

    def fiscal_year(self, per):
        return ledger.FiscalYear.get_by_ref(per[:2])

    def tim2number(self, number):
        number = number.strip()
        if number[0] == "A":
            number = "10" + number[1:]
        elif number[0] == "B":
            number = "20" + number[1:]
        if not number.isdigit():
            raise Exception("20160304 invalid number {}".format(number))
        return number

    def tim2period(self, ref):
        M = ledger.AccountingPeriod
        try:
            ap = M.objects.get(ref=ref)
        except M.DoesNotExist:
            ap = M(ref=ref, year=self.fiscal_year(ref))
            ap.full_clean()
            ap.save()
        return ap

    def tim2partner(self, m, pk):
        pk = pk.strip()
        if not pk:
            return None
        pk = int(pk)
        try:
            return m.objects.get(pk=pk)
        except m.DoesNotExist:
            if m.__name__ == "Client":
                self.missing_clients.add(1)
            else:
                self.missing_partners.add(1)
            return None

    def load_imp(self, row, **kw):
        jnl = ledger.Journal.get_by_ref(row.idjnl.strip(), None)
        if jnl is None:
            return
        if jnl.journal_group != ledger.JournalGroups.anw:
            return
        ap = self.tim2period(row.periode.strip())
        voucher_model = jnl.voucher_type.model
        acc = self.row2account(row)
        number = self.tim2number(row.iddoc)
        try:
            imp = voucher_model.objects.get(journal=jnl, number=number)
        except voucher_model.DoesNotExist:
            imp = voucher_model(journal=jnl, number=number)

        par, prj = self.row2parprj(row)
        imp.partner = par
        imp.project = prj
        compte = self.tim2compte(row, par, prj)
        imp.entry_date = row.date1
        imp.voucher_date = row.date2
        imp.accounting_period = ap
        username = settings.TIM2LINO_USERNAME(row.idusr.strip())
        if username:
            try:
                imp.user = User.objects.get(username=username)
            except User.DoesNotExist:
                if row.idusr.strip() not in self.unknown_users:
                    self.unknown_users.add(row.idusr.strip())
                    dd.logger.warning(
                        "%s %s : Unknown username '%s'",
                        row.idjnl, row.iddoc, row.idusr)

        # dd.logger.info("20160304 %s", imp)
        self.rows_by_year.collect(imp.entry_date.year, 1)
        imp.full_clean()
        # imp.save()
        if issubclass(voucher_model, vatless.AccountInvoice):
            imp.account = acc
            imp.narration = row.nb1.strip()
            imp.your_ref = row.nb2.strip()
            if compte:
                imp.bank_account = compte
        elif issubclass(voucher_model, finan.FinancialVoucher):
            imp.item_remark = row.nb2.strip()
            imp.item_account = acc
            if compte:
                if row.compte1.strip() not in self.ignored_bank_accounts:
                    self.ignored_bank_accounts.add(row.compte1.strip())
                    dd.logger.warning(
                        "%s %s : Ignoring bank account '%s'",
                        row.idjnl, row.iddoc, row.compte1)
        else:
            raise Exception("Unknown voucher_model {}".format(
                voucher_model))

        return imp

    def row2parprj(self, row):
        par = self.tim2partner(contacts.Partner, row.idpar2)
        prj = self.tim2partner(pcsw.Client, row.idpar)
        if prj is None and par is None:
            par = self.tim2partner(contacts.Partner, row.idpar)
        return par, prj

    def tim2compte(self, row, par, prj):
        compte = row.compte1.strip()
        if not compte:
            return
        a = compte.split(':')
        if len(a) == 1:
            try:
                iban = be2iban(compte)
            except ValidationError:
                iban = compte
        else:
            bic, iban = a
        if not iban:
            return
        qs = sepa.Account.objects.filter(iban=iban)
        if qs.count() == 1:
            return qs[0]
        elif qs.count() == 0:
            acc = sepa.Account(iban=iban, partner=par or prj)
            acc.full_clean()
            acc.save()
            return acc
        else:
            if par:
                qs2 = qs.filter(partner=par)
                if qs2.count() == 1:
                    return qs2[0]
            if prj:
                qs2 = qs.filter(partner=prj)
                if qs2.count() == 1:
                    return qs2[0]
        self.undefined_bank_accounts.add(iban)
        return

    def load_iml(self, row, **kw):
        idjnl = row.idjnl.strip()
        jnl = ledger.Journal.get_by_ref(idjnl, None)
        if jnl is None:
            if idjnl not in self.ignored_journals:
                dd.logger.warning("Ignoring journal %s", idjnl)
                self.ignored_journals.add(idjnl)
            return
        if jnl.journal_group != ledger.JournalGroups.anw:
            return
        voucher_model = jnl.voucher_type.model
        acc = self.row2account(row)
        number = self.tim2number(row.iddoc)
        try:
            imp = voucher_model.objects.get(journal=jnl, number=number)
        except voucher_model.DoesNotExist:
            imp = voucher_model(journal=jnl, number=number)
            imp.full_clean()
            imp.save()

        if acc is None:
            return
        kw.update(voucher=imp)
        kw.update(seqno=int(row.line))
        kw.update(amount=row.mont)

        kw.update(account=acc)
        par, prj = self.row2parprj(row)
        if prj:
            kw.update(project=prj)
        compte = self.tim2compte(row, par, prj)
        match = row.match.strip()
        if issubclass(voucher_model, vatless.AccountInvoice):
            # kw.update(remark=row.nb1.strip())
            kw.update(title=row.nb2.strip())
            if match:
                if match != imp.match:
                    self.ignored_matches.collect(jnl.ref, 1)
                    dd.logger.warning(
                        "Ignoring non-empty match in row %(seqno)s "
                        "of %(voucher)s", kw)
                else:
                    imp.match = match
                    imp.full_clean()
                    imp.save()
            if par:
                if par != imp.partner:
                    self.ignored_partners.collect(jnl.ref, 1)
                    dd.logger.warning(
                        "Ignoring non-empty partner in row %(seqno)s "
                        "of %(voucher)s", kw)
                else:
                    imp.partner = par
                    imp.full_clean()
                    imp.save()
            if compte:
                dd.logger.warning(
                    "%s %s : Ignoring bank account '%s'",
                    row.idjnl, row.iddoc, row.compte1)
        elif issubclass(voucher_model, finan.FinancialVoucher):
            kw.update(dc=(row.dc == "A"))
            kw.update(remark=row.nb1.strip())
            # kw.update(title=row.nb2.strip())
            if match:
                kw.update(match=match)
            if par:
                kw.update(partner=par)
            if compte:
                if issubclass(voucher_model, finan.PaymentOrder):
                    kw.update(bank_account=compte)
                else:
                    dd.logger.warning(
                        "%s %s : Ignoring bank account '%s'",
                        row.idjnl, row.iddoc, row.compte1)
        else:
            raise Exception("Unknown voucher_model {}".format(
                voucher_model))
        obj = jnl.voucher_type.get_items_model()(**kw)
        # dd.logger.info("20160304 %s", obj)
        return obj

    def load_mvi(self, row, **kw):
        pass

    def objects(self):

        self.ignored_journals = set()
        self.ignored_accounts = set()
        self.ignored_bank_accounts = set()
        self.undefined_bank_accounts = set()
        self.unknown_users = set()
        self.missing_partners = set()
        self.missing_clients = set()
        self.rows_by_year = SumCollector()
        self.ignored_matches = SumCollector()
        self.ignored_partners = SumCollector()

        yield wanted_accounts()

        # self.group = accounts.Group(name="Imported from TIM")
        # self.group.full_clean()
        # self.group.save()

        # yield self.load_dbf('BUD')

        # # self.after_gen_load()

        # yield self.load_dbf('JNL')

        # from lino_xl.lib.vat.fixtures import euvatrates
        # yield euvatrates.objects()

        settings.SITE.loading_from_dump = True
        yield self.load_dbf('IML')
        yield self.load_dbf('IMP')
        # yield self.load_dbf('MVI')
        settings.SITE.loading_from_dump = False

        if len(self.must_register) == 0:
            return

        ses = rt.login('roger')

        dd.logger.info("Register %d vouchers", len(self.must_register))
        failures = 0
        for doc in progress.bar(self.must_register):
            # puts("Registering {0}".format(doc))
            try:
                doc.register(ses)
            except Exception as e:
                dd.logger.warning("Failed to register %s : %s ", doc, e)
                failures += 1
                if failures > 100:
                    dd.logger.warning("Abandoned after 100 failures.")
                    break

    def write_report(self):
        self.ignored_accounts = sorted(self.ignored_accounts)
        self.ignored_journals = sorted(self.ignored_journals)
        self.missing_partners = sorted(self.missing_partners)
        self.missing_clietns = sorted(self.missing_clients)

        for k in ('ignored_journals', 'ignored_accounts',
                  'rows_by_year', 'ignored_matches',
                  'ignored_partners', 'missing_partners', 'missing_clients',
                  'unknown_users', 'undefined_bank_accounts',
                  'ignored_bank_accounts'):

            dd.logger.info("%s = %s", k, getattr(self, k))


class Command(BaseCommand):
    args = "/path/to/tim/data"

    help = """

    Import accounting data from TIM into this Lino database. To be
    invoked using something like::

        python manage.py cpas2lino /path/to/tim/data

    This was used in March 2016 as part of the NBH project for weleup.

    """

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError(self.help)

        models = []
        from lino_xl.lib.ledger.choicelists import VoucherTypes
        for vt in VoucherTypes.items():
            models.append(vt.get_items_model())
            models.append(vt.model)

        # from lino_xl.lib.ledger.mixins import VoucherItem
        # models = list(rt.models_by_base(rt.models.ledger.Voucher))
        # models += list(rt.models_by_base(VoucherItem))

        # from lino_xl.lib.finan.mixins import (FinancialVoucher,
        #                                         FinancialVoucherItem)
        # models = list(rt.models_by_base(FinancialVoucher))
        # models += list(rt.models_by_base(FinancialVoucherItem))
        # # models.append(rt.models.ledger.Journal)
        # models.append(rt.models.ledger.Voucher)
        models.append(rt.models.ledger.Movement)
        if True:
            for m in models:
                qs = m.objects.all()
                dd.logger.info("Delete %d rows from %s.", qs.count(), m)
                qs.delete()
                # for obj in qs:
                #     obj.delete()

        for pth in args:
            tim = TimLoader(pth)
            for obj in expand(tim.objects()):
                obj.full_clean()
                obj.save()
            tim.write_report()


def expand(obj):
    if obj is None:
        pass  # ignore None values
    elif hasattr(obj, '__iter__'):
        for o in obj:
            for so in expand(o):
                yield so
    else:
        yield obj
