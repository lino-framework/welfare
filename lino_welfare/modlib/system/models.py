# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""

"""

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _

from lino.api import dd, rt

from lino.modlib.system.models import *
from lino_welfare.modlib.cbss.roles import CBSSUser


class Signers(dd.Model):

    """Model mixin which adds two fields `signer1` and `signer2`,
    the two in-house signers of contracts and official documents.

    Inherited by :class:`SiteConfig
    <lino.modlib.system.models.SiteConfig>` and :class:`ContractBase`.

    """

    class Meta:
        abstract = True

    signer1 = dd.ForeignKey(
        "contacts.Person",
        related_name="%(app_label)s_%(class)s_set_by_signer1",
        #~ default=default_signer1,
        verbose_name=_("Secretary"))

    signer2 = dd.ForeignKey(
        "contacts.Person",
        related_name="%(app_label)s_%(class)s_set_by_signer2",
        #~ default=default_signer2,
        verbose_name=_("President"))

    @dd.chooser()
    def signer1_choices(cls):
        sc = settings.SITE.site_config
        kw = dict()
        if sc.signer1_function:
            kw.update(rolesbyperson__type=sc.signer1_function)
        return settings.SITE.models.contacts.Person.objects.filter(
            rolesbyperson__company=sc.site_company, **kw)

    @dd.chooser()
    def signer2_choices(cls):
        sc = settings.SITE.site_config
        kw = dict()
        if sc.signer2_function:
            kw.update(rolesbyperson__type=sc.signer2_function)
        return settings.SITE.models.contacts.Person.objects.filter(
            rolesbyperson__company=sc.site_company, **kw)


class SiteConfig(SiteConfig, Signers):

    """
    This adds the :class:`lino_welfare.modlib.isip.models.Signers`
    mixin to Lino's standard SiteConfig.

    """

    class Meta(SiteConfig.Meta):
        abstract = dd.is_abstract_model(__name__, 'SiteConfig')


    signer1_function = dd.ForeignKey(
        "contacts.RoleType",
        blank=True, null=True,
        verbose_name=_("First signer function"),
        help_text=_("""Contact function to designate the secretary."""),
        related_name="%(app_label)s_%(class)s_set_by_signer1")
    signer2_function = dd.ForeignKey(
        "contacts.RoleType",
        blank=True, null=True,
        verbose_name=_("Second signer function"),
        help_text=_(
            "Contact function to designate the president."),
        related_name="%(app_label)s_%(class)s_set_by_signer2")


dd.update_field(SiteConfig, 'signer1', blank=True, null=True)
dd.update_field(SiteConfig, 'signer2', blank=True, null=True)


class SiteConfigDetail(dd.DetailLayout):

    main = "general constants cbss"

    # window_size = (80, 'auto')  ExtJS does not support auto height on tabbed details

    general = dd.Panel(
        """
        site_company next_partner_id:10
        job_office master_budget
        signer1 signer2
        signer1_function signer2_function
        """, label=_("General"))

    constants = dd.Panel(
        """
        system_note_type default_build_method
        propgroup_skills propgroup_softskills propgroup_obstacles
        residence_permit_upload_type \
        work_permit_upload_type \
        driving_licence_upload_type
        # client_calendar
        default_event_type prompt_calendar hide_events_before
        client_guestrole team_guestrole
        """, label=_("Constants"))

    cbss = dd.Panel(
        """
        cbss_org_unit sector ssdn_user_id ssdn_email
        cbss_http_username cbss_http_password
        """,
        label=dd.plugins.cbss.verbose_name,
        required_roles=dd.login_required(CBSSUser))


# When a Welfare Site decides to hide the "debts" app (as chatelet does)
# then we must remove the `master_budget` field.
# TODO: find a more elegant way to do this.
if not dd.is_installed('debts'):
    SiteConfigDetail.general.replace('master_budget', '')


class SiteConfigs(SiteConfigs):
    detail_layout = SiteConfigDetail()
