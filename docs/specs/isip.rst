.. doctest docs/specs/isip.rst
.. _welfare.specs.isip:

=================================================
``isip`` : Individual Social Integration Projects
=================================================

.. currentmodule:: lino_welfare.modlib.isip

The :mod:`lino_welfare.modlib.isip` package provides data definitions for
Individual Social Integration Projects (ISIPs).

.. contents::
   :local:

.. include:: /shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *
>>> ses = rt.login('robin')
>>> translation.activate('en')


Overview
========

This module is also used and extended by
:mod:`lino_welfare.modlib.jobs` and
:mod:`lino_welfare.modlib.immersion`,
:mod:`lino_welfare.modlib.art61`.
See also :doc:`autoevents`.

An **ISIP** (called "PIIS" in French and "VSE" in German) is a
convention or contract between the PCSW and a young client that
leads to an individual coaching of the person, mostly concerning
the client's scholar education.



Contracts
=========

.. class:: ContractBase

    Abstract base class for all *integration contracts*, i.e.
    :class:`isip.Contract <lino_welfare.modlib.isip.Contract>`
    :class:`jobs.Contract <lino_welfare.modlib.jobs.Contract>` and
    :class:`immersions.Contract <lino_welfare.modlib.immersions.Contract>`

    Inherits from :class:`lino_welfare.modlib.system.Signers`,
    :class:`Certifiable`, :class:`EventGenerator`, :class:`UserAuthored`.

    .. attribute:: client

        The client for whom this contract is done.

    .. attribute:: applies_from

        The start date of the contract.

    .. attribute:: applies_until

        The *planned* end date of this contract.

    .. attribute:: date_ended

        The date when this contract was *effectively* ended.
        This field is set to the same value as :attr:`applies_until`.

    .. attribute:: ending

        The reason of prematured ending.  Pointer to
        :class:`ContractEnding
        <lino_welfare.modlib.isip.choicelists.ContractEnding>`

    .. attribute:: date_issued

        When the contract was issued to the client and signed by them.

    .. attribute:: date_decided

        When the contract was ratified by the responsible board.

    .. attribute:: language

        The language of this contract. Default value is the client's
        :attr:`language<lino_welfare.modlib.pcw.models.Client.language>`.

    .. attribute:: type

        The type of this contract. Pointer to a subclass of
        :class:`ContractTypeBase`.

    .. method:: get_excerpt_title(self)

        The printed title of a contract specifies just the contract type
        (not the number and name of client).

    .. method:: get_excerpt_templates(self, bm)

        Overrides
        :meth:`lino_xl.lib.excerpts.Certifiable.get_excerpt_templates`.

    .. method:: client_changed(self, ar)

        If the contract's author is the client's primary coach, then set
        user_asd to None, otherwise set user_asd to the primary coach.
        We no longer suppose that only integration agents write
        contracts.

    .. method:: full_clean(self, *args, **kw)

        Checks for the following error conditions:

        - You must specify a contract type.
        - :message:`Contract ends before it started.`
        - Any error message returned by :class:`OverlappingContractsTest`

    .. method:: get_aid_confirmation(self)

        Returns the last aid confirmation that has been issued for this
        contract. May be used in `.odt` template.

        Update 20170530: not the last *confirmation* but the last
        *granting*.

    .. method:: suggest_cal_guests(self, event)

        Automatic evaluation events have the client as mandatory
        participant, plus possibly some other coach.

    .. method:: get_printable_demo_objects(cls)

        All contracts of a demo project (not only one) are being printed.
        Overrides
        :meth:`lino.modlib.printing.Printable.get_printable_demo_objects`.


.. class:: ContractBaseTable

    Base for contract tables. Defines the following parameter fields:

    .. attribute:: user

    .. attribute:: observed_event

        See :class:`ContractEvents`.

    .. attribute:: ending

        Show only contracts with the specified
        :class:`ContractEnding
        <lino_welfare.modlib.isip.models.ContractEnding>`.

    .. attribute:: ending_success

        Select "Yes" to show only contracts whose ending
        :class:`ContractEnding
        <lino_welfare.modlib.isip.models.ContractEnding>` has
        :attr:`is_success
        <lino_welfare.modlib.isip.models.ContractEnding.is_success>`
        checked.


.. class:: Contract

    The Django model representing an *ISIP*.

    .. attribute:: type

        The type of this contract.
        Pointer to :class:`ContractType`.

    .. attribute:: study_type

        The type of study that is going to be followed during this
        contract.

        Pointer to :class:`lino_xl.lib.cv.models.StudyType`.




Related models
==============


.. class:: ContractTypes

   The table of all ISIP contract types.

.. class:: ContractType(ContractTypeBase)

    The type of a :class:`Contract`.

    .. attribute:: needs_study_type

        Whether contracts of this type need their :attr:`study_type`
        field filled in.

.. class:: ExamPolicy

    An **examination policy** is mostly a :class:`RecurrenceSet
    <lino_xl.lib.cal.RecurrenceSet>` used for generating
    "evaluation meetings".  That is, Lino automatically suggests dates
    where the agent invites the client.

    TODO: replace this by :class:`lino_xl.lib.cal.EventPolicy` (?).


.. class:: ContractEnding

    A possible reason for premature termination of a contract.

    TODO: move this to :mod:`lino_welfare.modlib.integ`.

.. class:: ContractPartner

    Represents a third-party external partner who participates in this
    contract. For every partner there is a rich text field describing
    their duties.


Miscellaneous models
====================

.. class:: ContractEvents

    A list of observable events for filtering contracts
    (:attr:`ContractBaseTable.observed_event`).

    >>> rt.show(isip.ContractEvents)
    ======= ========= =========
     value   name      text
    ------- --------- ---------
     10      active    Active
     20      started   Started
     30      ended     Ended
     40      decided   Decided
     50      issued    Issued
    ======= ========= =========
    <BLANKLINE>

.. class:: ClientHasContract

    Whether the client has at least one ISIP contact during the
    observed date range.
    
    A filter criteria added to
    :class:`lino_xl.lib.clients.ClientEvents`.


.. class:: ContractsByClient

    To see this table you need either IntegrationAgent or
    SocialCoordinator.



.. class:: ContractTypeBase

    Base class for all `ContractType` models.

    Used by :mod:`lino_welfare.modlib.isip`, :mod:`lino_welfare.modlib.jobs`,
    :mod:`lino_welfare.modlib.art61` and :mod:`lino_welfare.modlib.immersion`,

    .. attribute:: full_name

        The full description of this contract type as used in printed
        documents.

    .. attribute:: exam_policy

        The default examination policy to be used for contracts of
        this type.

        This is a pointer to :class:`ExamPolicy
        <lino_welfare.modlib.isip.models.ExamPolicy>`. All contract
        types share the same set of examination policies.

    .. attribute:: overlap_group

        The overlap group to use when checking whether two contracts are
        overlapping or not. If this field is empty, Lino does not check at all
        for overlapping contracts.

        See :class:`OverlappingContractsTest`.

    .. attribute:: template

        The main template to use instead of the default template
        defined on the excerpt type.

        See
        :meth:`lino_xl.lib.excerpts.mixins.Certifiable.get_excerpt_templates`.

Overlapping contracts
=====================

Lino Welfare helps social agents to avoid problems resulting from wrong dates
concerning the beginning and ending of contracts.

When entering several contracts for a client, Lino can check whether they
overlap.  This check is not done for alle contracts. For example, a client can
have an active job contract (these usually run for 18 months) and still have
additional training contractrs in parallel.


.. class:: OverlapGroups

    The list of all known overlap groups to be selected for the
    :attr:`overlap_group <ContractTypeBase.overlap_group>`
    of a contract type.

    >>> rt.show(isip.OverlapGroups)
    ======= =========== =============
     value   name        text
    ------- ----------- -------------
     10      contracts   Conventions
     20      trainings   Trainings
    ======= =========== =============
    <BLANKLINE>


.. class:: OverlappingContractsTest

    Volatile object used to test for overlapping contracts.  It is
    responsible for issuing the following error messages:

    - :message:`Date range overlaps with X #Y` means that the date
      periods of two contracts of a same client overlap in time.

      This message is issued only when the two contracts are in the same
      overlap group (see :class:`OverlapGroups`).

      The overlap group of a contract is defined by its contract type.

      No warning is issued if the contract type has no overlap group.

    - (Currently deactivated) Date range X lies outside of coached period (Y)

.. class:: OverlappingContractsChecker

    A given client cannot have two active contracts at the same time.






Visibility
==========

ISIP contracts are created and managed by Integration agents, but they
are also available for consultation to social agents, newcomer
consultants and reception clerks.

>>> p100 = users.UserTypes.get_by_value('100') # integ agents
>>> p200 = users.UserTypes.get_by_value('200') # newcomer agents
>>> p210 = users.UserTypes.get_by_value('210') # reception clerks
>>> p400 = users.UserTypes.get_by_value('400') # social agents

>>> isip.MyContracts.get_view_permission(p100)
True
>>> isip.MyContracts.get_view_permission(p200)  #doctest: +SKIP
False
>>> isip.MyContracts.get_view_permission(p210)  #doctest: +SKIP
False
>>> isip.MyContracts.get_view_permission(p400)  #doctest: +SKIP
False

>>> isip.ContractsByClient.get_view_permission(p100)
True
>>> isip.ContractsByClient.get_view_permission(p200)
True
>>> isip.ContractsByClient.get_view_permission(p210)
True
>>> isip.ContractsByClient.get_view_permission(p400)
True


Configuration
=============

>>> ses.show(isip.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== =========== ==================== ==================
 Designation           Reference   Examination Policy   needs Study type
--------------------- ----------- -------------------- ------------------
 VSE Ausbildung        vsea        Every month          Yes
 VSE Arbeitssuche      vseb        Every month          No
 VSE Lehre             vsec        Every month          No
 VSE Vollzeitstudium   vsed        Every month          Yes
 VSE Sprachkurs        vsee        Every month          No
===================== =========== ==================== ==================
<BLANKLINE>


>>> rt.show(isip.Contracts)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ============== ============ ============================ ================= =====================
 ID   applies from   date ended   Client                       Author            Contract Type
---- -------------- ------------ ---------------------------- ----------------- ---------------------
 1    29/09/2012     07/08/2013   AUSDEMWALD Alfons (116)      Hubert Huppertz   VSE Ausbildung
 2    08/08/2013     01/12/2014   AUSDEMWALD Alfons (116)      Mélanie Mélard    VSE Arbeitssuche
 3    09/10/2012     17/08/2013   DOBBELSTEIN Dorothée (124)   Alicia Allmanns   VSE Lehre
 4    19/10/2012     11/02/2014   EVERS Eberhart (127)         Alicia Allmanns   VSE Vollzeitstudium
 5    12/02/2014     14/03/2014   EVERS Eberhart (127)         Caroline Carnol   VSE Sprachkurs
 6    15/03/2014     21/01/2015   EVERS Eberhart (127)         Caroline Carnol   VSE Ausbildung
 7    29/10/2012     21/02/2014   ENGELS Edgar (129)           Alicia Allmanns   VSE Arbeitssuche
 8    22/02/2014     31/12/2014   ENGELS Edgar (129)           Mélanie Mélard    VSE Lehre
 9    08/11/2012     03/03/2014   GROTECLAES Gregory (132)     Alicia Allmanns   VSE Vollzeitstudium
 10   18/11/2012     18/12/2012   JACOBS Jacqueline (137)      Alicia Allmanns   VSE Sprachkurs
 11   28/11/2012     06/10/2013   KAIVERS Karl (141)           Alicia Allmanns   VSE Ausbildung
 12   08/12/2012     02/04/2014   LAZARUS Line (144)           Alicia Allmanns   VSE Arbeitssuche
 13   03/04/2014     09/02/2015   LAZARUS Line (144)           Mélanie Mélard    VSE Lehre
 14   18/12/2012     12/04/2014   MEESSEN Melissa (147)        Mélanie Mélard    VSE Vollzeitstudium
 15   13/04/2014     13/05/2014   MEESSEN Melissa (147)        Mélanie Mélard    VSE Sprachkurs
 16   14/05/2014     22/03/2015   MEESSEN Melissa (147)        Mélanie Mélard    VSE Ausbildung
 17   28/12/2012     22/04/2014   RADERMACHER Alfons (153)     Alicia Allmanns   VSE Arbeitssuche
 18   07/01/2013     15/11/2013   RADERMACHER Edgard (157)     Alicia Allmanns   VSE Lehre
 19   17/01/2013     12/05/2014   RADERMACHER Guido (159)      Caroline Carnol   VSE Vollzeitstudium
 20   13/05/2014     12/06/2014   RADERMACHER Guido (159)      Mélanie Mélard    VSE Sprachkurs
 21   13/06/2014     21/04/2015   RADERMACHER Guido (159)      Mélanie Mélard    VSE Ausbildung
 22   27/01/2013     22/05/2014   DA VINCI David (165)         Alicia Allmanns   VSE Arbeitssuche
 23   23/05/2014     31/03/2015   DA VINCI David (165)         Alicia Allmanns   VSE Lehre
 24   06/02/2013     01/06/2014   ÖSTGES Otto (168)            Alicia Allmanns   VSE Vollzeitstudium
 25   02/06/2014     02/07/2014   ÖSTGES Otto (168)            Mélanie Mélard    VSE Sprachkurs
 26   03/07/2014     11/05/2015   ÖSTGES Otto (168)            Mélanie Mélard    VSE Ausbildung
 27   16/02/2013     11/06/2014   BRECHT Bernd (177)           Alicia Allmanns   VSE Arbeitssuche
 28   12/06/2014     20/04/2015   BRECHT Bernd (177)           Hubert Huppertz   VSE Lehre
 29   26/02/2013     21/06/2014   DUBOIS Robin (179)           Alicia Allmanns   VSE Vollzeitstudium
 30   22/06/2014     22/07/2014   DUBOIS Robin (179)           Mélanie Mélard    VSE Sprachkurs
 31   23/07/2014     31/05/2015   DUBOIS Robin (179)           Mélanie Mélard    VSE Ausbildung
 32   08/03/2013     01/07/2014   JEANÉMART Jérôme (181)       Mélanie Mélard    VSE Arbeitssuche
 33   02/07/2014     10/05/2015   JEANÉMART Jérôme (181)       Hubert Huppertz   VSE Lehre
==== ============== ============ ============================ ================= =====================
<BLANKLINE>


Contracts and Grantings
=======================

(The following is not yet very useful:)

>>> for obj in isip.Contracts.request():
...    print ("{} {} {}".format(obj.id, obj.applies_from, repr(obj.get_granting())))
1 2012-09-29 Granting #1 ('EiEi/29/09/2012/116')
2 2013-08-08 None
3 2012-10-09 Granting #3 ('EiEi/09/10/2012/124')
4 2012-10-19 Granting #4 ('Ausl\xe4nderbeihilfe/19/10/2012/127')
5 2014-02-12 None
6 2014-03-15 None
7 2012-10-29 Granting #7 ('EiEi/29/10/2012/129')
8 2014-02-22 None
9 2012-11-08 Granting #9 ('EiEi/08/11/2012/132')
10 2012-11-18 Granting #10 ('Ausl\xe4nderbeihilfe/18/11/2012/137')
11 2012-11-28 Granting #11 ('EiEi/28/11/2012/141')
12 2012-12-08 Granting #12 ('Ausl\xe4nderbeihilfe/08/12/2012/144')
13 2014-04-03 None
14 2012-12-18 Granting #14 ('Ausl\xe4nderbeihilfe/18/12/2012/147')
15 2014-04-13 None
16 2014-05-14 None
17 2012-12-28 Granting #17 ('EiEi/28/12/2012/153')
18 2013-01-07 Granting #18 ('Ausl\xe4nderbeihilfe/07/01/2013/157')
19 2013-01-17 Granting #19 ('EiEi/17/01/2013/159')
20 2014-05-13 None
21 2014-06-13 None
22 2013-01-27 Granting #22 ('Ausl\xe4nderbeihilfe/27/01/2013/165')
23 2014-05-23 None
24 2013-02-06 Granting #24 ('Ausl\xe4nderbeihilfe/06/02/2013/168')
25 2014-06-02 None
26 2014-07-03 None
27 2013-02-16 Granting #27 ('EiEi/16/02/2013/177')
28 2014-06-12 None
29 2013-02-26 Granting #29 ('EiEi/26/02/2013/179')
30 2014-06-22 None
31 2014-07-23 None
32 2013-03-08 Granting #32 ('Ausl\xe4nderbeihilfe/08/03/2013/181')
33 2014-07-02 None

