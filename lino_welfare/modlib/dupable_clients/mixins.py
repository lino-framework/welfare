# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Model mixins for `lino_welfare.modlib.dupable_clients`."""

from django.db.models import Q
from lino.mixins.dupable import Dupable

from lino.api import _


class DupableClient(Dupable):
    """Model mixin to add to the base classes of your application's
    `pcsw.Client` model.

    Note that using the mixin does not yet install the plugin, it just
    declares a model as being dupable. In order to activate
    verification, you must also add
    :mod:`lino.modlib.dupable_clients` to your
    :meth:`get_installed_apps
    <lino.core.site.Site.get_installed_apps>` method.

    """

    class Meta:
        abstract = True

    dupable_word_model = 'dupable_clients.Word'

    def find_similar_instances(self, limit=None, **kwargs):
        # kwargs.update(is_obsolete=False, national_id__isnull=True)
        qs = super(DupableClient, self).find_similar_instances(None, **kwargs)
        if self.birth_date:
            qs = qs.filter(
                Q(birth_date__isnull=True) | Q(birth_date=self.birth_date))
        if limit is not None:
            qs = qs[:limit]
        # print qs.query
        return qs


