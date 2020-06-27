.. doctest docs/specs/newcomers.rst
.. _welfare.specs.newcomers:

=======================
Newcomers (tested tour)
=======================

This is a tested tour about the :mod:`lino_welfare.modlib.newcomers`
module.

.. contents::
   :local:


.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *




Newcomers configuration
=======================

The newcomer module adds three configuration models:
:class:`Broker <lino_welfare.modlib.newcomers.models.Broker>`,
:class:`Faculty <lino_welfare.modlib.newcomers.models.Faculty>`
and
:class:`Competence <lino_welfare.modlib.newcomers.models.Competence>`.

The corresponding tables are populated with the following data:

>>> rt.show('newcomers.Brokers')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============
 name
------------
 Other PCSW
 Police
============
<BLANKLINE>


>>> rt.show('newcomers.Faculties')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================================ =========
 Bezeichnung                      Aufwand
-------------------------------- ---------
 Ausländerbeihilfe                4
 DSBE                             5
 Eingliederungseinkommen (EiEi)   10
 Finanzielle Begleitung           6
 Laufende Beihilfe                2
 **Total (5 Zeilen)**             **27**
================================ =========
<BLANKLINE>


Every newcomer agent gets attributed a set of Competences:

>>> rt.show('newcomers.Competences')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ================= ================================ =========
 ID   Benutzer          Fachbereich                      Aufwand
---- ----------------- -------------------------------- ---------
 1    Alicia Allmanns   Eingliederungseinkommen (EiEi)   10
 2    Hubert Huppertz   DSBE                             5
 3    Mélanie Mélard    Ausländerbeihilfe                4
 4    Alicia Allmanns   Finanzielle Begleitung           6
 5    Hubert Huppertz   Laufende Beihilfe                2
 6    Mélanie Mélard    Eingliederungseinkommen (EiEi)   10
 7    Alicia Allmanns   DSBE                             5
                                                         **42**
==== ================= ================================ =========
<BLANKLINE>



The newcomers table
===================

>>> rt.show('newcomers.NewClients')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================================== =========== ============ ================================ =============== ===== ================================= =========== ================ =========
 Name                                 Zustand     Vermittler   Fachbereich                      NR-Nummer       GSM   Adresse                           Alter       E-Mail-Adresse   Telefon
------------------------------------ ----------- ------------ -------------------------------- --------------- ----- --------------------------------- ----------- ---------------- ---------
 BASTIAENSEN Laurent (117)            Neuantrag                Finanzielle Begleitung           971207 001-67         Am Berg, 4700 Eupen               16 Jahre
 BRAUN Bruno (259)                    Neuantrag                                                                                                         40 Jahre
 DEMEULENAERE Dorothée (122)          Neuantrag                Ausländerbeihilfe                                      Auf'm Rain, 4700 Eupen            unbekannt
 DERICUM Daniel (121)                 Neuantrag                DSBE                             950221 001-20         August-Thonnar-Str., 4700 Eupen   19 Jahre
 EIERSCHAL Emil (175)                 Neuantrag                Laufende Beihilfe                930412 001-68         Aachen, Deutschland               21 Jahre
 EMONTSPOOL Erwin (151)               Neuantrag                DSBE                             910602 001-49         4730 Raeren                       22 Jahre
 ERNST Berta (125)                    Neuantrag                Laufende Beihilfe                900627 002-53         Bergkapellstraße, 4700 Eupen      23 Jahre
 FRISCH Paul (240)                    Neuantrag                                                                                                         46 Jahre
 GERNEGRO... Germaine (131)           Neuantrag                Laufende Beihilfe                880816 002-64         Buchenweg, 4700 Eupen             25 Jahre
 HILGERS Henri (134)                  Neuantrag                Ausländerbeihilfe                870911 001-07         Euregiostraße, 4700 Eupen         26 Jahre
 INGELS Irene (135)                   Neuantrag                Finanzielle Begleitung           861006 002-45         Feldstraße, 4700 Eupen            27 Jahre
 JANSEN Jérémy (136)                  Neuantrag                Laufende Beihilfe                851031 001-51         Gewerbestraße, 4700 Eupen         28 Jahre
 KASENNOVA Tatjana (213)              Neuantrag                DSBE                             830115 002-37         4701 Kettenis                     31 Jahre
 LAHM Lisa (176)                      Neuantrag                Eingliederungseinkommen (EiEi)   820209 002-09         Aachen, Deutschland               32 Jahre
 LASCHET Laura (143)                  Neuantrag                Eingliederungseinkommen (EiEi)   810306 002-85         Habsburgerweg, 4700 Eupen         33 Jahre
 MARTELAER Mark (172)                 Neuantrag                DSBE                             790426 001-33         Amsterdam, Niederlande            35 Jahre
 MEIER Marie-Louise (149)             Neuantrag                Laufende Beihilfe                780521 002-71         Hisselsgasse, 4700 Eupen          36 Jahre
 RADERMACHER Berta (154)              Neuantrag                Laufende Beihilfe                770615 002-43         4730 Raeren                       36 Jahre
 RADERMACHER Daniela (156)            Neuantrag                DSBE                             760710 002-82         4730 Raeren                       37 Jahre
 RADERMACHER Inge (162)               Neuantrag                DSBE                             730924 002-01         4730 Raeren                       40 Jahre
 VANDENMEULENBOS Marie-Louise (174)   Neuantrag                Finanzielle Begleitung           721019 002-40         Amsterdam, Niederlande            41 Jahre
 DI RUPO Didier (164)                 Neuantrag                Ausländerbeihilfe                711114 001-80         4730 Raeren                       42 Jahre
==================================== =========== ============ ================================ =============== ===== ================================= =========== ================ =========
<BLANKLINE>


Assigning a coach to a newcomer
-------------------------------

Let's look at the
:class:`AvailableCoachesByClient
<lino_welfare.modlib.newcomers.models.AvailableCoachesByClient>`
table.


>>> obj = pcsw.Client.objects.get(pk=117)
>>> print(obj)
BASTIAENSEN Laurent (117)

>>> rt.show(newcomers.AvailableCoachesByClient, master_instance=obj)
================= ========== ================= =============== =================== =========== =============== ===================
 Name              Workflow   Komplette Akten   Neue Klienten   Quote Erstempfang   Belastung   Mehrbelastung   Mehrbelastung (%)
----------------- ---------- ----------------- --------------- ------------------- ----------- --------------- -------------------
 Alicia Allmanns              **12**            **1**           100                 6,          6,              100,00
================= ========== ================= =============== =================== =========== =============== ===================
<BLANKLINE>

>>> url = '/api/newcomers/AvailableCoachesByClient?fmt=json&mt=58&mk=117'
>>> test_client.force_login(rt.login('rolf').user)
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> res.status_code
200
>>> d = json.loads(res.content)

The value in column "Arbeitsablauf" of the first data row in the above
table looks empty, but when rendered on screen it contains a call to
the :class:`AssignCoach
<lino_welfare.modlib.newcomers.models.AssignCoach>` action:

>>> html = d['rows'][0][1]
>>> soup = BeautifulSoup(html, 'lxml')
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF
Zuweisen

>>> links = soup.find_all('a')
>>> len(links)
1

The text of this action call is "Zuweisen":

>>> print(links[0].string)
Zuweisen

And the `status` of this call (the second argument to
:js:func:`Lino.WindowAction.run`) must include the `record_id` of the
user being assigned (6 in this case):

..
    >>> contenttypes.ContentType.objects.get_for_model(pcsw.Client).pk #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    56

>>> print(links[0].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.newcomers.AvailableCoachesByClient.assign_coach.run(null,{
  "base_params": { "mk": 117, "mt": ... }, "field_values": {
  "notify_body": "BASTIAENSEN Laurent (117) wird ab jetzt begleitet f\u00fcr Finanzielle Begleitung durch Alicia Allmanns.",
  "notify_silent": false,
  "notify_subject": "BASTIAENSEN Laurent (117) zugewiesen zu Alicia Allmanns" },
  "param_values": { "for_client": null, "for_clientHidden": null, "since": "22.04.2014" },
  "record_id": 6 })

This call is generated by :attr:`dd.Model.workflow_buttons
<lino.core.model.Model.workflow_buttons>`, which calls
:meth:`ar.action_button
<lino.core.requests.BaseRequest.action_button>`. Which is where we had
a bug on :blogref:`20150515`.



User roles
==========

The newcomers module distinguishes between **newcomer agents** and
**newcomer operators**.

- The fields `broker`, `faculty` and `refusal_reason` are readonly for
  all except newcomer agents/operators.

- A :class:`NewcomersAgent
  <lino_welfare.modlib.newcomers.roles.NewcomersAgent>` is a
  :class:`SocialAgent <lino_welfare.modlib.pcsw.roles.SocialAgent>`
  who can also manage newcomers.

:class:`lino_welfare.modlib.newcomers.models.NewClients`


:class:`lino_xl.lib.contacts.roles.ContactsUser`
:class:`lino.modlib.office.roles.OfficeOperator`

-   The :class:`AvailableCoaches
    <lino_welfare.modlib.newcomers.models.AvailableCoaches>` table shows
    only users who are :class:`SocialAgent
    <lino_welfare.modlib.pcsw.roles.SocialAgent>`
