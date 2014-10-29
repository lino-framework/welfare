# -*- coding: UTF-8 -*-
# Copyright 2002-2014 Luc Saffre
# License: BSD (see file COPYING for details)

import os

execfile(os.path.join(os.path.dirname(__file__), 'setup_info.py'))
__version__ = SETUP_INFO['version']

doc_trees = ['docs_de', 'docs_fr', 'docs']
intersphinx_urls = dict(docs="http://welfare.lino-framework.org")
intersphinx_urls.update(docs_de="http://de.welfare.lino-framework.org")
intersphinx_urls.update(docs_fr="http://fr.welfare.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino-welfare/blob/master/%s'
