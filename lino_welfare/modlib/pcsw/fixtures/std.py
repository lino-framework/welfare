# -*- coding: UTF-8 -*-
# Copyright 2011-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds default data for `PersonGroup` and `DispenseReason`.

"""

from django.utils.translation import gettext_lazy as _

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
