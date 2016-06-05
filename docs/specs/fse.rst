.. _welfare.specs.fse:

==========================================
Statistiques pour le Fonds Social Européen
==========================================

..  To test only this document:

    $ python setup.py test -s tests.SpecsTests.test_fse

    doctest initialization:

    >>> from __future__ import print_function
    >>> from lino import startup
    >>> startup('lino_welfare.projects.chatelet.settings.doctests')
    >>> from lino.api.doctest import *

This is (a first draft) of the functional specification for the
:mod:`lino_welfare.modlib.fse` plugin which helps generating yearly
reports for the `ESF
<http://ec.europa.eu/esf/main.jsp?catId=35&langId=en>`_.

Ticket :ticket:`584` is to write a first prototype.


.. contents::
   :local:
   :depth: 2

The :mod:`lino_welfare.modlib.fse` plugin needs
:mod:`lino.modlib.summaries` and :mod:`lino.modlib.weasyprint`:

>>> dd.plugins.fse.needs_plugins
['lino.modlib.summaries', 'lino.modlib.weasyprint']


Dossier
=======

The plugin adds one central database object model called
:class:`Dossier <lino_welfare.modlib.fse.models.Dossier>`. Every
*dossier* represents a document to be printed as "Fiche stagiaire".

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
  encoder les données dans un fichier Excel protégé issu par 

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

  

