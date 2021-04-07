# -*- coding: UTF-8 -*-
# Copyright 2011-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""User interface definitions for this plugin.
"""

from lino.api import dd, _
from lino.utils import AttrDict
from lino.modlib.users.mixins import My
from .roles import CBSSUser, SecurityAdvisor
from .mixins import RequestStates
from .utils import (nodetext, cbss2gender, cbss2date, cbss2address,
                    cbss2civilstate)


class Sectors(dd.Table):
    model = 'cbss.Sector'
    required_roles = dd.login_required(CBSSUser, dd.SiteStaff)
    column_names = 'code subcode abbr name *'
    order_by = ['code', 'subcode']


class Purposes(dd.Table):
    model = 'cbss.Purpose'
    required_roles = dd.login_required(CBSSUser, dd.SiteStaff)
    column_names = 'sector_code code name *'
    order_by = ['sector_code', 'code']


class CBSSRequestDetail(dd.DetailLayout):
    main = 'request technical'

    request = dd.Panel("""
    info
    parameters
    result
    """, label=_("Request"))

    technical = dd.Panel("""
    environment ticket
    # response_xml
    info_messages
    debug_messages
    """, label=_("Technical"),
        required_roles=dd.login_required(CBSSUser, dd.SiteStaff))

    info = dd.Panel("""
    id person user sent status printed
    """, label=_("Request information"))


class CBSSRequests(dd.Table):
    column_names = "user person environment sent status ticket *"


class IdentifyPersonRequestDetail(CBSSRequestDetail):
    p1 = dd.Panel("""
    national_id
    spacer
    """, label=_("Using the national ID"))

    p2 = dd.Panel("""
    first_name middle_name last_name
    birth_date tolerance  gender
    """, label=_("Using phonetic search"))

    parameters = dd.Panel("p1 p2", label=_("Parameters"))

    # result = dd.Panel("IdentifyPersonResult", label=_("Result"))
    result = "IdentifyPersonResult"


class IdentifyPersonRequestInsert(dd.InsertLayout, IdentifyPersonRequestDetail):
    window_size = (60, 'auto')

    main = """
    person national_id
    p2
    """

    p2 = dd.Panel("""
    first_name middle_name last_name
    birth_date tolerance gender
    """, label=_("Phonetic search"))


class IdentifyPersonRequests(CBSSRequests):
    required_roles = dd.login_required(CBSSUser)
    model = 'cbss.IdentifyPersonRequest'
    active_fields = 'person'
    detail_layout = IdentifyPersonRequestDetail()
    insert_layout = IdentifyPersonRequestInsert()

    @dd.constant()
    def spacer(self):
        return '<br/>'


class AllIdentifyPersonRequests(IdentifyPersonRequests):
    required_roles = dd.login_required(dd.SiteStaff, CBSSUser)


class MyIdentifyPersonRequests(My, IdentifyPersonRequests):
    required_roles = dd.login_required(CBSSUser)


class IdentifyRequestsByPerson(IdentifyPersonRequests):
    required_roles = dd.login_required(CBSSUser)
    master_key = 'person'
    column_names = 'user sent status *'


class ConfidentialResultsTable(dd.VirtualTable):
    """Base class for virtual tables which show highly confidential data
    which must be visible only to the user who made the request (and
    to security advisors).

    """
    abstract = True
    label = _("Results")

    @classmethod
    def check_permission(cls, obj, ar):
        u = ar.user  # the real user, not the subst_user
        if obj.user != u:
            if not u.user_type.has_required_roles([SecurityAdvisor]):
                # print("20180926 {} {}".format(obj.user, u))
                raise Warning(
                    _("Confidential data"))
        

class IdentifyPersonResult(ConfidentialResultsTable):
    """
    Displays the response of an :class:`IdentifyPersonRequest`
    as a table.
    """
    master = 'cbss.IdentifyPersonRequest'
    master_key = None
    column_names = 'national_id:10 last_name:20 first_name:10 address birth_date:10 birth_location civil_state *'

    class Row(AttrDict):
        @classmethod
        def get_chooser_for_field(cls, fieldname):
            return None

    @classmethod
    def get_data_rows(self, ar):
        ipr = ar.master_instance
        if ipr is None:
            return
        if ipr.status not in (RequestStates.ok, RequestStates.warnings):
            return
        self.check_permission(ipr, ar)
        service_reply = ipr.get_service_reply()
        results = service_reply.childAtPath('/SearchResults').children
        if results is None:
            return
        for obj in results:
            data = dict()
            data.update(
                national_id=nodetext(
                    obj.childAtPath('/Basic/SocialSecurityUser')))
            data.update(
                last_name=nodetext(obj.childAtPath('/Basic/LastName')))
            data.update(
                first_name=nodetext(obj.childAtPath('/Basic/FirstName')))
            data.update(
                gender=cbss2gender(nodetext(obj.childAtPath('/Basic/Gender'))))
            data.update(
                birth_date=cbss2date(nodetext(
                    obj.childAtPath('/Basic/BirthDate'))))
            data.update(civil_state=cbss2civilstate(
                obj.childAtPath('/Extended/CivilState')))
            data.update(
                birth_location=nodetext(
                    obj.childAtPath('/Extended/BirthLocation')))
            data.update(cbss2address(obj))
            yield self.Row(**data)

    @dd.displayfield(_("National ID"))
    def national_id(self, obj, ar):
        return obj.national_id

    @dd.displayfield(_("Last name"))
    def last_name(self, obj, ar):
        return obj.last_name

    @dd.displayfield(_("First name"))
    def first_name(self, obj, ar):
        return obj.first_name

    @dd.virtualfield(dd.Genders.field())
    def gender(self, obj, ar):
        return obj.gender

    @dd.displayfield(_("Birth date"))
    def birth_date(self, obj, ar):
        return obj.birth_date

    @dd.displayfield(_("Birth location"))
    def birth_location(self, obj, ar):
        return obj.birth_location

    @dd.displayfield(_("Civil state"))
    def civil_state(self, obj, ar):
        return obj.civil_state

    @dd.displayfield(_("Address"))
    def address(self, obj, ar):
        return obj.address


class ManageAccessRequestDetail(CBSSRequestDetail):

    p1 = dd.Panel("""
    action start_date end_date
    purpose query_register
    """, label=_("Requested action"))

    proof = dd.Panel("""
    national_id sis_card_no id_card_no
    first_name last_name birth_date
    """, label=_("Proof of authentication"))
    parameters = dd.Panel("p1 proof", label=_("Parameters"))

    # def setup_handle(self,lh):
    #     lh.p1.label = _("Requested action")
    #     lh.proof.label = _("Proof of authentication")
    #     CBSSRequestDetail.setup_handle(self,lh)


class ManageAccessRequestInsert(dd.InsertLayout):
    window_size = (60, 'auto')

    p1 = dd.Panel("""
    action start_date end_date
    purpose query_register
    """, label=_("Requested action"))

    proof = dd.Panel("""
    national_id sis_card_no id_card_no
    first_name last_name birth_date
    """, label=_("Proof of authentication"))

    main = """
    person
    p1
    proof
    """

    # def setup_handle(self,lh):
    #     lh.p1.label = _("Requested action")
    #     lh.proof.label = _("Proof of authentication")
    #     super(ManageAccessRequestInsert,self).setup_handle(lh)


class ManageAccessRequests(CBSSRequests):
    required_roles = dd.login_required(CBSSUser)
    model = 'cbss.ManageAccessRequest'
    detail_layout = ManageAccessRequestDetail()
    insert_layout = ManageAccessRequestInsert()
    active_fields = 'person'


class AllManageAccessRequests(ManageAccessRequests):
    required_roles = dd.login_required(dd.SiteStaff, CBSSUser)


class ManageAccessRequestsByPerson(ManageAccessRequests):
    master_key = 'person'


class MyManageAccessRequests(My, ManageAccessRequests):
    required_roles = dd.login_required(CBSSUser)


class RetrieveTIGroupsRequestDetail(CBSSRequestDetail):

    parameters = dd.Panel("national_id language history",
                          label=_("Parameters"))

    result = "cbss.RetrieveTIGroupsResult"

    # def setup_handle(self,lh):
        # CBSSRequestDetail.setup_handle(self,lh)


class RetrieveTIGroupsRequests(CBSSRequests):
    # debug_permissions = True
    required_roles = dd.login_required(CBSSUser)
    model = 'cbss.RetrieveTIGroupsRequest'
    detail_layout = RetrieveTIGroupsRequestDetail()
    insert_layout = dd.InsertLayout("""
    person
    national_id language
    history
    """, window_size=(40, 'auto'))
    # insert_layout = RetrieveTIGroupsRequestInsert(window_size=(400,'auto'))


class AllRetrieveTIGroupsRequests(RetrieveTIGroupsRequests):
    required_roles = dd.login_required(dd.SiteStaff, CBSSUser)


class RetrieveTIGroupsRequestsByPerson(RetrieveTIGroupsRequests):
    master_key = 'person'


class MyRetrieveTIGroupsRequests(My, RetrieveTIGroupsRequests):
    required_roles = dd.login_required(CBSSUser)


from .tx25 import RetrieveTIGroupsResult
