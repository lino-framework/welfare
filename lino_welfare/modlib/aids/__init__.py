# Copyright 2014-2015 Luc Saffre
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


r"""Provides functionality for managing "social aids". An "aid" here
means the decision that some client gets some kind of aid during a
given period.

See also :doc:`/specs/aids`.

.. autosummary::
   :toctree:

    mixins
    choicelists
    models
    fixtures.std
    fixtures.demo

Templates
=========

Here is a list of the templates defined in the `Aids` module.

..  Building the following requires the lino_welfare.projects.std
    database to be populated.

.. django2rst::

  try:
    from django.utils import translation
    from atelier.rstgen import header
    from lino.api.shell import *

    def f(name):
        print("\n\n.. xfile:: %s\n\n" % name)
    
        print("\nSee the :srcref:`source code <lino_welfare/modlib/aids/config/aids/Confirmation/%s>`" % name)

        try:
            at = aids.AidType.objects.get(body_template=name)
        except (aids.AidType.MultipleObjectsReturned, aids.AidType.DoesNotExist):
            print("(no example documents)")
            return
    
        qs = at.confirmation_type.model.objects.all()
        qs = qs.filter(granting__aid_type=at, printed_by__isnull=False)
        print("or %d example documents:" % qs.count())

        items = []
        for conf in qs:
            ex = conf.printed_by
            url = "http://de.welfare.lino-framework.org/dl/excerpts/"
            url += ex.filename_root()
            url += ex.get_build_method().target_ext
            items.append("`%s <%s>`__" % (conf, url))
        print(', '.join(items))

    for name in '''
    certificate.body.html
    clothing_bank.body.html
    fixed_income.body.html
    food_bank.body.html
    foreigner_income.body.html
    furniture.body.html
    heating_refund.body.html
    integ_income.body.html
    medical_refund.body.html
    urgent_medical_care.body.html
    '''.split():
        if not name.startswith("#"):
            f(name)
    

  except Exception as e:
    print("Oops: %s" % e)



"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Aids")

    def setup_main_menu(config, site, profile, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.MyPendingGrantings')

    def setup_config_menu(config, site, profile, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.AidTypes')
        m.add_action('aids.Categories')

    def setup_explorer_menu(config, site, profile, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.AllGrantings')
        m.add_action('aids.AllIncomeConfirmations')
        m.add_action('aids.AllRefundConfirmations')
        m.add_action('aids.AllSimpleConfirmations')
