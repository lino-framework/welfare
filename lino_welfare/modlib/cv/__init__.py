# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This is an early implementation still used in
:mod:`lino_welfare.projects.eupen`.  But it uses
:mod:`lino_xl.lib.properties` which is deprecated.
New installations should use
:mod:`lino_welfare.chatelet.lib.cv` instead.

"""

from lino_xl.lib.cv import Plugin


class Plugin(Plugin):

    ## settings
    person_model = 'pcsw.Client'

