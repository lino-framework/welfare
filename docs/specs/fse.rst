.. _welfare.specs.fse:

==========================================
Statistiques pour le Fonds Social Européen
==========================================

This is a first draft of a functional specification for a project to
be implemented as a new plugin :mod:`lino_welfare.modlib.fse`.

Ticket :ticket:`584` is to write a first prototype.


..  To test only this document:

    $ python setup.py test -s tests.SpecsTests.test_aids

    doctest initialization:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.chatelet.settings.doctests'
    >>> from lino.api.doctest import *

    >>> ses = rt.login('rolf')
    >>> translation.activate('de')

.. contents::
   :local:
   :depth: 2


Dossier
=======

There will be one central database object model (:class:`Dossier
<lino_welfare.modlib.fse.models.Dossier>`). Every *dossier* represents
a document to be printed as "Fiche stagiaire".  List of the data
fields per *dossier*:

- `client` : a pointer to the :class:`Client
  <lino_welfare.modlib.pcsw.models.Client>`

- The observed period (`start_date` and `end_date`, usually one
  calendar year)

- Situation professionnelle à l’entrée: Bénéficiaire CPAS (ce sera
  uniquement cette appellation)

- Inoccupé(e) depuis : date field filled from « Cherche du travail
  depuis » date FSE (onglet RAE))

- Ménage: combo box ("ménage sans emploi", "ménage dont au moins 1
  personne occupe un emploi")
  
- Enfant(s) à charge: checkbox

- Niveau diplôme : combobox (Sans diplôme - CEB - CE1D - CESI -
  CESS-CQ6-CE6P-7P - Bachelier-graduat - Master-licence - 
  Enseignement secondaire complémentaire - Non reconnu – inconnu)

- Handicap reconnu: checkbox

- Autre difficulté rencontrée :	checkbox

- Date d’entrée : reprendre date de l’atelier « Séance d’information » 
- Contrat de travail sous art. 60 depuis le : date field filled from `jobs.Contract`
- Date de sortie : Onglet intervenant – module intervention date « au »  
- Type de sortie : Onglet intervenants – Module intervention - « Cause d’abandon »

- Acquis en fin de formation : filled from Onglet Compétence – Module
  compétences professionnelles - case « Preuve de qualification »


- Attestation de participation: combobox (Epreuve d’évaluation réussie
  sans titre spécifique - Certificat sectoriel - Titre de validation
  des compétences - Certificat de valorisation de l’acquis de
  l’expérience - Diplôme ou certificat délivré par un établissement
  scolaire - Pas d’acquis)


HoursByDossier
==============

And then a virtual table which summarizes the total duration of
presences (:class:`Guest <lino.modlib.cal.models.Guest>` objects) of
that client into the following columns:

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
for each column. Most columns must automatically get generated from
database content (one entry per `courses.Line` as it seems), but some
columns are special and require a hard-coded method.


