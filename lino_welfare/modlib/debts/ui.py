# -*- coding: UTF-8 -*-
# Copyright 2012-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The :xfile:`ui.py` module for `lino_welfare.modlib.debts`.

"""

import logging ; logger = logging.getLogger(__name__)

import decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.encoding import force_text

from lino.api import dd
from lino.core.constants import _handle_attr_name

from lino.modlib.users.mixins import My

from lino_welfare.modlib.pcsw import models as pcsw

from .choicelists import AccountTypes, AMOUNT_WIDTH
from .roles import DebtsUser, DebtsStaff


class Clients(pcsw.CoachedClients):
    # ~ Black right-pointing triangle : Unicode number: U+25B6  HTML-code: &#9654;
    # ~ Black right-pointing pointer Unicode number: U+25BA HTML-code: &#9658;
    help_text = u"""Wie Kontakte --> Klienten, aber mit Kolonnen und Filterparametern für Schuldnerberatung."""
    required_roles = dd.login_required(DebtsUser)
    params_panel_hidden = True
    title = _("DM Clients")
    order_by = "last_name first_name id".split()
    allow_create = False  # see blog/2012/0922
    use_as_default_table = False
    column_names = "name_column:20 national_id:10 gsm:10 address_column email phone:10 id "

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Clients, self).param_defaults(ar, **kw)
        kw.update(coached_by=ar.get_user())
        return kw


class Groups(dd.Table):
    """The global table of all account groups."""
    model = 'debts.Group'
    required_roles = dd.login_required(DebtsStaff)
    order_by = ['ref']
    column_names = 'ref name account_type entries_layout *'

    insert_layout = """
    name
    account_type ref
    """

    detail_layout = """
    ref name id
    account_type entries_layout
    AccountsByGroup
    """


class Accounts(dd.Table):
    model = 'debts.Account'
    required_roles = dd.login_required(DebtsStaff)
    order_by = ['ref']
    column_names = "ref name default_amount periods required_for_household "\
                   "required_for_person group *"
    insert_layout = """
    ref group type
    name
    """
    detail_layout = """
    ref name
    group type
    required_for_household required_for_person periods default_amount
    debts.EntriesByAccount
    """


class AccountsByGroup(Accounts):
    required_roles = dd.login_required()
    master_key = 'group'


class Actors(dd.Table):
    required_roles = dd.login_required(DebtsStaff)
    model = 'debts.Actor'
    column_names = "budget seqno partner header remark *"


class ActorsByBudget(Actors):
    """The table used to edit Actors in a Budget's detail.

    """
    required_roles = dd.login_required(DebtsUser)
    master_key = 'budget'
    column_names = "seqno partner header remark *"
    auto_fit_column_widths = True
    help_text = _("To be filled if there is more than one person involved.")


class ActorsByPartner(Actors):
    required_roles = dd.login_required(DebtsUser)
    master_key = 'partner'
    label = _("Is actor in these budgets:")
    editable = False


class BudgetDetail(dd.DetailLayout):
    """Defines the Detail form of a :class:`Budget`.

    """
    main = "general entries1 entries2 summary_tab preview_tab"
    general = dd.Panel("""
    date partner id user
    intro
    ActorsByBudget
    """, label=_("General"))

    entries1 = dd.Panel("""
    ExpensesByBudget
    IncomesByBudget
    """, label=_("Expenses & Income"))

    entries2 = dd.Panel("""
    LiabilitiesByBudget
    AssetsByBudget
    """, label=_("Liabilities & Assets"))

    tmp_tab = """
    PrintExpensesByBudget
    PrintIncomesByBudget
    """

    summary_tab = dd.Panel("""
    summary1:30 summary2:40
    DistByBudget
    """, label=pgettext(u"debts", u"Summary"))

    summary1 = """
    ResultByBudget
    DebtsByBudget
    AssetsByBudgetSummary
    """
    summary2 = """
    conclusion:30x5
    dist_amount printed total_debt
    include_yearly_incomes print_empty_rows print_todos
    """

    preview_tab = dd.Panel("""
    data_box
    summary_box
    """, label=_("Preview"))

    #~ ExpensesSummaryByBudget IncomesSummaryByBudget
    #~ LiabilitiesSummaryByBudget AssetsSummaryByBudget

    #~ def setup_handle(self,h):
        #~ h.general.label = _("General")
        #~ h.entries1.label = _("Expenses & Income")
        #~ h.entries2.label = _("Liabilities & Assets")
        #~ h.summary_tab.label = pgettext(u"debts",u"Summary")
        #~ h.tmp_tab.label = _("Preview")


class Budgets(dd.Table):
    """
    Base class for lists of :class:`Budgets <Budget>`.
    Serves as base for :class:`MyBudgets` and :class:`BudgetsByPartner`,
    but is directly used by :menuselection:`Explorer --> Debts -->Budgets`.
    """
    model = 'debts.Budget'
    required_roles = dd.login_required(DebtsStaff)
    detail_layout = BudgetDetail()
    insert_layout = """
    partner
    date user
    """

    @dd.constant()
    def spacer(self):
        return '<br/>'


class MyBudgets(My, Budgets):
    required_roles = dd.login_required(DebtsUser)


class BudgetsByPartner(Budgets):
    required_roles = dd.login_required(DebtsUser)
    master_key = 'partner'
    label = _("Is partner of these budgets:")


#

class Entries(dd.Table):
    model = 'debts.Entry'
    required_roles = dd.login_required(DebtsStaff)


class EntriesByType(Entries):
    _account_type = None
    required_roles = dd.login_required(DebtsUser)

    @classmethod
    def get_known_values(self):  # 20130906
        return dict(account_type=self._account_type)

    @classmethod
    def get_actor_label(self):  # 20130906
        if self._account_type is not None:
            return self._account_type.text
        return self._label or self.__name__


class EntriesByAccount(Entries):
    master_key = 'account'


class EntriesByBudget(Entries):

    """
    Base class for the tables used to edit Entries by budget.
    """
    master_key = 'budget'
    column_names = "account description amount actor:10 periods:10 remark move_buttons:8 seqno todo id"
    hidden_columns = "seqno id"
    auto_fit_column_widths = True
    required_roles = dd.login_required(DebtsUser)
    order_by = ['seqno']


class ExpensesByBudget(EntriesByBudget, EntriesByType):
    _account_type = AccountTypes.expenses


class IncomesByBudget(EntriesByBudget, EntriesByType):
    _account_type = AccountTypes.incomes


class LiabilitiesByBudget(EntriesByBudget, EntriesByType):
    _account_type = AccountTypes.liabilities
    column_names = "account partner remark amount actor:10 bailiff distribute monthly_rate:10 move_buttons:8 todo seqno id"


class AssetsByBudget(EntriesByBudget, EntriesByType):
    _account_type = AccountTypes.assets
    column_names = "account remark amount actor move_buttons:8 todo seqno id"


## PrintEntriesByBudget


class EntryGroup(object):
    """Volatile object used to encapsulate the account groups which have
    some data in a given budget.  Entry groups are instantiated and
    yeld by :meth:`Budget.entry_groups
    <lino_welfare.modlib.debts.models.Budget.entry_groups>`, and they
    are used as the master instance for all
    :class:`PrintEntriesByBudget` tables.

    """

    pk = None

    def __init__(self, budget, group, ar):
        self.budget = budget
        self.group = group
        self.action_request = ar.spawn(
            PrintEntriesByBudget, master_instance=self)

    def has_data(self):
        return self.action_request.get_total_count() > 0


class PrintEntriesByBudget(dd.VirtualTable):
    """Base class for the printable tables of entries by budget
(:class:`PrintExpensesByBudget`, :class:`PrintIncomesByBudget`,
:class:`PrintLiabilitiesByBudget` and :class:`PrintAssetsByBudget`).

This is historically the first table that uses Lino's per-request
dynamic columns feature.

This feature means that a single table can have different "column
sets".  You must define a `get_handle_name` method which returns a
"handle name" for each request.  For example if you want a column set
per user, you would add the user name to the default name::

    from lino.core.constants import _handle_attr_name

    class MyTable(...):

        @classmethod
        def get_handle_name(self, ar):
            hname = _handle_attr_name
            hname += ar.get_user().username
            return hname

TODO: more explanations....

.. attribute:: yearly_amount

  Shows the yearly amount. For entries with periodicity 12 this is the
  same as :attr:`total`, otherwise it is `total` * 12 / `periods`.

    """
    master = EntryGroup
    display_mode = 'html'
    # _account_type = None

    # @classmethod
    # def get_actor_label(self):  # 20130906
    #     if self._account_type is not None:
    #         return self._account_type.text
    #     return self._label or self.__name__

    @classmethod
    def get_title(self, ar):
        eg = ar.master_instance
        if eg is None:
            return None
        return str(eg.group)

    @classmethod
    def get_handle_name(self, ar):
        hname = _handle_attr_name
        eg = ar.master_instance
        if eg is not None:
            hname += eg.group.entries_layout.value
            hname += "_" + str(len(eg.budget.get_actors()))
        return hname


    @classmethod
    def get_column_names(self, ar):
        """
        Builds columns dynamically by request. Called once per UI handle.
        """
        eg = ar.master_instance
        if eg is None:
            return
        column_names = eg.group.entries_layout.columns_spec

        if 'dynamic_amounts' in column_names:
            amounts = ''
            actors = eg.budget.get_actors()
            if len(actors) == 1:
                amounts = 'amount0' + AMOUNT_WIDTH
            else:
                for i, a in enumerate(actors):
                    if i <= 4:  # amount4
                        amounts += 'amount' + str(i) + AMOUNT_WIDTH + ' '
                amounts += 'total' + AMOUNT_WIDTH +' '
            column_names = column_names.replace('dynamic_amounts', amounts)
        return column_names

    @classmethod
    def override_column_headers(self, ar):
        d = dict()
        eg = ar.master_instance
        if eg is not None:
            for i, a in enumerate(eg.budget.get_actors()):
                d['amount' + str(i)] = a.header
        return d

    class Row:

        def __init__(self, e):
            self.has_data = e.budget.print_empty_rows
            self.description = e.description
            self.periods = e.periods
            self.partner = e.partner
            self.bailiff = e.bailiff
            self.remarks = []
            self.account = e.account
            self.monthly_rate = e.monthly_rate
            #~ self.todos = [''] * len(e.budget.get_actors())
            self.todo = ''
            self.amounts = [decimal.Decimal(0)] * len(e.budget.get_actors())
            self.total = decimal.Decimal(0)
            self.collect(e)

        def matches(self, e):
            if e.partner != self.partner:
                return False
            if e.bailiff != self.bailiff:
                return False
            if e.account != self.account:
                return False
            if e.monthly_rate != self.monthly_rate:
                return False
            if e.periods != self.periods:
                return False
            if e.description != self.description:
                return False
            return True

        def collect(self, e):
            if e.actor is None:
                i = 0
            else:
                i = e.budget.get_actor_index(e.actor)
            amount = e.amount
            if amount is not None:
                self.has_data = True
                self.amounts[i] += amount
                self.total += amount
            if e.remark:
                self.remarks.append(e.remark)
            if self.todo:
                self.todo += ', '
            self.todo += e.todo
            return True

    @classmethod
    def get_data_rows(self, ar):
        """
        """
        eg = ar.master_instance
        if eg is None:
            return
        qs = eg.budget.entry_set.filter(
            account__group=eg.group).order_by('seqno')
        if ar.filter:
            qs = qs.filter(ar.filter)
        row = None
        for e in qs:
            if row is None:
                row = self.Row(e)
            elif row.matches(e):
                row.collect(e)
            else:
                if row.has_data:
                    yield row
                row = self.Row(e)
        if row is not None:
            if row.has_data:
                yield row

    @dd.virtualfield(dd.PriceField(_("Total")))
    def total(self, obj, ar):
        return obj.total / obj.periods

    @dd.displayfield(_("Description"))
    def full_description(self, obj, ar):
        desc = obj.description
        if len(obj.remarks) > 0:
            desc += ' (%s)' % ', '.join(obj.remarks)
        if obj.periods != 1:
            desc += " (%s / %s)" % (obj.total, obj.periods)
        return desc

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        return obj.description

    @dd.displayfield(_("Remarks"))
    def remarks(self, obj, ar):
        return ', '.join(obj.remarks)

    @dd.virtualfield(dd.PriceField(_("Yearly amount")))
    def yearly_amount(self, obj, ar):
        if obj.periods == 12:
            return obj.total
        return obj.total * 12 / obj.periods

    @dd.displayfield(_("Yearly amount"))
    def old_yearly_amount(self, obj, ar):
        if obj.periods == 1:
            return ''
        if obj.periods == 12:
            return str(obj.total)
        return "%s / %s" % (obj.total, obj.periods)

    @dd.virtualfield(dd.ForeignKey('contacts.Partner'))
    def partner(self, obj, ar):
        return obj.partner

    @dd.virtualfield(dd.ForeignKey(
        'contacts.Company', verbose_name=_("Debt collection agency")))
    def bailiff(self, obj, ar):
        return obj.bailiff

    @dd.virtualfield(dd.PriceField(_("Monthly rate")))
    def monthly_rate(self, obj, ar):
        return obj.monthly_rate

    # TODO: generate amountN columns dynamically.

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount0(self, obj, ar):
        return obj.amounts[0] / obj.periods

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount1(self, obj, ar):
        return obj.amounts[1] / obj.periods

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount2(self, obj, ar):
        return obj.amounts[2] / obj.periods

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount3(self, obj, ar):
        return obj.amounts[3] / obj.periods

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount4(self, obj, ar):
        return obj.amounts[4] / obj.periods


class SummaryTable(dd.VirtualTable):
    auto_fit_column_widths = True
    column_names = "desc:60 amount:12"
    display_mode = 'html'

    @classmethod
    def get_title_base(self, ar):
        # we want just "Debts", not "Debts of Budget #3"
        return self.title or self.label

    @dd.displayfield(_("Description"))
    def desc(self, row, ar):
        # print("20160531 get_data_rows", force_text(row[0]))
        return force_text(row[0])

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self, row, ar):
        return row[1]

    @classmethod
    def get_sum_text(self, ar, sums):
        """
        Return the text to display on the totals row.
        """
        return self.label

    @classmethod
    def get_data_rows(self, ar):
        for row in self.get_summary_numbers(ar):
            if row[1]:  # don't show summary rows with value 0
                yield row


class ResultByBudget(SummaryTable):
    help_text = _("""Shows the Incomes & Expenses for this budget.""")
    label = _("Incomes & Expenses")
    required_roles = dd.login_required(DebtsUser)
    master = 'debts.Budget'

    @classmethod
    def get_summary_numbers(self, ar):
        budget = ar.master_instance
        if budget is None:
            return
        yield [_("Monthly incomes"), budget.sum('amount', 'I', periods=1)]
        # yield ["Monatliche Einkünfte", budget.sum('amount', 'I', periods=1)]
        if budget.include_yearly_incomes:
            yi = budget.sum('amount', 'I', periods=12)
            if yi:
                # txt = "Jährliche Einkünfte (%s / 12)"
                txt = _("Yearly incomes ({0} / 12)")
                txt = txt.format(dd.decfmt(yi * 12, places=2))
                yield [txt, yi]

        a = budget.sum('amount', 'I', exclude=dict(periods__in=(1, 12)))
        # yield ["Einkünfte mit sonstiger Periodizität", a]
        yield [_("Incomes with other periodicity"), a]

        # yield ["Monatliche Ausgaben", -budget.sum('amount', 'E', periods=1)]
        yield [_("Monthly expenses"), -budget.sum('amount', 'E', periods=1)]

        a = - budget.sum('amount', 'E', exclude=dict(periods__in=(1, 12)))
        # yield ["Ausgaben mit sonstiger Periodizität", a]
        yield [_("Expenses with other periodicity"), a]

        ye = budget.sum('amount', 'E', periods=12)
        if ye:
            txt = _("Monthly reserve for yearly expenses ({0} / 12)")
            txt = txt.format(dd.decfmt(ye * 12, places=2))
            yield [txt, -ye]
            # yield [
            #     ("Monatliche Reserve für jährliche Ausgaben (%s / 12)"
            #      % dd.decfmt(ye * 12, places=2)),
            #     -ye]

        # ye = budget.sum('amount','E',models.Q(periods__ne=1) & models.Q(periods__ne=12))
        # if ye:
        #     yield [
        #       u"Monatliche Reserve für sonstige periodische Ausgaben",
        #       -ye]

        # yield ["Raten der laufenden Kredite",
        yield [_("Monthly installment for running credits"),
               -budget.sum('monthly_rate', 'L')]

    @classmethod
    def get_sum_text(self, ar, sums):
        return _("Remaining for credits and debts")
        # return _("Restbetrag für Kredite und Zahlungsrückstände")


class DebtsByBudget(SummaryTable):
    label = _("Liabilities")
    required_roles = dd.login_required(DebtsUser)
    master = 'debts.Budget'

    @classmethod
    def get_summary_numbers(self, ar):
        budget = ar.master_instance
        if budget is None:
            return
        for eg in budget.entry_groups(ar, 'L'):
            if not eg.has_data():
                continue
            for acc in eg.group.account_set.all():
                yield [_("%s (distributable)") % dd.babelattr(acc, 'name'),
                       budget.sum('amount', account=acc, distribute=True)]
                yield [dd.babelattr(acc, 'name'),
                       budget.sum('amount', account=acc, distribute=False)]
        #~ "Total Kredite / Schulden"


class AssetsByBudgetSummary(SummaryTable):
    label = _("Assets")
    required_roles = dd.login_required(DebtsUser)
    master = 'debts.Budget'

    @classmethod
    def get_summary_numbers(self, ar):
        budget = ar.master_instance
        if budget is None:
            return
        for eg in budget.entry_groups(ar, 'A'):
            if not eg.has_data():
                continue
            for acc in eg.group.account_set.all():
                yield [dd.babelattr(acc, 'name'),
                       budget.sum('amount', account=acc)]


class DistByBudget(EntriesByBudget):

    column_names = "partner:30 description:30 amount:12 dist_perc:8 dist_amount:12"
    filter = models.Q(distribute=True)
    label = _("Debts distribution")
    known_values = dict(account_type=AccountTypes.liabilities)
    display_mode = 'html'
    help_text = _("""\
Répartition au marc-le-franc.
A table with one row per entry in Liabilities which has "distribute" checked,
proportionally distributing the `Distributable amount` among the debtors.
""")

    @classmethod
    def get_title_base(self, ar):
        return self.label

    @classmethod
    def get_data_rows(self, ar):
        budget = ar.master_instance
        if budget is None:
            return
        qs = self.get_request_queryset(ar)
        #~ fldnames = ['amount1','amount2','amount3']
        #~ sa = [models.Sum(n) for n in fldnames]
        total = decimal.Decimal(0)

        entries = []
        for e in qs.annotate(models.Sum('amount')):
            if e.amount__sum:
                total += e.amount__sum
            entries.append(e)

        for e in entries:
            if e.amount is not None:
                e.dist_perc = 100 * e.amount / total
                #~ if e.dist_perc == 0:
                    #~ e.dist_amount = decimal.Decimal(0)
                #~ else:
                e.dist_amount = budget.dist_amount * e.dist_perc / 100
                yield e

    @dd.virtualfield(dd.PriceField(_("%")))
    def dist_perc(self, row, ar):
        return row.dist_perc

    @dd.virtualfield(dd.PriceField(_("Monthly payback suggested")))
    def dist_amount(self, row, ar):
        return row.dist_amount

    @classmethod
    def override_column_headers(self, ar):
        d = dict()
        d.update(partner=_("Creditor"))
        d.update(amount=_("Debt"))
        return d

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        desc = obj.description
        if obj.remark:
            desc += ' (%s)' % obj.remark
        return desc
            #~ return "%s (%s / %s)" % (obj.description,obj.total,obj.periods)
        #~ return obj.description
