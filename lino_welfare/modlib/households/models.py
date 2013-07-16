# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

"""
This module extends :mod:`lino.modlib.cal.models`
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

from lino.modlib.households.models import *

from lino_welfare.modlib.contacts.models import Partner

class Household(Household):
    """
    for lino_welfare we want to inherit also from lino_welfare's Partner
    """
    #~ class Meta(households.Household.Meta):
        #~ app_label = 'households'
        
    #~ @classmethod
    #~ def on_analyze(cls,site):
        #~ super(Household,cls).on_analyze(site)
        #~ cls.declare_imported_fields('type')
          
    def disable_delete(self,ar):
        # skip the is_imported_partner test
        return super(Partner,self).disable_delete(ar)
        
