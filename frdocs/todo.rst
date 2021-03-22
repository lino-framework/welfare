================
Liste des tâches
================

(Document obsolète. Demandez un accès à http://bugs.lino-framework.org
pour voir nos listes des tâches.)

Voici --en langage utilisateurs mais classifiés par le développeur--
une liste des questions à discuter et choses à faire.

.. contents:: 
   :local:
   :depth: 2

à voir ensemble
===============

#.  Recherche d'emploi active :

    - Nouvelles tables "Antécédents judiciaires", "Disponibilité et
      mobilité", "Agences interim", "Recherches d'emploi"

    - Utiliser module :mod:`ml.polls` pour les évaluations "Pour
      commencer ma recherche d'emploi, je dois..." et "Est-ce que je
      sais..." et

    - Petites annonces / Demande à l'entourage / Candidature spontanée

#.  Est-ce que "plan d'action sociale" correspond à vos questionnaires
    dans l'onglet "Recherche d'emploi"

#.  Expliquez le tableau "Preuve des recherches" (Date, Spontanée,
    Réponse à une offre)



à programmer
============

#.  Vocabulaire: remplacer "Accompagnement" par "Intervention" et
    "Accompagnant" par "Intervenant".

#.  Ajouter un champ "Garde enfant" par ménage. Texte libre. 

#.  Soit empècher de créer des interventions dans l'onglet "Personne"
    (après avoir terminé `ticket #104
    <http://lino-framework.org/tickets/104.html>`_), soit faire en
    sorte que Lino envoye un avertissement par courier aussi dans le
    cas d'une création spontanée d'intervention.

#.  "EnrolmentsByPupil" : Renommer en "Orientations internes en attente"

    Si on ajoute une orientation par ce module, il ne s’inscrit pas dans
    l’onglet « Orientation interne »…Par contre, si on ajoute la
    personne par l’onglet « Orientation interne », il apparaît
    correctement dans « Enrolments ».

    Quand on a créé un atelier, dans l’onglet inscription : Si on a fait
    une demande pour un bénéficiaire et qu’on clique sur annulé, la
    ligne disparaît des inscriptions mais pas du module Enrolments situé
    dans l’onglet personne. Peut-on faire en sorte que ça disparaisse
    aussi d’Enrolments ?

#.  Quand on insère dans les "Modules", Lino affiche également les
    types de cours des autres areas.


à installer
===========

#.  Navigateur polymorphique pour passer facilement à la vue
    "Bénéficiaire" en étant sur une "Personne" (#8).

Problèmes connus
================

#.  Il est difficile d'ouvrir une boite de sélection (combobox) en mode
    "tableau" (#10).

Demandes refusées
=================

#.  Vous vouliez ajouter une colonne "Suivi par" dans la composition
    de ménage. Pour l'instant cette info s'obtient indirectement en
    cliquant sur la petite flèche en face du nom dans la colonne
    "Personne", puis passer en vue bénéficiaire, puis passer à
    l'onglet "Intervenants". Je peux afficher cette information
    directement, mais le voulez-vous vraiment? Quid s'il y a plusieurs
    intervenants?

