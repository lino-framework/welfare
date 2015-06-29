# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is an early implementation still used in
:mod:`lino_welfare.projects.eupen`.  But it uses
:mod:`lino.modlib.properties` which is deprecated.
New installations should use
:mod:`lino_welfare.projects.chatelet.modlib.cv` instead.

"""

from lino.modlib.cv import Plugin


class Plugin(Plugin):

    ## settings
    person_model = 'pcsw.Client'

