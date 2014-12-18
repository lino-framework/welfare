# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

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
    # verbose_name = _("Art.60§7")
    verbose_name = _("Job supply")
