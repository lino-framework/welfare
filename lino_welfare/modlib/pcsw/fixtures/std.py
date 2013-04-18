# -*- coding: UTF-8 -*-
## Copyright 2011,2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from lino.utils.instantiator import Instantiator, i2d
from north.dbutils import babel_values, babelitem

def objects():
  
    persongroup = Instantiator('pcsw.PersonGroup','name').build
    #~ pg1 = persongroup(u"Art. 60 § 7",ref_name='1')
    pg1 = persongroup(u"Bilan",ref_name='1')
    yield pg1
    #~ pg2 = persongroup(u"Préformation",ref_name='2')
    pg2 = persongroup(u"Formation",ref_name='2')
    yield pg2
    #~ yield persongroup(u"Formation",ref_name='3')
    yield persongroup(u"Recherche",ref_name='4')
    yield persongroup(u"Travail",ref_name='4bis')
    standby = persongroup(u"Standby",ref_name='9',active=False)
    yield standby
