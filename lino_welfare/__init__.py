# -*- coding: UTF-8 -*-
# Copyright 2002-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
This package defines functionality specific to :ref:`welfare`.

.. autosummary::
   :toctree:

   modlib
   migrate


"""

from .setup_info import SETUP_INFO

# doc_trees = ['docs', 'dedocs', 'frdocs']
# doc_trees = ['dedocs', 'frdocs']
doc_trees = ['docs']
intersphinx_urls = dict(docs="http://welfare.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/welfare/blob/master/%s'
