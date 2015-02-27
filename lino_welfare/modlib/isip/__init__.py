# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino_welfare.modlib.isip` package provides data definitions
for ISIPs (Individual Social Integration Projects, called "PIIS" in
French and "VSE" in German).

An ISIP is a convention or contract between the PCSW and a young
client that leads to an individual coaching of the person, mostly
concerning her scholar education.

Un **PIIS** (Project d'Insertion Sociale Personnalisé) est une
convention entre le CPAS et un jeune client qui engendra un
accompagnement individuel de la personne surtout au niveau
enseignement.

This module is also used and extended by
:mod:`lino_welfare.modlib.jobs` and
:mod:`lino_welfare.modlib.immersion`.

.. autosummary::
   :toctree:

   models
   mixins
   choicelists

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import ad


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("ISIP")
    needs_plugins = ['lino_welfare.modlib.integ']
