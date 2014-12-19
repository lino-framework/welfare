# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)


"""

The :mod:`lino_welfare.modlib.pcsw` package provides data definitions
for PCSW specific objects.

Most important models are :class:`Client` and :class:`Coaching`.

.. autosummary::
   :toctree:

   models
   coaching
   client_address
   fixtures

See also :mod:`welfare.pcsw`.

"""


from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "Ceci n'est pas une documentation."
    verbose_name = _("PCSW")

