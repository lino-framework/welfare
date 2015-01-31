# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)


"""The :xfile:`models.py` module for `lino_welfare.modlib.trainings`.

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino import mixins

from lino.modlib.cv.mixins import SectorFunction
from lino_welfare.modlib.isip.mixins import (
    ContractTypeBase, ContractBase, ContractPartnerBase, ContractBaseTable)

isip = dd.resolve_app('isip')


class TrainingType(ContractTypeBase):

    templates_group = 'trainings/Training'

    class Meta:
        verbose_name = _("Immersion training type")
        verbose_name_plural = _('Immersion training types')
        ordering = ['name']


class TrainingTypes(dd.Table):
    """
    """
    required = dd.required(user_groups='integ', user_level='manager')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = 'trainings.TrainingType'
    column_names = 'name *'
    detail_layout = """
    id name exam_policy
    TrainingsByType
    """
    insert_layout = """
    name
    exam_policy
    """


class Goal(mixins.BabelNamed):

    preferred_foreignkey_width = 20

    class Meta:
        verbose_name = _("Training goal")
        verbose_name_plural = _('Training goals')
        ordering = ['name']


class TrainingGoals(dd.Table):
    """
    """
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'trainings.Goal'
    column_names = 'name *'
    detail_layout = """
    id name
    TrainingsByGoal
    """


class Training(ContractBase, ContractPartnerBase, SectorFunction):
    """An immersion training.

    """

    class Meta:
        verbose_name = _("Immersion training")
        verbose_name_plural = _('Immersion trainings')

    type = dd.ForeignKey(
        "trainings.TrainingType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        blank=True)

    goal = dd.ForeignKey(
        "trainings.Goal", related_name="trainings", blank=True)

    reference_person = models.CharField(
        _("reference person"), max_length=200, blank=True)
    responsibilities = dd.RichTextField(
        _("responsibilities"), blank=True, null=True, format='html')
    remark = models.TextField(_("Remark"), blank=True)

    @dd.chooser()
    def company_choices(cls):
        return rt.modules.jobs.JobProvider.objects.all()

    @classmethod
    def get_certifiable_fields(cls):
        return (
            'client company contact_person contact_role type '
            'applies_from applies_until '
            'language  '
            'reference_person responsibilities '
            'user user_asd exam_policy '
            'date_decided date_issued ')


dd.update_field(Training, 'user', verbose_name=_("responsible (IS)"))


class TrainingDetail(dd.FormLayout):
    box1 = """
    id:8 client:25 user:15 user_asd:15 language:8
    type company contact_person contact_role
    applies_from applies_until exam_policy
    sector function
    reference_person printed
    date_decided date_issued date_ended ending:20
    responsibilities
    """

    right = """
    cal.EventsByController
    cal.TasksByController
    """

    main = """
    box1:70 right:30
    """


class Trainings(ContractBaseTable):

    required = dd.required(user_groups='integ')
    model = Training
    column_names = 'id client applies_from applies_until user type *'
    order_by = ['id']
    detail_layout = TrainingDetail()
    insert_layout = """
    client
    company
    """

    parameters = dict(
        type=models.ForeignKey(
            'trainings.TrainingType', blank=True,
            verbose_name=_("Only trainings of type")),
        **isip.ContractBaseTable.parameters)

    params_layout = """
    user type start_date end_date observed_event
    company ending_success ending
    """

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Trainings, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.company:
            qs = qs.filter(company=pv.company)
        return qs


class TrainingsByClient(Trainings):
    """
    """
    master_key = 'client'
    auto_fit_column_widths = True
    column_names = 'applies_from applies_until user type *'


class TrainingsByProvider(Trainings):
    master_key = 'company'
    column_names = 'client applies_from applies_until user type *'


class TrainingsByPolicy(Trainings):
    master_key = 'exam_policy'


class TrainingsByType(Trainings):
    master_key = 'type'
    column_names = "applies_from client user *"
    order_by = ["applies_from"]


class TrainingsByGoal(Trainings):
    master_key = 'goal'
    column_names = "applies_from client user *"
    order_by = ["applies_from"]


class TrainingsByEnding(Trainings):
    master_key = 'ending'



class MyTrainings(Trainings):
    column_names = "applies_from client type company applies_until date_ended ending *"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyTrainings, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


