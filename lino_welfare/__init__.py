# -*- coding: UTF-8 -*-
# Copyright 2002-2014 Luc Saffre
# License: BSD (see file COPYING for details)

import os

execfile(os.path.join(os.path.dirname(__file__), 'setup_info.py'))
__version__ = SETUP_INFO['version']

intersphinx_url = "http://welfare.lino-framework.org"
intersphinx_url_userdocs = "http://welfare-user.lino-framework.org"
srcref_url = 'https://github.com/lsaffre/lino-welfare/blob/master/%s'
