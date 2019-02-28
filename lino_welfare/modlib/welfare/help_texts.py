# -*- coding: UTF-8 -*-
# generated by lino.sphinxcontrib.help_text_builder
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

help_texts = {
    'lino_welfare.migrate.Migrator' : _("""The standard migrator for welfare."""),
    'lino_welfare.modlib.aids.Plugin' : _("""The plugin."""),
    'lino_welfare.modlib.aids.Plugin.no_date_range_veto_until' : _("""Optionally specify the primary key (an integer) of the last
granting for whose confirmations you want to suppress checking of
date range.  This is useful for keeping legacy confirmations that
have been issued before the rule was activated."""),
    'lino_welfare.modlib.aids.ConfirmationTypes' : _("""A list of the models that may be used as confirmation."""),
    'lino_welfare.modlib.aids.ConfirmationTypes.et_template' : _("""The template defined for the ExcerptType defined for this
confirmation type."""),
    'lino_welfare.modlib.art61.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.badges.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.badges.Plugin.holder_model' : _("""A string referring to the model which represents the badge holder in
your application.  Default value is 'contacts.Person'."""),
    'lino_welfare.modlib.cal.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.cbss.Plugin' : _("""The descriptor for this plugin. See
lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.cbss.Plugin.cbss_live_requests' : _("""Whether executing requests should try to really connect to the
CBSS.  Real requests would fail with a timeout if run from behind
an IP address that is not registered at the CBSS."""),
    'lino_welfare.modlib.cbss.Plugin.cbss_environment' : _("""Either None or one of 'test', 'acpt' or 'prod'."""),
    'lino_welfare.modlib.cbss.RequestStates' : _("""The status of a CBSSRequest."""),
    'lino_welfare.modlib.cbss.ManageActions' : _("""Possible values for the action field of a
lino_welfare.modlib.cbss.models.ManageAccessRequest."""),
    'lino_welfare.modlib.cbss.ManageActions.REGISTER' : _("""Ce service est sollicité au moment du démarrage de l’enquête
sociale.  Le CPAS déclare au réseau de la sécurité sociale qu’il
possède un dossier pour lequel il a l’autorisation (dispositions
légales et réglementaires) d’obtenir des informations des autres
institutions en vue de compléter son enquête dans le cadre de
l’octroi du revenu d’intégration.  Cette déclaration concerne le
répertoire sectoriel des CPAS à la SmalS-MvM et peut concerner
plusieurs catégories de personnes : le demandeur, les
cohabitants et les tiers concernés et ce, pour des finalités
différentes."""),
    'lino_welfare.modlib.cbss.ManageActions.UNREGISTER' : _("""L’opération contraire est aussi mise à disposition."""),
    'lino_welfare.modlib.cbss.ManageActions.LIST' : _("""Il est en plus possible d’obtenir une liste des enregistrements
dans le répertoire sectoriel des CPAS à la SmalS-MvM ainsi qu’au
sein du réseau BCSS."""),
    'lino_welfare.modlib.cbss.QueryRegisters' : _("""Possible values for the query_register field of a
lino_welfare.modlib.cbss.models.ManageAccessRequest."""),
    'lino_welfare.modlib.cbss.QueryRegisters.PRIMARY' : _("""Query only the primary register."""),
    'lino_welfare.modlib.cbss.QueryRegisters.SECONDARY' : _("""Query only the secondary register."""),
    'lino_welfare.modlib.cbss.QueryRegisters.ALL' : _("""Query both registers."""),
    'lino_welfare.modlib.cbss.CBSSRequest' : _("""Common Abstract Base Class for SSDNRequest
and NewStyleRequest"""),
    'lino_welfare.modlib.cbss.CBSSRequest.wsdl_parts' : _("""alias of exceptions.NotImplementedError"""),
    'lino_welfare.modlib.cbss.CBSSRequest.on_duplicate' : _("""When duplicating a CBSS request, we want re-execute it.  So please
duplicate only the parameters, not the execution data like
ticket, sent and status.  Note that also the user will
be set to the user who asked to duplicate (because this is a
subclass of UserAuthored."""),
    'lino_welfare.modlib.cbss.CBSSRequest.get_row_permission' : _("""CBSS requests that have a ticket may never be modified."""),
    'lino_welfare.modlib.cbss.CBSSRequest.on_cbss_ok' : _("""Called when a successful reply has been received."""),
    'lino_welfare.modlib.cbss.CBSSRequest.execute_request' : _("""This is the common part of a request for both classic and
new-style."""),
    'lino_welfare.modlib.cbss.CBSSRequest.get_excerpt_options' : _("""When we print a request, the resulting excerpt should go to the
client's history."""),
    'lino_welfare.modlib.cbss.SSDNRequest' : _("""Abstract Base Class for Models that represent SSDN ("classic")
requests."""),
    'lino_welfare.modlib.cbss.SSDNRequest.validate_request' : _("""Validates the generated XML against the XSD files.
Used by test suite.
It is not necessary to validate each real request before actually sending it."""),
    'lino_welfare.modlib.cbss.SSDNRequest.execute_request_' : _("""SSDN specific part of a request."""),
    'lino_welfare.modlib.cbss.SSDNRequest.wrap_ssdn_request' : _("""Wrap the given service request into the SSDN envelope 
by adding AuthorizedUser and other information common 
the all SSDN requests)."""),
    'lino_welfare.modlib.cbss.NewStyleRequest' : _("""Abstract Base Class for Models that represent
"new style" requests to the CBSS (and responses)."""),
    'lino_welfare.modlib.cbss.NewStyleRequest.execute_request_' : _("""NewStyle specific part of a request."""),
    'lino_welfare.modlib.cbss.NewStyleRequest.on_cbss_ok' : _("""Called when a successful reply has been received."""),
    'lino_welfare.modlib.cbss.SSIN' : _("""Abstract base for Requests that have a field national_id and a method 
get_ssin()."""),
    'lino_welfare.modlib.cbss.WithPerson' : _("""Mixin for models that have certain fields"""),
    'lino_welfare.modlib.client_vouchers.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.client_vouchers.VoucherItem' : _("""An item of an ClientVoucher."""),
    'lino_welfare.modlib.client_vouchers.ClientVouchersByJournal' : _("""Shows all simple invoices of a given journal (whose
Journal.voucher_type must be
lino_xl.lib.sales.models.ClientVoucher)."""),
    'lino_welfare.modlib.debts.fields.PeriodsField' : _("""Used for Entry.periods and Account.periods
(the latter holds simply the default value for the former).
It means: for how many months the entered amount counts.
Default value is 1. For yearly amounts set it to 12."""),
    'lino_welfare.modlib.debts.ActorBase' : _("""Base class for both the volatile MainActor and the
Actor model."""),
    'lino_welfare.modlib.debts.MainActor' : _("""A volatile object that represents the budget partner as actor"""),
    'lino_welfare.modlib.dupable_clients.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.dupable_clients.DupableClient' : _("""Model mixin to add to the base classes of your application's
pcsw.Client model."""),
    'lino_welfare.modlib.dupable_clients.DupableClient.find_similar_instances' : _("""Overrides
lino.mixins.dupable.Dupable.find_similar_instances(),
adding some additional rules."""),
    'lino_welfare.modlib.esf.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.immersion.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.integ.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.integ.Plugin.only_primary' : _("""Whether to show only primary coachings in the dynamic ventilation
columns (coachings per PersonGroup table."""),
    'lino_welfare.modlib.integ.roles.IntegUser' : _("""Has access to data used by integration agents."""),
    'lino_welfare.modlib.integ.roles.IntegrationStaff' : _("""Can configure social integration functionality."""),
    'lino_welfare.modlib.isip.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.isip.OverlapGroups' : _("""The list of all known overlap groups to be selected for the
overlap_group
of a contract type."""),
    'lino_welfare.modlib.jobs.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.ledger.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.pcsw.Plugin' : _("""See lino.core.plugin.Plugin."""),
    'lino_welfare.modlib.pcsw.RefuseClient' : _("""Refuse this newcomer request."""),
    'lino_welfare.modlib.pcsw.MarkClientFormer' : _("""Change client's state to 'former'. This will also end any active
coachings."""),
    'lino_welfare.modlib.pcsw.roles.SocialCoordinator' : _("""Has limited access to data of social workers. Can see contracts."""),
    'lino_welfare.modlib.pcsw.roles.SocialUser' : _("""Can access data managed by general social workers."""),
    'lino_welfare.modlib.pcsw.roles.SocialStaff' : _("""Can configure general social work functionality."""),
    'lino_welfare.modlib.xcourses.roles.CoursesUser' : _("""Can manage external courses."""),
    'lino_welfare.modlib.xcourses.roles.CoursesStaff' : _("""Can manage and configure external courses."""),
    'lino_welfare.modlib.aids.AidType' : _("""The Django model representing an aid type."""),
    'lino_welfare.modlib.aids.AidType.short_name' : _("""The short name for internal use, e.g. when a user must select
an aid type from a combobox."""),
    'lino_welfare.modlib.aids.AidType.confirmation_type' : _("""The database model to use for issuing an aid confirmation of
this type. This is a mandatory pointer to
ConfirmationTypes."""),
    'lino_welfare.modlib.aids.AidType.name' : _("""The designation of this aid type as seen by the user e.g. when
selecting an aid type."""),
    'lino_welfare.modlib.aids.AidType.excerpt_title' : _("""The text to print as title in confirmations.
See also
lino_xl.lib.excerpts.mixins.ExcerptTitle.excerpt_title."""),
    'lino_welfare.modlib.aids.AidType.body_template' : _("""The body template to use when printing a confirmation of this type.
If this field is empty, Lino uses the excerpt type's
body_template.
See also /admin/printing."""),
    'lino_welfare.modlib.aids.AidType.is_urgent' : _("""Whether aid grantings of this type are considered as urgent.
This is used by Confirmation.get_urgent_granting()"""),
    'lino_welfare.modlib.aids.AidType.board' : _("""Pointer to the default lino_xl.lib.boards.models.Board
for aid projects of this type."""),
    'lino_welfare.modlib.aids.AidType.confirmed_by_primary_coach' : _("""Whether grantings for this aid type are to be signed by the
client's primary coach (see Client.get_primary_coach)."""),
    'lino_welfare.modlib.aids.AidType.pharmacy_type' : _("""A pointer to the ClientContactType to be used when
selecting the pharmacy of a refund confirmation
(RefundConfirmation.pharmacy)."""),
    'lino_welfare.modlib.aids.Granting' : _("""The Django model representing an aid granting."""),
    'lino_welfare.modlib.aids.Granting.client' : _("""Pointer to the lino_welfare.modlib.pcsw.models.Client."""),
    'lino_welfare.modlib.aids.Granting.aid_type' : _("""The type of aid being granted. Mandatory.
Pointer to the AidType."""),
    'lino_welfare.modlib.aids.Granting.signer' : _("""Pointer to the user who is expected to "sign" this granting
(i.e. to confirm that it is real)."""),
    'lino_welfare.modlib.aids.Granting.board' : _("""Pointer to the Board
which decided to allocate this aid project."""),
    'lino_welfare.modlib.aids.Granting.category' : _("""Currently only used for printing an isip.Contract."""),
    'lino_welfare.modlib.aids.Confirmation' : _("""Base class for all aid confirmations."""),
    'lino_welfare.modlib.aids.Confirmation.get_date_range_veto' : _("""Return an error message if this confirmation lies outside of
granted period."""),
    'lino_welfare.modlib.aids.Confirmable' : _("""Base class for both Granting and Confirmation."""),
    'lino_welfare.modlib.aids.Confirmable.state' : _("""The confirmation state of this object. Pointer to
ConfirmationStates."""),
    'lino_welfare.modlib.aids.Confirmable.sign' : _("""Sign this granting or confirmation, making most fields read-only."""),
    'lino_welfare.modlib.aids.Confirmable.revoke' : _("""Revoke your signature of this granting or confirmation."""),
    'lino_welfare.modlib.art61.Contract' : _("""The Django database model."""),
    'lino_welfare.modlib.art61.Contract.get_subsidizations' : _("""Yield a list of all subsidizations activated for this
contract."""),
    'lino_welfare.modlib.art61.ContractsByClient' : _("""Shows the Art61 job supplyments for this client."""),
    'lino_welfare.modlib.cal.EventType' : _("""Adds two fields."""),
    'lino_welfare.modlib.cal.Guest' : _("""Adds a virtual field client."""),
    'lino_welfare.modlib.cal.Guest.client' : _("""Virtual field which returns the partner if it is a client."""),
    'lino_welfare.modlib.cbss.Sector' : _("""Default values filled from
lino_welfare.modlib.cbss.fixtures.sectors."""),
    'lino_welfare.modlib.cbss.Purpose' : _("""Codes qualité (Hoedanigheidscodes).
This table is usually filled with the official codes
by lino_welfare.modlib.cbss.fixtures.purposes."""),
    'lino_welfare.modlib.cbss.IdentifyPersonRequest' : _("""A request to the IdentifyPerson service."""),
    'lino_welfare.modlib.cbss.ManageAccessRequest' : _("""A request to the ManageAccess service."""),
    'lino_welfare.modlib.cbss.ManageAccessRequest.sector' : _("""Pointer to Sector."""),
    'lino_welfare.modlib.cbss.ManageAccessRequest.purpose' : _("""Pointer to Purpose."""),
    'lino_welfare.modlib.cbss.ManageAccessRequest.action' : _("""The action to perform.  This must be one of the values in
lino_welfare.modlib.cbss.choicelists.ManageActions"""),
    'lino_welfare.modlib.cbss.ManageAccessRequest.query_register' : _("""The register to be query.
This must be one of the values in
lino_welfare.modlib.cbss.choicelists.QueryRegisters"""),
    'lino_welfare.modlib.cbss.RetrieveTIGroupsRequest' : _("""A request to the RetrieveTIGroups service (aka Tx25)"""),
    'lino_welfare.modlib.debts.Account' : _("""An account is an item of an account chart used to collect
ledger transactions or other accountable items."""),
    'lino_welfare.modlib.debts.Account.name' : _("""The multilingual designation of this account, as the users see
it."""),
    'lino_welfare.modlib.debts.Account.group' : _("""The account group to which this account belongs.  This must
point to an instance of Group."""),
    'lino_welfare.modlib.debts.Account.seqno' : _("""The sequence number of this account within its group."""),
    'lino_welfare.modlib.debts.Account.ref' : _("""An optional unique name which can be used to reference a given
account."""),
    'lino_welfare.modlib.debts.Account.type' : _("""The account type of this account.  This must
point to an item of
lino_welfare.modlib.debts.AccountTypes."""),
    'lino_welfare.modlib.debts.Budget' : _("""A document which expresses the financial situation of a partner at
a given date."""),
    'lino_welfare.modlib.debts.Actor' : _("""An actor of a budget is a partner who is part of the household
for which the budget has been established."""),
    'lino_welfare.modlib.debts.Entry' : _("""A detail row of a Budget."""),
    'lino_welfare.modlib.debts.Entry.amount' : _("""The amount of money. An empty amount is different from a zero
amount in that the latter will be printed while the former
not."""),
    'lino_welfare.modlib.debts.Entry.account' : _("""The related Account."""),
    'lino_welfare.modlib.pcsw.Client' : _("""Inherits from lino_welfare.modlib.contacts.Person and
lino_xl.lib.beid.BeIdCardHolder."""),
    'lino_welfare.modlib.pcsw.Client.has_esf' : _("""Whether Lino should make ESF summaries for this client."""),
    'lino_welfare.modlib.pcsw.Client.overview' : _("""A panel with general information about this client."""),
    'lino_welfare.modlib.pcsw.Client.cvs_emitted' : _("""A virtual field displaying a group of shortcut links for managing CVs
(Curriculum Vitaes)."""),
    'lino_welfare.modlib.pcsw.Client.id_document' : _("""A virtual field displaying a group of buttons for managing the
"identifying document", i.e. an uploaded document which has been
used as alternative to the eID card."""),
    'lino_welfare.modlib.pcsw.Client.group' : _("""Pointer to PersonGroup.
The intergration phase of this client."""),
    'lino_welfare.modlib.pcsw.Client.civil_state' : _("""The civil state of this client. Allowed choices are defined in
CivilState."""),
    'lino_welfare.modlib.pcsw.Client.client_state' : _("""Pointer to ClientStates."""),
    'lino_welfare.modlib.pcsw.Client.unemployed_since' : _("""The date when this client got unemployed and stopped to have a
regular work."""),
    'lino_welfare.modlib.pcsw.Client.seeking_since' : _("""The date when this client registered as unemployed and started
to look for a new job."""),
    'lino_welfare.modlib.pcsw.Client.get_first_meeting' : _("""Return the last note of type "First meeting" for this client.
Usage example see debts and
notes."""),
    'lino_welfare.modlib.pcsw.Clients' : _("""The list that opens by Contacts ‣ Clients."""),
    'lino_welfare.modlib.pcsw.Clients.client_state' : _("""If not empty, show only Clients whose client_state equals
the specified value."""),
    'lino_welfare.modlib.cbss.tx25.RetrieveTIGroupsResult' : _("""Displays the response of an RetrieveTIGroupsRequest
as a table."""),
}
