# -*- coding: UTF-8 -*-
## Copyright 2002-2012 Luc Saffre
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

"""
The ``lino_welfare`` module can be imported even from a Django :xfile:`settings.py` 
file since it does not import any django module.

"""

import os

__name__ = "Lino/Welfare"

#~ __version__ = file(os.path.join(os.path.dirname(
    #~ __file__),'..','VERSION')).read().strip()
__version__ = "1.0.1"
"""
Version number. 
"""

__author__ = "Luc Saffre <luc.saffre@gmx.net>"

#~ __url__ = "http://lino-welfare.saffre-rumma.net"
__url__ = "http://code.google.com/p/lino-welfare/"

__copyright__ = """\
Copyright (c) 2002-2012 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""


