# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
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

"""The :mod:`lino_welfare.modlib.jobs` package provides data
definitions for managing so-called job supply projects.

    A job supply project is when the PCSW arranges a job for a client,
    with the aim to bring this person back into the social security
    system and the employment process. In most cases, the PSWC acts as
    the legal employer.  It can employ the person in its own services
    (internal contracts) or put him/her at the disposal of a third
    party employer (external contracts).

    (Adapted from `mi-is.be
    <http://www.mi-is.be/en/public-social-welfare-centers/article-60-7>`_).

This module is technically similar to :mod:`ISIP <isip>` which it
extends.

.. autosummary::
   :toctree:

   models
   mixins
   fixtures.std

"""

from __future__ import unicode_literals

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    # verbose_name = _("Art.60§7")
    verbose_name = _("Job supplying")  # Mise à l'emploi
    needs_plugins = ['lino_welfare.modlib.isip']

