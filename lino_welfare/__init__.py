# -*- coding: UTF-8 -*-
# Copyright 2002-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
This package defines functionality specific to :ref:`welfare`.

.. autosummary::
   :toctree:

   modlib
   migrate


"""

import os

fn = os.path.join(os.path.dirname(__file__), 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))

# doc_trees = ['docs', 'dedocs', 'frdocs']
# doc_trees = ['dedocs', 'frdocs']
doc_trees = ['docs']
intersphinx_urls = dict(docs="http://welfare.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/welfare/blob/master/%s'
