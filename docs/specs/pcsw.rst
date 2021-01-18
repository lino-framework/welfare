.. doctest docs/specs/pcsw.rst
.. _welfare.specs.pcsw:

==========================================
The :mod:`lino_welfare.modlib.pcsw` plugin
==========================================

.. currentmodule:: lino_welfare.modlib.pcsw


This page describes the :mod:`lino_welfare.modlib.pcsw` plugin.

.. contents:: Contents
   :local:
   :depth: 2

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *


.. >>> len(settings.SITE.languages)
   3


Client events
==============

>>> show_choicelist(pcsw.ClientEvents)
=========== =========== ===================== ========================= ========================
 value       name        de                    fr                        en
----------- ----------- --------------------- ------------------------- ------------------------
 created     created     Erstellt              Créé                      Created
 modified    modified    Bearbeitet            Modifié                   Modified
 note        note        Notiz                 Notiz                     Note
 dispense    dispense    Dispenz               Dispenz                   Dispense
 penalty     penalty     AG-Sperre             AG-Sperre                 Penalty
 active      active      Begleitung            Intervention              Coaching
 isip        isip        VSE                   PIIS                      ISIP
 jobs        jobs        Art.60§7-Konvention   Mise à l'emploi art60§7   Art60§7 job supplyment
 available   available   Verfügbar             Disponible                Available
 art61       art61       Art.61-Konvention     Mise à l'emploi art.61    Art61 job supplyment
=========== =========== ===================== ========================= ========================
<BLANKLINE>


Refusal reasons
================

>>> show_choicelist(pcsw.RefusalReasons)
======= ====== ============================================= ============================================ ==========================================
 value   name   de                                            fr                                           en
------- ------ --------------------------------------------- -------------------------------------------- ------------------------------------------
 10      None   Information (keine Begleitung erforderlich)   Demande d'information (pas d'intervention)   Information request (No coaching needed)
 20      None   ÖSHZ ist nicht zuständig                      CPAS n'est pas compétent                     PCSW is not competent
 30      None   Antragsteller ist nicht zurück gekommen       Client n'est plus revenu                     Client did not return
======= ====== ============================================= ============================================ ==========================================
<BLANKLINE>




eID card summary
================

Here a test case (fixed :blogref:`20130827`)
to test the new `eid_info` field:

>>> soup = get_json_soup('rolf', 'pcsw/Clients/116', 'overview')
>>> print(soup.get_text("\n"))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Ansicht als Partner , Person , Klient
Herr
Alfons Ausdemwald
Am Bahndamm
4700 Eupen
Adressen verwalten
Karte Nr. 123456789012 (C (Personalausweis für Ausländer)), ausgestellt durch Eupen
, gültig von 19.08.12 bis 18.08.13
Muss eID-Karte einlesen!
Keinen Kaffee anbieten
>>> soup = get_json_soup('rolf', 'pcsw/Clients/118', 'overview')
>>> print(soup.get_text("\n"))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Ansicht als Partner , Person ,  Klient
Frau
Charlotte Collard
Auf dem Spitzberg
4700 Eupen
Adressen verwalten
Karte Nr. 591413288107 (Belgischer Staatsbürger), ausgestellt durch Eupen, gültig von 19.08.11 bis 19.08.16


Coaching types
==============

>>> ses = rt.login('rolf')
>>> ses.show('coachings.CoachingTypes')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=================== ====== ====== =====================
 Bezeichnung         DSBE   ASD    Role in evaluations
------------------- ------ ------ ---------------------
 ASD                 Nein   Ja     Kollege
 DSBE                Ja     Nein   Kollege
 Schuldnerberatung   Nein   Nein
=================== ====== ====== =====================
<BLANKLINE>

.. note: above table shows only Bezeichnung in German because the othe
   languages are hidden:

   >>> hidden_languages = [lng.name for lng in ses.user.user_type.hidden_languages]
   >>> hidden_languages.sort()
   >>> hidden_languages
   ['en', 'fr']


Creating a new client
=====================


>>> url = '/api/pcsw/CoachedClients/-99999?an=insert&fmt=json'
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> res.status_code
200
>>> d = AttrDict(json.loads(res.content))
>>> keys = list(d.keys())
>>> keys.sort()
>>> rmu(keys)
... #doctest: +NORMALIZE_WHITESPACE +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
['data', 'phantom', 'title']
>>> d.phantom
True
>>> print(d.title)
Klient erstellen


There are a lot of data fields:

>>> len(d.data.keys())
8

>>> print(' '.join(sorted(d.data.keys())))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
disabled_fields first_name gender genderHidden language languageHidden last_name national_id



The detail action
=================

The following would have detected a bug which caused the MTI navigator
to not work (bug has been fixed :blogref:`20150227`) :

>>> from etgen.html import E
>>> p = contacts.Person.objects.get(pk=178)
>>> cli = pcsw.Client.objects.get(pk=178)

>>> ses = rt.login('robin')
>>> ar = contacts.Partners.request_from(ses)
>>> cli.get_detail_action(ses)
<BoundAction(pcsw.Clients, <lino.core.actions.ShowDetail detail ('Detail')>)>
>>> cli.get_detail_action(ar)
<BoundAction(pcsw.Clients, <lino.core.actions.ShowDetail detail ('Detail')>)>

And this tests a potential source of problems in `E.tostring` which I
removed at the same time:

>>> ses = rt.login('robin', renderer=settings.SITE.kernel.default_renderer)
>>> ar = contacts.Partners.request_from(ses)
>>> ar.renderer = settings.SITE.kernel.extjs_renderer
>>> print(tostring(ar.obj2html(p)))
<a href="javascript:Lino.contacts.Persons.detail.run(null,{ &quot;record_id&quot;: 178 })">Herr Karl KELLER</a>

>>> print(tostring(ar.obj2html(cli)))
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 178 })">KELLER Karl (178)</a>
>>> print(settings.SITE.kernel.extjs_renderer.instance_handler(ar, cli, None))
Lino.pcsw.Clients.detail.run(null,{ "record_id": 178 })
>>> print(tostring(p.get_mti_buttons(ar)))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
<a href="javascript:Lino.contacts.Partners.detail.run(null,{ &quot;record_id&quot;: 178 })">Partner</a>,
<b>Person</b>, <a
href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 178 })">Klient</a> [<a
...javascript:Lino.contacts.Partners.del_client(null,true,178,{ })...">❌</a>]


Virtual fields on client
========================

The following snippet just tests some virtual fields on Client for
runtime errors.

>>> vfields = ('primary_coach', 'coaches', 'active_contract', 'contract_company',
...     'find_appointment', 'cbss_relations', 'applies_from', 'applies_until')
>>> counters = { k: set() for k in vfields }
>>> for cli in pcsw.Client.objects.all():
...     for k in vfields:
...         counters[k].add(getattr(cli, k))
>>> [len(counters[k]) for k in vfields]
[1, 20, 21, 4, 1, 1, 21, 21]



.. class:: Client

    Inherits from :class:`lino_welfare.modlib.contacts.Person` and
    :class:`lino_xl.lib.beid.BeIdCardHolder`.

    A :class:`Client` is a polymorphic specialization of :class:`Person`.

    .. attribute:: has_esf

        Whether Lino should make ESF summaries for this client.

        This field exists only if :mod:`lino_welfasre.modlib.esf` is
        installed.

    .. attribute:: overview

        A panel with general information about this client.

    .. attribute:: cvs_emitted

        A virtual field displaying a group of shortcut links for managing CVs
        (Curriculum Vitaes).

        This field is an excerpts shortcut
        (:class:`lino_xl.lib.excerpts.models.Shortcuts`) and works only if
        the database has an :class:`ExcerptType
        <lino_xl.lib.excerpts.models.ExcerptType>` whose `shortcut` points
        to it.

    .. attribute:: id_document

        A virtual field displaying a group of buttons for managing the
        "identifying document", i.e. an uploaded document which has been
        used as alternative to the eID card.

    .. attribute:: group

        Pointer to :class:`PersonGroup`.
        The intergration phase of this client.

        The :class:`UsersWithClients <welfare.integ.UsersWithClients>`
        table groups clients using this field.


    .. attribute:: civil_state

       The civil state of this client. Allowed choices are defined in
       :class:`CivilState
       <lino_xl.lib.contacts.CivilStates>`.

    .. attribute:: client_state

        Pointer to :class:`ClientStates`.

    .. attribute:: needs_residence_permit

    .. attribute:: unemployed_since

       The date when this client got unemployed and stopped to have a
       regular work.

    .. attribute:: seeking_since

       The date when this client registered as unemployed and started
       to look for a new job.

    .. attribute:: work_permit_suspended_until


    .. method:: get_first_meeting(self, today=None)

        Return the last note of type "First meeting" for this client.
        Usage example see :doc:`debts` and
        :doc:`notes`.


.. class:: Clients

    The list that opens by :menuselection:`Contacts --> Clients`.

    .. attribute:: client_state

        If not empty, show only Clients whose `client_state` equals
        the specified value.
