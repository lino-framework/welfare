# -*- coding: UTF-8 -*-
# Copyright 2011-2020 Rumma & Ko Ltd
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
"""Adds default data for `PersonGroup` and `DispenseReason`.

"""

from django.utils.translation import ugettext_lazy as _

from lino.utils.instantiator import Instantiator, i2d
from lino.api.dd import babelkw


from lino.api import dd, rt


def objects():
    from lino.api import dd, rt
    pcsw = dd.resolve_app('pcsw')

    #~ persongroup = Instantiator('pcsw.PersonGroup','name').build
    # Auswertung / Bilan
    yield pcsw.PersonGroup(ref_name='1', name=_("Evaluation"))
    # Formation / Ausbildung
    yield pcsw.PersonGroup(ref_name='2', name=_("Formation"))
    yield pcsw.PersonGroup(ref_name='4', name=_("Search"))  # Suche / Recherche
    yield pcsw.PersonGroup(ref_name='4bis', name=_("Work"))  # Arbeit / Travail
    yield pcsw.PersonGroup(ref_name='9', name=_("Standby"))
    #~ yield persongroup(u"Bilan",ref_name='1')
    #~ yield persongroup(u"Formation",ref_name='2')
    #~ yield persongroup(u"Recherche",ref_name='4')
    #~ yield persongroup(u"Travail",ref_name='4bis')
    #~ yield persongroup(u"Standby",ref_name='9',active=False)

    yield pcsw.DispenseReason(**babelkw('name', de="Gesundheitlich", fr="Santé", en="Health"))
    yield pcsw.DispenseReason(**babelkw('name', de="Studium/Ausbildung", fr="Etude/Formation", en="Studies"))
    yield pcsw.DispenseReason(**babelkw('name', de="Familiär", fr="Cause familiale", en="Familiar"))
    yield pcsw.DispenseReason(**babelkw('name', de="Sonstige", fr="Autre", en="Other"))
