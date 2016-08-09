.. _welfare.specs.fse:
.. _welfare.specs.esf:

==========================================
Statistiques pour le Fonds Social Européen
==========================================

..  To test only this document:

    $ python setup.py test -s tests.SpecsTests.test_esf

    doctest initialization:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.chatelet.settings.doctests')
    >>> from lino.api.doctest import *

This is (a first draft) of the functional specification for the
:mod:`lino_welfare.modlib.esf` plugin which helps generating yearly
reports for the `ESF
<http://ec.europa.eu/esf/main.jsp?catId=35&langId=en>`_.

Ticket :ticket:`584` is to write a first prototype.


.. contents::
   :local:
   :depth: 2

The :mod:`lino_welfare.modlib.esf` plugin needs
:mod:`lino.modlib.summaries` and :mod:`lino.modlib.weasyprint`:

>>> dd.plugins.esf.needs_plugins
['lino.modlib.summaries', 'lino.modlib.weasyprint']


Dossier
=======

The plugin adds one central database object model called
:class:`Client summary
<lino_welfare.modlib.esf.models.ClientSummary>`. Every *client
summary* represents a document to be printed as "Fiche stagiaire".

A client summary is a subclass of
:class:`lino.modlib.summaries.mixins.Summary`

List of the data fields per *dossier*:

- `client` : a pointer to the :class:`Client
  <lino_welfare.modlib.pcsw.models.Client>`

- The observed period (`start_date` and `end_date`, usually one
  calendar year)

- Situation professionnelle à l’entrée: Bénéficiaire CPAS (ce sera
  uniquement cette appellation)

- Inoccupé(e) depuis : date field filled from «Cherche du travail
  depuis» date FSE (onglet RAE))

- Ménage: combo box ("ménage sans emploi", "ménage dont au moins 1
  personne occupe un emploi")
  
- Enfant(s) à charge: checkbox

- Niveau diplôme: combobox (Sans diplôme - CEB - CE1D - CESI -
  CESS-CQ6-CE6P-7P - Bachelier-graduat - Master-licence - 
  Enseignement secondaire complémentaire - Non reconnu – inconnu)

- Handicap reconnu: checkbox

- Autre difficulté rencontrée:	checkbox

- Date d’entrée: reprendre date de l’atelier « Séance d’information » 
- Contrat de travail sous art. 60 depuis le: date field filled from `jobs.Contract`
- Date de sortie: Onglet intervenant – module intervention date « au »  
- Type de sortie: Onglet intervenants – Module intervention - « Cause d’abandon »

- Acquis en fin de formation : filled from Onglet Compétence – Module
  compétences professionnelles - case « Preuve de qualification »

- Attestation de participation: combobox (Epreuve d’évaluation réussie
  sans titre spécifique - Certificat sectoriel - Titre de validation
  des compétences - Certificat de valorisation de l’acquis de
  l’expérience - Diplôme ou certificat délivré par un établissement
  scolaire - Pas d’acquis)


HoursByDossier
==============

And then the module provides a way for defining a series of
"statistical numbers" which represent the activity of that client
during a given period.

For most fields this is the total duration of presences (:class:`Guest
<lino.modlib.cal.models.Guest>` objects) of that client.

- Information : Séance d’info. (2h FSE)

- Orientation - suivi:

  - Entretien individuel (1h FSE)
  - Evaluation formation externe et art.61 (1h FSE)

- Mobilisation : S.I.S. agréé (en fonction de la participation à un ou
  plusieurs ateliers)

- Apprentissage de base

  - Test de niveau (math, français, informatique) (3h FSE)
  - Initiation informatique (3h FSE) 
  - Mobilité (3h FSE)
  - Remédiation mathématique et français (3h FSE)

- Module projet : Activons-nous (3h FSE)

- Mise en situation professionnelle Case « Heure » à ajouter au module

- Recherche d’emploi : Cyber emploi (à discuter)

- Mise à l’emploi sous contrat art.60§7 (Sélection des années – case Heure)

This distribution will probably require a choicelist with one choice
for each field. 

These fields will probably not be columns of a slave table but
(dynamicaly generated) database fields in the Dossier model.

There will also be a pointer to 
(one entry per `courses.Line` as it seems), but some columns are
special and require a hard-coded method.



Notes de discussion
===================

- Par bénéficiaire il peut y avoir plusieurs fiches stagiaire au cours
  du temps. En principe une fiche pour chaque stage.
- Où dans le détail du bénéficaire faut-il afficher ce panneau avec
  les "fiches stagiaire"? --> dans l'onglet "Historique"
- Idéal serait d'avoir une checkbox "Générer fiches stagiaire" par
  bénéficiaire.

- Bouton "Remplir les données"

- la fiche est un document à usage interne utilisé par Sandra pour
  encoder les données dans un fichier Excel protégé issu par X.

- Colonne "Mise en situation professionnelle" : calculer les heures
  par stage d'immersion, en fonction des dates de début et de fin et
  de l'horaire de travail.

- Colonne "Recherche d'emploi" : Somme des présences aux ateliers
  "Cyber-emploi", mais pour ces ateliers on note les heures d'arrivée
  et de départ par participation.

- Colonne "Mise à l'emploi sous contrat a60" : comme pour 
  "Mise en situation professionnelle"

- Tous les "champs statistiques" représentent des heures de présences.
  Il y a deux modes d'encodage de présences des ateliers: soit avec
  soit sans les heures de d'arrivée de départ individuelles.  Par
  exemple en Insertion si la personne arrive en retard, elle aura les
  heures de présence de l'évènement (tant pis pour la statistique).


Par type d'entrée calendrier on doit configurer le champ FSE dans
lequel seront totalisés les heures.

>>> rt.show(cal.EventTypes, language="fr")
======================================== ======================================== =============================== ======================== ==============================
 Désignation                              Désignation (de)                         Désignation (en)                Inviter le bénéficiare   Champ FSE
---------------------------------------- ---------------------------------------- ------------------------------- ------------------------ ------------------------------
 Jours fériés                             Feiertage                                Holidays                        Non
 Réunion                                  Versammlung                              Meeting                         Non
 Internal meetings with client            Internal meetings with client            Internal meetings with client   Oui                      Séance d’information
 Évaluation                               Auswertung                               Evaluation                      Oui                      Entretien individuel
 Consultations avec le bénéficiaire       Beratungen mit Klient                    Consultations with client       Non
 Réunions externes avec le bénéficiaire   Réunions externes avec le bénéficiaire   External meetings with client   Oui                      Evaluation formation externe
 Informational meetings                   Informational meetings                   Informational meetings          Oui                      S.I.S. agréé
 Réunions interne                         Réunions interne                         Internal meetings               Non
 Réunions externe                         Réunions externe                         External meetings               Non
 Privé                                    Privat                                   Private                         Non
 Atelier                                  Atelier                                  Workshop                        Non
======================================== ======================================== =============================== ======================== ==============================
<BLANKLINE>
  

>>> rt.show(esf.StatisticalFields, language="fr")
======= ====== =================================== =================
 value   name   text                                Type
------- ------ ----------------------------------- -----------------
 10             Séance d’information                GuestHoursFixed
 20             Entretien individuel                GuestHoursFixed
 21             Evaluation formation externe        GuestHoursFixed
 30             S.I.S. agréé                        GuestHoursFixed
 40             Tests de niveau                     GuestHoursFixed
 41             Initiation informatique             GuestHoursFixed
 42             Mobilité                            GuestHoursFixed
 43             Remédiation                         GuestHoursFixed
 44             Activons-nous!                      GuestHours
 50             Mise en situation professionnelle   ImmersionHours
 60             Cyber Emploi                        GuestHours
 70             Mise à l’emploi art.60§7            Art60Hours
======= ====== =================================== =================
<BLANKLINE>

.. currentmodule:: lino_welfare.modlib.esf.choicelists

Les types de champ suivants sont disponibles par défaut:

- :class:`GuestHoursFixed`
- :class:`GuestHours>`
- :class:`ImmersionHours`
- :class:`Art60Hours`

>>> # rt.show(esf.AllSummaries)

>>> dd.plugins.summaries.start_year
2012
>>> dd.plugins.summaries.end_year
2014

>>> obj = pcsw.Client.objects.get(pk=116)
>>> print(obj)
AUSDEMWALD Alfons (116)

The field :attr:`has_esf
<lino_welfare.modlib.pcsw.models.Client.has_esf>` must be checked:

>>> print(obj.has_esf)
True

>>> show_fields(rt.models.pcsw.Client, 'has_esf')
=============== ============== =========================================================
 Internal name   Verbose name   Help text
--------------- -------------- ---------------------------------------------------------
 has_esf         ESF data       Whether Lino should make ESF summaries for this client.
=============== ============== =========================================================

>>> rt.show(esf.SummariesByClient, obj)
========== ====== ====== ========== =========== ========== ====== ====== ====== ====== ====== ====== ======
 Year       10     20     21         30          40         41     42     43     44     50     60     70
---------- ------ ------ ---------- ----------- ---------- ------ ------ ------ ------ ------ ------ ------
 2012       0:00   0:00   0:00       3:00        0:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 2013       0:00   0:00   0:00       11:00       0:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 2014       0:00   0:00   1:00       11:00       1:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 **6039**                 **1:00**   **25:00**   **1:00**
========== ====== ====== ========== =========== ========== ====== ====== ====== ====== ====== ====== ======
<BLANKLINE>

>>> rt.login().run(obj.check_summaries)
{'refresh': True}

>>> rt.show(esf.SummariesByClient, obj)
========== ====== ====== ========== =========== ========== ====== ====== ====== ====== ====== ====== ======
 Year       10     20     21         30          40         41     42     43     44     50     60     70
---------- ------ ------ ---------- ----------- ---------- ------ ------ ------ ------ ------ ------ ------
 2012       0:00   0:00   0:00       3:00        0:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 2013       0:00   0:00   0:00       11:00       0:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 2014       0:00   0:00   1:00       11:00       1:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 **6039**                 **1:00**   **25:00**   **1:00**
========== ====== ====== ========== =========== ========== ====== ====== ====== ====== ====== ====== ======
<BLANKLINE>


>>> obj = pcsw.Client.objects.get(pk=177)
>>> print(obj)
BRECHT Bernd (177)

>>> rt.show(esf.SummariesByClient, obj)
========== ====== ====== ====== ========== ========== ====== ====== ====== ====== ====== ====== ============
 Year       10     20     21     30         40         41     42     43     44     50     60     70
---------- ------ ------ ------ ---------- ---------- ------ ------ ------ ------ ------ ------ ------------
 2012       0:00   0:00   0:00   0:00       0:00       0:00   0:00   0:00   0:00   0:00   0:00   342:00
 2013       0:00   0:00   0:00   3:00       0:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 2014       0:00   0:00   0:00   0:00       1:00       0:00   0:00   0:00   0:00   0:00   0:00   0:00
 **6039**                        **3:00**   **1:00**                                             **342:00**
========== ====== ====== ====== ========== ========== ====== ====== ====== ====== ====== ====== ============
<BLANKLINE>
