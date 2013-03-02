# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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


class SiteMixin(object):
    
    cbss_live_tests = False
    """
    Whether unit tests should try to really connect to the cbss.
    Some test cases of the test suite would fail with a timeout if run 
    from behind an IP address that is not registered at the :term:`CBSS`.
    These tests are skipped by default. To activate them, 
    set `cbss_live_tests` to `True` in your :xfile:`settings.py`.
    
    """
    
    cbss_environment = None
    """
    Either `None` or one of 'test', 'acpt' or 'prod'.
    See :mod:`lino.modlib.cbss.models`.
    Leaving this to `None` means that the cbss module is "inactive" even if installed.
    """
    
    
