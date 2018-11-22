# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Rumma & Ko Ltd
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

"""
Database models for `lino_welfare.modlib.dupable_clients`.
"""
from builtins import str
from lino.api import dd, _

from lino.mixins.dupable import PhoneticWordBase, SimilarObjects


class Word(PhoneticWordBase):
    """Phonetic word for `pcsw.Client`.
    See :class:`lino.mixins.dupable.PhoneticWordBase`.
    """

    class Meta:
        verbose_name = _("Phonetic word")
        verbose_name_plural = _("Phonetic words")

    owner = dd.ForeignKey('pcsw.Client', related_name='dupable_words')


class Words(dd.Table):
    model = 'dupable_clients.Word'
    required_roles = dd.login_required(dd.SiteAdmin)


class WordsByOwner(Words):
    required_roles = dd.login_required()
    master_key = 'owner'
    column_names = "word"


class SimilarClients(SimilarObjects):
    """Shows the other clients who are similar to this one."""
    label = _("Similar clients")

from lino_welfare.modlib.pcsw.models import ClientChecker

# dd.inject_action('pcsw.Client', show_phonetic_words=dd.ShowSlaveTable(
#     WordsByOwner))


class SimilarClientsChecker(ClientChecker):
    """If several clients have similar names, their coach should fill at
    least their `birth_date` and `national_id` to assert their
    identity.

    """
    verbose_name = _("Check for similar clients")

    def get_checkdata_problems(self, obj, fix=False):
        lst = list(obj.find_similar_instances(1))
        if len(lst):
            msg = _("Similar clients: {clients}").format(
                clients=', '.join([str(i) for i in lst]))
            yield (False, msg)

SimilarClientsChecker.activate()
