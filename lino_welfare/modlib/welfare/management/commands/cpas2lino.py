# -*- coding: UTF-8 -*-
# Copyright 2016 by Luc Saffre.
"""

Defines the :manage:`cpas2lino` management command:

.. management_command:: cpas2lino

.. py2rst::

  from lino_welfare.modlib.welfare.management.commands.cpas2lino \
      import Command
  print(Command.help)

"""

from __future__ import unicode_literals, print_function

# from optparse import make_option

from clint.textui import puts, progress

from django.conf import settings

from django.core.management.base import BaseCommand, CommandError

from lino.utils import dpy
from lino.api import rt

from lino.api import dd

from lino_cosi.lib.tim2lino.utils import TimLoader

User = rt.modules.users.User
accounts = rt.modules.accounts
ledger = rt.modules.ledger
vatless = rt.modules.vatless
finan = rt.modules.finan
contacts = rt.modules.contacts
pcsw = rt.modules.pcsw
# Account = rt.modules.accounts.Account


def get_or_none(m, pk):
    pk = pk.strip()
    if not pk:
        return None
    try:
        return m.objects.get(pk=int(pk))
    except m.DoesNotExist:
        return None


class TimLoader(TimLoader):

    archive_name = 'LFD'

    archived_tables = set('IMP IML'.split())

    def unused_load_jnl_alias(self, row, **kw):
        if row.alias == 'IMP':
            finan = rt.modules.finan
            ledger = rt.modules.ledger
            # accounts = rt.modules.accounts
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

    def row2account(self, row):
        # return row.dc + ' ' + '/'.join(row.idbud.strip().split())
        return '/'.join(row.idbud.strip().split())

    def unused_load_bud(self, row, **kw):
        idbud = row.idbud.strip()
        if not idbud:
            return
        kw.update(ref=self.row2account(row))
        kw.update(seqno=row.recno())
        kw.update(group=self.group)
        if row.dc == "A":
            kw.update(type=accounts.AccountTypes.expenses)
        else:
            kw.update(type=accounts.AccountTypes.incomes)
        self.babel2kw('name', 'name', row, kw)
        obj = accounts.Account(**kw)
        # dd.logger.info("20160302 %s", dd.obj2str(obj))
        yield obj

    def fiscal_year(self, per):
        return ledger.FiscalYears.get_by_value(per[:2])

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

    def load_imp(self, row, **kw):
        jnl = ledger.Journal.get_by_ref(row.idjnl.strip(), None)
        if jnl is None:
            return
        ap = self.tim2period(row.periode.strip())
        voucher_model = jnl.voucher_type.model
        acc = self.row2account(row)
        number = self.tim2number(row.iddoc)
        try:
            imp = voucher_model.objects.get(journal=jnl, number=number)
        except voucher_model.DoesNotExist:
            imp = voucher_model(journal=jnl, number=number)

        imp.partner = get_or_none(contacts.Partner, row.idpar2)
        imp.project = get_or_none(pcsw.Client, row.idpar)
        imp.entry_date = row.date1
        imp.account = acc
        imp.voucher_date = row.date2
        imp.accounting_period = ap
        imp.user = row.idusr

        if issubclass(voucher_model, vatless.AccountInvoice):
            kw.update(narration=row.nb1.strip())
            kw.update(your_ref=row.nb2.strip())
        elif issubclass(voucher_model, finan.FinancialVoucher):
            kw.update(remark=row.nb2.strip())
        else:
            raise Exception("Unknown voucher_model {}".format(
                voucher_model))

        dd.logger.info("20160304 %s", imp)
        return imp
        # imp.full_clean()
        # imp.save()

    def load_iml(self, row, **kw):
        idjnl = row.idjnl.strip()
        jnl = ledger.Journal.get_by_ref(idjnl, None)
        if jnl is None:
            if idjnl not in self.ignored:
                dd.logger.warning("Ignoring journal %s", idjnl)
                self.ignored.add(idjnl)
            return
        voucher_model = jnl.voucher_type.model
        ref = self.row2account(row)
        number = self.tim2number(row.iddoc)
        try:
            imp = voucher_model.objects.get(journal=jnl, number=number)
        except voucher_model.DoesNotExist:
            imp = voucher_model(journal=jnl, number=number)
            imp.full_clean()
            imp.save()
            
        acc = accounts.Account.get_by_ref(ref, None)
        if acc is None:
            if ref not in self.ignored_accounts:
                self.ignored_accounts.add(ref)
                dd.logger.warning("Ignored %s : no such account", ref)
            return
        kw.update(voucher=imp)
        kw.update(seqno=int(row.line))
        kw.update(amount=row.mont)

        kw.update(account=acc)
        p = get_or_none(contacts.Partner, row.idpar2)
        if p:
            kw.update(partner=p)
        p = get_or_none(pcsw.Client, row.idpar)
        if p:
            kw.update(project=p)
        match = row.match.strip()
        if issubclass(voucher_model, vatless.AccountInvoice):
            # kw.update(remark=row.nb1.strip())
            kw.update(title=row.nb2.strip())
            if match:
                if imp.match:
                    dd.logger.warning(
                        "Ignoring non-empty match of %(seqno)s in %(voucher)s",
                        **kw)
                else:
                    imp.match = match
                    imp.full_clean()
                    imp.save()
        elif issubclass(voucher_model, finan.FinancialVoucher):
            kw.update(dc=(row.dc == "A"))
            kw.update(remark=row.nb1.strip())
            # kw.update(title=row.nb2.strip())
            if match:
                kw.update(match=match)
        else:
            raise Exception("Unknown voucher_model {}".format(
                voucher_model))
        obj = jnl.voucher_type.get_items_model()(**kw)
        dd.logger.info("20160304 %s", obj)
        return obj

    def load_mvi(self, row, **kw):
        pass

    def objects(self):

        self.ignored = set()
        self.ignored_accounts = set()

        # self.group = accounts.Group(name="Imported from TIM")
        # self.group.full_clean()
        # self.group.save()

        # yield self.load_dbf('BUD')

        # # self.after_gen_load()

        # yield self.load_dbf('JNL')

        # from lino_cosi.lib.vat.fixtures import euvatrates
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


class Command(BaseCommand):
    args = "Input_file1.xls [Input_file2.xls] ..."
    help = """

    Import accounting data from TIM into this Lino database. To be
    invoked using something like::

        python manage.py cpas2lino /path/to/tim/data

    This is designed to be used several times in March 2016 during the
    transitional phase.

    """

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError(self.help)

        models = []
        from lino_cosi.lib.ledger.choicelists import VoucherTypes
        for vt in VoucherTypes.items():
            models.append(vt.get_items_model())
            models.append(vt.model)

        # from lino_cosi.lib.ledger.mixins import VoucherItem
        # models = list(rt.models_by_base(rt.modules.ledger.Voucher))
        # models += list(rt.models_by_base(VoucherItem))

        # from lino_cosi.lib.finan.mixins import (FinancialVoucher,
        #                                         FinancialVoucherItem)
        # models = list(rt.models_by_base(FinancialVoucher))
        # models += list(rt.models_by_base(FinancialVoucherItem))
        # # models.append(rt.modules.ledger.Journal)
        # models.append(rt.modules.ledger.Voucher)
        models.append(rt.modules.ledger.Movement)
        if True:
            for m in models:
                qs = m.objects.all()
                dd.logger.info("Delete %d rows from %s.", qs.count(), m)
                qs.delete()

        for pth in args:
            tim = TimLoader(pth)
            for obj in expand(tim.objects()):
                obj.full_clean()
                obj.save()


def expand(obj):
    if obj is None:
        pass  # ignore None values
    elif hasattr(obj, '__iter__'):
        for o in obj:
            for so in expand(o):
                yield so
    else:
        yield obj


