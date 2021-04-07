# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Model mixins for `lino_welfare.modlib.dupable_clients`."""

from django.db.models import Q
from lino.mixins.dupable import Dupable
from lino.mixins.human import strip_name_prefix


class DupableClient(Dupable):
    """Model mixin to add to the base classes of your application's
    `pcsw.Client` model.

    """

    class Meta:
        abstract = True

    dupable_word_model = 'dupable_clients.Word'

    def get_dupable_words(self, s):
        s = strip_name_prefix(s)
        return super(DupableClient, self).get_dupable_words(s)

    def find_similar_instances(self, limit=None, **kwargs):
        """Overrides
        :meth:`lino.mixins.dupable.Dupable.find_similar_instances`,
        adding some additional rules.

        """
        if self.dupable_word_model is None:
            return
        # kwargs.update(is_obsolete=False, national_id__isnull=True)
        qs = super(DupableClient, self).find_similar_instances(None, **kwargs)
        if self.national_id:
            qs = qs.filter(national_id__isnull=True)
        # else:
        #     qs = qs.filter(national_id__isnull=False)
        if self.birth_date:
            qs = qs.filter(Q(birth_date='') | Q(birth_date=self.birth_date))

        last_name_words = set(self.get_dupable_words(self.last_name))

        found = 0
        for other in qs:
            found += 1
            if limit is not None and found > limit:
                return
            ok = False
            for w in other.get_dupable_words(other.last_name):
                if w in last_name_words:
                    ok = True
                    break
            if ok:
                yield other
        # if found == 2:
        #     msg = ', '.join(["{} {}".format(o.num, o) for o in qs])
        #     print("20200813 %s" % msg)
