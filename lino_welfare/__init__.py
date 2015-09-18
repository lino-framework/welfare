# -*- coding: UTF-8 -*-
# Copyright 2002-2015 Luc Saffre
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

""":mod:`lino_welfare` is the main module of Lino Welfare.

.. autosummary::
   :toctree:

   modlib
   migrate
   projects


"""

import os

execfile(os.path.join(os.path.dirname(__file__), 'setup_info.py'))

# doc_trees = ['docs_de', 'docs_fr', 'docs']
doc_trees = ['docs', 'docs_de', 'docs_fr']
intersphinx_urls = dict(docs="http://welfare.lino-framework.org")
intersphinx_urls.update(docs_de="http://de.welfare.lino-framework.org")
intersphinx_urls.update(docs_fr="http://fr.welfare.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino-welfare/blob/master/%s'
