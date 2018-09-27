.. doctest docs/specs/clients_eupen.rst
.. _welfare.specs.clients.eupen:

===============
Clients (Eupen)
===============

..  doctest init:
    >>> import lino
    >>> lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

.. contents::
   :depth: 2
   :local:



The detail layout of a client
=============================

Here is a textual description of the fields and their layout used in
the :class:`ClientDetail
<lino_welfare.projects.eupen.modlib.pcsw.models.ClientDetail>` of a
Lino Welfare à la Eupen.

.. lino2rst::
   
    from lino.api.doctest import *
    with translation.override('de'):
      print(py2rst(pcsw.Clients.detail_layout, False))

..
    >>> print(py2rst(pcsw.Clients.detail_layout))
    ... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
    (main) [visible for all]:
    - **Person** (general):
      - (general_1):
        - **None** (overview)
        - (general2):
          - (general2_1): **Geschlecht** (gender), **ID** (id), **TIM-ID** (tim_id)
          - (general2_2): **Vorname** (first_name), **Zwischenname** (middle_name), **Familienname** (last_name)
          - (general2_3): **Geburtsdatum** (birth_date), **Alter** (age), **NR-Nummer** (national_id)
          - (general2_4): **Staatsangehörigkeit** (nationality), **Deklarierter Name** (declared_name)
          - (general2_5): **Zivilstand** (civil_state), **Geburtsland** (birth_country), **Geburtsort** (birth_place)
        - (general3): **Sprache** (language), **E-Mail-Adresse** (email), **Telefon** (phone), **Fax** (fax), **GSM** (gsm)
        - **None** (image)
      - (general_2) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
        - **Termine** (reception.AppointmentsByPartner)
        - **Termin machen mit** (AgentsByClient)
    - **Beziehungen** (contact):
      - (contact_1): **Ähnliche Klienten** (dupable_clients_SimilarClients) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910], **Beziehungen** (humanlinks_LinksByHuman) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910], **ZDSS** (cbss_relations)
      - (contact_2) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]:
        - **Mitgliedschaft in Haushalten** (households_MembersByPerson)
        - **Haushaltszusammensetzung** (households.SiblingsByPerson)
    - **Begleiter** (coaching) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
      - (coaching_1) [visible for 110 120 200 220 300 420 800 admin 910]:
        - (newcomers_left):
          - (newcomers_left_1) [visible for all]: **Workflow** (workflow_buttons), **Identifizierendes Dokument** (id_document)
          - **Vermittler** (broker) [visible for all]
          - **Fachbereich** (faculty) [visible for all]
          - **Ablehnungsgrund** (refusal_reason) [visible for all]
        - **Verfügbare Begleiter** (newcomers.AvailableCoachesByClient)
      - (coaching_2):
        - **Kontakte** (clients.ContactsByClient)
        - **Begleitungen** (coachings.CoachingsByClient)
    - **Hilfen** (aids_tab):
      - (aids_tab_1):
        - (status):
          - (status_1): **Lebt in Belgien seit** (in_belgium_since), **Einwohnerregister** (residence_type), **Gesdos-Nr** (gesdos_id)
          - (status_2): **Interim-Agenturen** (job_agents), **Integrationsphase** (group)
        - (income):
          - (income_1): **Arbeitslosengeld** (income_ag), **Wartegeld** (income_wg)
          - (income_2): **Krankengeld** (income_kg), **Rente** (income_rente)
          - **andere Einkommen** (income_misc)
      - **Bankkonten** (sepa.AccountsByClient) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]
      - **Hilfebeschlüsse** (aids.GrantingsByClient) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]
    - **Arbeitssuche** (work_tab_1):
      - (suche) [visible for 100 110 120 200 300 400 410 420 admin 910]:
        - **Dispenzen** (pcsw.DispensesByClient)
        - **AG-Sperren** (pcsw.ExclusionsByClient)
      - (papers):
        - (papers_1): **Sucht Arbeit seit** (seeking_since), **Arbeitslos seit** (unemployed_since), **Wartezeit bis** (work_permit_suspended_until)
        - (papers_2): **Braucht Aufenthaltserlaubnis** (needs_residence_permit), **Braucht Arb.Erl.** (needs_work_permit)
        - **Uploads** (uploads_UploadsByClient) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]
    - **Lebenslauf** (career) [visible for 100 110 120 420 admin 910]:
      - **Erstellte Lebensläufe** (cvs_emitted) [visible for all]
      - **Studien** (cv.StudiesByPerson)
      - **Ausbildungen** (cv.TrainingsByPerson)
      - **Berufserfahrungen** (cv.ExperiencesByPerson)
    - **Sprachen** (languages) [visible for 100 110 120 200 300 400 410 420 admin 910]:
      - **Sprachkenntnisse** (cv_LanguageKnowledgesByPerson) [visible for 100 110 120 420 admin 910]
      - **Kursanfragen** (xcourses.CourseRequestsByPerson)
    - **Kompetenzen** (competences) [visible for 100 110 120 420 admin 910]:
      - (competences_1) [visible for all]:
        - **Fachkompetenzen** (cv.SkillsByPerson) [visible for 100 110 120 420 admin 910]
        - **Sozialkompetenzen** (cv.SoftSkillsByPerson) [visible for 100 110 120 420 admin 910]
        - **Sonstige Fähigkeiten** (skills)
      - (competences_2) [visible for all]:
        - **Hindernisse** (cv.ObstaclesByPerson) [visible for 100 110 120 420 admin 910]
        - **Sonstige Hindernisse** (obstacles)
    - **Verträge** (contracts) [visible for 100 110 120 200 210 300 400 410 420 admin 910]:
      - **VSEs** (isip.ContractsByClient) [visible for 100 110 120 210 420 admin 910]
      - **Stellenanfragen** (jobs.CandidaturesByPerson)
      - **Art.60§7-Konventionen** (jobs.ContractsByClient)
    - **Historie** (history) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]: **Ereignisse/Notizen** (notes_NotesByProject), **Bestehende Auszüge** (excerpts_ExcerptsByProject)
    - **Kalender** (calendar) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
      - **Kalendereinträge** (cal.EntriesByClient)
      - **Aufgaben** (cal.TasksByProject)
    - **Bewegungen** (MovementsByProject) [visible for 500 510 admin 910]
    - **Sonstiges** (misc) [visible for 110 120 210 410 420 800 admin 910]:
      - (misc_1) [visible for all]: **Beruf** (activity), **Zustand** (client_state), **Adelstitel** (noble_condition), **Nicht verfügbar bis** (unavailable_until), **Grund** (unavailable_why)
      - (misc_2) [visible for all]: **Sozialhilfeempfänger** (is_cpas), **Altenheim** (is_senior), **veraltet** (is_obsolete)
      - (misc_3) [visible for all]: **Erstellt** (created), **Bearbeitet** (modified)
      - (misc_4) [visible for all]: **Bemerkungen** (remarks), **Bemerkungen (Sozialsekretariat)** (remarks2)
      - (misc_5) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
        - **Datenprobleme** (checkdata_ProblemsByOwner)
        - **Kontaktperson für** (contacts.RolesByPerson)
    - **ZDSS** (cbss) [visible for 100 110 120 200 210 300 400 410 420 admin 910]:
      - (cbss_1) [visible for all]: **IdentifyPerson-Anfragen** (cbss_identify_person), **ManageAccess-Anfragen** (cbss_manage_access), **Tx25-Anfragen** (cbss_retrieve_ti_groups)
      - **Zusammenfassung ZDSS** (cbss_summary) [visible for all]
    - **Schuldnerberatung** (debts) [visible for 120 300 420 admin 910]:
      - **Ist Hauptpartner in folgenden Budgets:** (debts.BudgetsByPartner)
      - **Ist Akteur in folgenden Budgets:** (debts.ActorsByPartner)
    <BLANKLINE>


Some panels are not visible to everybody. Their visibility is marked
between brackets (e.g. `[visible for all except anonymous, 210]`).

The window itself is visible to everybody:

>>> ui = dd.plugins.extjs
>>> lh = rt.models.pcsw.Clients.detail_layout.get_layout_handle(ui)
>>> lh.main
<TabPanel main in lino_welfare.projects.eupen.modlib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients>
>>> list(lh.main.required_roles)
[]

>>> list(lh['general'].required_roles)
[]

But the "Miscellaneous" tab is visible only to users having either the
:class:`SocialStaff <lino_welfare.modlib.pcsw.roles.SocialStaff>` or
the :class:`ContactsStaff <lino_xl.lib.contacts.roles.ContactsStaff>`
role:

>>> misc = lh['misc']
>>> misc
<Panel misc in lino_welfare.projects.eupen.modlib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients>
>>> list(misc.required_roles)
[(<class 'lino_welfare.modlib.pcsw.roles.SocialStaff'>, <class 'lino_xl.lib.contacts.roles.ContactsStaff'>)]



