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

    """

    class Meta:
        abstract = True

    dupable_word_model = 'dupable_clients.Word'

    def find_similar_instances(self, limit=None, **kwargs):
        """Overrides
        :meth:`lino.mixins.dupable.Dupable.find_similar_instances`,
        adding some additional rules:

        

        """
        # kwargs.update(is_obsolete=False, national_id__isnull=True)
        qs = super(DupableClient, self).find_similar_instances(None, **kwargs)
        if self.national_id:
            qs = qs.filter(national_id__isnull=True)
        else:
            qs = qs.filter(national_id__isnull=False)
        if self.birth_date:
            qs = qs.filter(Q(birth_date='') | Q(birth_date=self.birth_date))
        if limit is not None:
            qs = qs[:limit]
        # print qs.query
        return qs


