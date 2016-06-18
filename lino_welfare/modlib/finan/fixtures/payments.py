# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
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


"""
Creates fictive demo bookings to monthly payment orders and bank
statements.

Extends :mod:`lino_cosi.lib.finan.fixtures.demo_bookings`


"""

from __future__ import unicode_literals


import datetime
from dateutil.relativedelta import relativedelta as delta

from django.conf import settings
from lino.utils import Cycler
from lino.api import dd, rt

finan = dd.resolve_app('finan')

REQUEST = settings.SITE.login()  # BaseRequest()


from lino_cosi.lib.finan.fixtures.payments import objects as cosi_objects


def objects():

    # Journal = rt.modules.ledger.Journal
    # USERS = Cycler(settings.SITE.user_model.objects.all())

    # START_YEAR = dd.plugins.ledger.start_year
    # date = datetime.date(START_YEAR, 1, 1)
    # end_date = settings.SITE.demo_date(-30)
    # while date < end_date:
    #     jnl = Journal.objects.get(ref="AAW")
    #     voucher = jnl.create_voucher(
    #         user=USERS.pop(),
    #         date=date + delta(days=10))
    #     yield voucher
    #     sug_table = jnl.voucher_type.table_class.suggestions_table
    #     suggestions = sug_table.request(voucher)
    #     # finan.SuggestionsByPaymentOrder.request(voucher)
    #     ba = sug_table.get_action_by_name('do_fill')
    #     ar = ba.request(master_instance=voucher)
    #     ar.selected_rows = list(suggestions)
    #     ar.run()
    #     voucher.register(REQUEST)
    #     voucher.save()

    #     date += delta(months=1)

    yield cosi_objects('AAW ZKBC')
