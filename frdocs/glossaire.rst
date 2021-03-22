==============
Glossaire
==============

.. glossary::
  :sorted:


  Vue tabulaire

    Nous parlons de vue tabullaire quand une série d'enregistrements
    vous est présentée sous forme de grille.
    Les colonnes portent des libellés.

  Vue détaillée

    Nous parlons de vue détaillée quand un seul enregistrement
    vous est présenté sous forme de formulaire.

 
  Titulaire d'un dossier
  
    cfr :attr:`welfare.coachings.Coaching.primary`


  Parcours d'insertion
    cfr :attr:`welfare.pcsw.Client.group`


  Orientation interne 
    L'orientation interne consiste en des "ateliers" que le CPAS
    organise.  Les **ateliers** proprement dits sont ouverts, càd
    fontionnent toute l'année, et les participants vont et viennent.
    On parle de **module** si c'est un atelier d'une durée déterminée
    avec un groupe de participantss fixe. Cette distinction n'est pas
    importante pour Lino.

    Il y a plusieurs grandes "catégories" d'ateliers, à savoir:

    - Ateliers d'insertion sociale (`ActivityLayouts.integ`), p.ex.
      "Trucs et astuces", "Cuisine", "Créatif", "Parentalité"

    - Ateliers d'apprentissage des savoirs de base
      (`ActivityLayouts.basic`), p.ex. "Remédiation
      français/Mathématiques".

    - Modules de détermination d'un projet socioprofessionnel
      (`ActivityLayouts.job`), p.ex. le module "Activons-nous".


  Mise au travail 

     On appelle *mise au travail* l'ensemble les projects Art.60§7,
     Art.61 **et** autres certains autres types de projets
     (:term:`ALE`, ...)

  RIS

   Revenu d'Intégration Sociale.

   Le RIS est une des formes que peut prendre le :term:`DIS`. Il
   remplace l’ancien minimum de moyens d’existence (minimex). Comme le
   minimex, le RIS est une aide purement financière.

  DIS

    Droit à l'intégration sociale.

    Concrètement le *droit à l’intégration sociale* peut prendre trois
    formes : un revenu d’intégration sociale (:term:`RIS`), un emploi,
    ou un projet individualisé d’intégration sociale (:term:`PIIS`).
    (`f1`_)

  PIIS 
  
     Un *projet individualisé d’intégration sociale* (PIIS) vise à
     établir les étapes nécessaires et les objectifs en vue de
     l’insertion sociale et/ou professionnelle progressive de tout
     bénéficiaire du DIS, pour lequel l’emploi n’est pas (encore)
     possible ou souhaitable dans un premier temps. (f1_)

     :class:`welfare.isip.Contract`.

  ALE
    Agence locale de l'emploi. Il s'agit de contrats gérés à
    l'extérieur.


  Economie sociale
    Un contrat de mise à l'emploi Art.60§7 dont le 

  Service utilisateur

    Le "service utilisateur" d'un :term:`PIIS` est l'organisation
    externe qui "utilise" le bénéficiaire, càd qui profite de son
    travail.


.. _f1: http://www.ocmw-info-cpas.be

