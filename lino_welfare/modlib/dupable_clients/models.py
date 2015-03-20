# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino_welfare.modlib.dupable_clients`.
"""

from lino.api import dd, _

from lino.mixins.dupable import DupableWordBase, SimilarObjects


class Word(DupableWordBase):
    """Phonetic words for Clients."""

    class Meta:
        verbose_name = _("Phonetic word")
        verbose_name_plural = _("Phonetic words")

    owner = dd.ForeignKey('pcsw.Client', related_name='dupable_words')


class Words(dd.Table):
    model = 'dupable_clients.Word'
    required = dd.Required(user_level='admin')


class SimilarClients(SimilarObjects):
    """Shows the other clients who are similar to this one."""
    label = _("Similar clients")

from lino_welfare.modlib.pcsw.models import ClientChecker


class SimilarClientsChecker(ClientChecker):
    """If several clients have similar names, their coach should fill at
    least their `birth_date` and `national_id` to assert their
    identity.

    """
    verbose_name = _("Check for similar clients")

    def get_checker_problems(self, obj):
        qs = obj.find_similar_instances(3)
        if qs.count() > 0:
            yield _("{num} similar clients: {clients}").format(
                num=qs.count(),
                clients=', '.join(map(unicode, qs)))


SimilarClientsChecker.activate()
