.. _welfare.specs.clients.eupen:

===============
Clients (Eupen)
===============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_clients_eupen
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
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

Some panels are not visible to everybody. Their modified visibility is marked 
between brackets (e.g. `[visible for all except anonymous, 210]`).

.. py2rst::
    from lino.api.doctest import *
    from lino.utils.diag import py2rst
    with translation.override('de'):
      print(py2rst(pcsw.Clients.detail_layout))

..
    >>> from lino.utils.diag import py2rst
    >>> print(py2rst(pcsw.Clients.detail_layout, True))
    ... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
    (main) [visible for all except anonymous]:
    - **Person** (general):
      - (general_1):
        - **None** (overview)
        - (general2):
          - (general2_1): **Geschlecht** (gender), **ID** (id)
          - (general2_2): **Vorname** (first_name), **Zwischenname** (middle_name), **Familienname** (last_name)
          - (general2_3): **Geburtsdatum** (birth_date), **Alter** (age), **NR-Nummer** (national_id)
          - (general2_4): **Staatsangehörigkeit** (nationality), **Deklarierter Name** (declared_name)
          - (general2_5): **Zivilstand** (civil_state), **Geburtsland** (birth_country), **Geburtsort** (birth_place)
        - (general3): **Sprache** (language), **E-Mail** (email), **Telefon** (phone), **Fax** (fax), **GSM** (gsm)
        - **None** (image)
      - (general_2):
        - **Termine** (reception.AppointmentsByPartner)
        - **Termin machen mit** (AgentsByClient)
    - **Beziehungen** (contact):
      - (contact_1): **Ähnliche Klienten** (SimilarClients), **Beziehungen** (LinksByHuman), **ZDSS** (cbss_relations)
      - (contact_2):
        - **Mitgliedschaft in Haushalten** (MembersByPerson)
        - **Haushaltszusammensetzung** (households.SiblingsByPerson)
    - **Begleiter** (coaching):
      - (coaching_1) [visible for all except anonymous, 100, 210, 400, 410]:
        - (newcomers_left):
          - (newcomers_left_1) [visible for all except anonymous]: **Arbeitsablauf** (workflow_buttons), **Identifizierendes Dokument** (id_document)
          - **Vermittler** (broker) [visible for all except anonymous]
          - **Fachbereich** (faculty) [visible for all except anonymous]
          - **Ablehnungsgrund** (refusal_reason) [visible for all except anonymous]
        - **Verfügbare Begleiter** (newcomers.AvailableCoachesByClient)
      - (coaching_2):
        - **Kontakte** (pcsw.ContactsByClient)
        - **Begleitungen** (pcsw.CoachingsByClient)
    - **Hilfen** (aids_tab):
      - (aids_tab_1):
        - (status):
          - (status_1): **Lebt in Belgien seit** (in_belgium_since), **Register** (residence_type), **Gesdos-Nr** (gesdos_id), **TIM ID** (tim_id)
          - (status_2): **Interim-Agenturen** (job_agents), **Integrationsphase** (group), **Sozialhilfeart** (aid_type)
        - (income):
          - (income_1): **Arbeitslosengeld** (income_ag), **Wartegeld** (income_wg)
          - (income_2): **Krankengeld** (income_kg), **Rente** (income_rente)
          - **andere Einkommen** (income_misc)
      - **Konten** (sepa.AccountsByClient)
      - **Hilfebeschlüsse** (aids.GrantingsByClient)
    - **Arbeitssuche** (work_tab_1):
      - (suche) [visible for all except anonymous, 210, 220]:
        - **Dispenzen** (pcsw.DispensesByClient)
        - **AG-Sperren** (pcsw.ExclusionsByClient)
      - (papers):
        - (papers_1): **Arbeit suchend** (is_seeking), **eingetragen seit** (unemployed_since), **Wartezeit bis** (work_permit_suspended_until)
        - (papers_2): **Braucht Aufenthaltserlaubnis** (needs_residence_permit), **Braucht Arb.Erl.** (needs_work_permit)
        - **Uploads** (UploadsByClient)
    - **Lebenslauf** (career) [visible for 100, 110, 120, admin]:
      - **Erstellte Lebensläufe** (cvs_emitted) [visible for all except anonymous]
      - **Studien** (cv.StudiesByPerson)
      - **Ausbildungen** (cv.TrainingsByPerson)
      - **Berufserfahrungen** (cv.ExperiencesByPerson)
    - **Sprachen** (languages) [visible for 100, 110, 120, admin]:
      - **Sprachkenntnisse** (cv.LanguageKnowledgesByPerson)
      - **Kursanfragen** (courses.CourseRequestsByPerson)
    - **Kompetenzen** (competences) [visible for 100, 110, 120, admin]:
      - (competences_1) [visible for all except anonymous]:
        - **Fachkompetenzen** (cv.SkillsByPerson) [visible for 100, 110, 120, admin]
        - **Sozialkompetenzen** (cv.SoftSkillsByPerson) [visible for 100, 110, 120, admin]
        - **Sonstige Fähigkeiten** (skills)
      - (competences_2) [visible for all except anonymous]:
        - **Hindernisse** (cv.ObstaclesByPerson) [visible for 100, 110, 120, admin]
        - **Sonstige Hindernisse** (obstacles)
    - **Verträge** (contracts) [visible for 100, 110, 120, admin]:
      - **VSEs** (isip.ContractsByClient)
      - **Stellenanfragen** (jobs.CandidaturesByPerson)
      - **Art.60§7-Konventionen** (jobs.ContractsByClient)
    - **Historie** (history):
      - **Ereignisse/Notizen** (notes.NotesByProject)
      - **Bestehende Auszüge** (ExcerptsByProject)
    - **Kalender** (calendar) [visible for all except anonymous, 210, 220]:
      - **Termine** (cal.EventsByClient)
      - **Aufgaben** (cal.TasksByProject)
    - **Sonstiges** (misc) [visible for 110, 410, admin]:
      - (misc_1) [visible for all except anonymous]: **Beruf** (activity), **Zustand** (client_state), **Adelstitel** (noble_condition), **Nicht verfügbar bis** (unavailable_until), **Grund** (unavailable_why)
      - (misc_2) [visible for all except anonymous]: **Sozialhilfeempfänger** (is_cpas), **Altenheim** (is_senior), **veraltet** (is_obsolete)
      - (misc_3) [visible for all except anonymous]: **Erstellt** (created), **Bearbeitet** (modified)
      - (misc_4) [visible for all except anonymous]: **Bemerkungen** (remarks), **Bemerkungen (Sozialsekretariat)** (remarks2)
      - (misc_5) [visible for all except anonymous]:
        - **Datenprobleme** (plausibility.ProblemsByOwner)
        - **Kontaktperson für** (contacts.RolesByPerson)
    - **ZDSS** (cbss) [visible for all except anonymous, 210, 220]:
      - (cbss_1) [visible for all except anonymous]: **IdentifyPerson-Anfragen** (cbss_identify_person), **ManageAccess-Anfragen** (cbss_manage_access), **Tx25-Anfragen** (cbss_retrieve_ti_groups)
      - **Zusammenfassung ZDSS** (cbss_summary) [visible for all except anonymous]
    - **Schuldnerberatung** (debts) [visible for 300, admin]:
      - **Ist Hauptpartner in folgenden Budgets:** (debts.BudgetsByPartner)
      - **Ist Akteur in folgenden Budgets:** (debts.ActorsByPartner)
    <BLANKLINE>
