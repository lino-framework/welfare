Nouvelles demandes
==================

Une nouvelle demande est quand une personne arrive au CPAS et 
demande de l'aide.

L'accueil crée dans ce cas une 
fiche client à l'état "Nouvelle Demande". 
Le cas le plus simple est si la personne a sa carte d'identité.
(cfr `Lire une carte d'identité`_).

Pour chaque nouvelle demande il faut si possible 
remplir le champ 
`Spécificité` dans l'onglet `Accompagnement` du Client 
pour indiquer le type de problématique.

Lino va alors aider à décider quel agent social aura 
la responsabilité de s'occuper de cette personne.
Cette action s'appelle `Attribuer un accompagnateur`_.

Attribuer un accompagnateur
---------------------------

Action réservée aux utilisateurs qui font partie du groupe "Nouvelles demandes".
  
- :menuselection:`Nouvelles demandes --> Clients`. 
  Trouver le client en question.
  Double click sur ce client.

- Lino affiche,  
  dans l'onglet `Accompagnement` du Client, 
  une `Liste des agents disponibles`_, 
  triée selon un `Score`_ 
  
Score
-----

Le `score` dans la `Liste des agents disponibles`_ indique 
"la probabilité théorique de devenir accompagnateur pour ce client".
Ce score n'est bien sûr qu'un nombre théorique qui prend en compte certains facteurs.

- :menuselection:`Nouvelles demandes --> Clients`. 



Liste des agents disponibles
----------------------------

blabla

Configuration
-------------

Avant d'attendre des résultat il faut donner à Lino certaines informations de configuration.

- La liste des Spécificités (:menuselection:`Configuration --> Spécificités`

- Lino doit savoir quel agent social a la "compétence" de s'occuper 
  d'une spécificité donnée. Cette information se trouve dans l'onglet 
  `Accompagnement` de le chaque utilisateur.
  :menuselection:`Configuration --> Système --> Utilisateurs`.
  Dans ce même onglet il y a un champ `Quota Nouvelles Demandes` qui indique dans quelle mesure cet agent s'occupe de nouvelles demandes.
  Cette valeur s'exprime *en pourcentage de temps-plein*: 
  100% signifie cinq jours par semaine, 10% une demi-journée par semaine, etc.
  
- Il faut également dire à Lino combien de temps prend le traitement 
  une nouvelle demande. Ceci dépend de la spécificité: 
  un nouveau client RIS signifie plus de travail qu'une 
  simple demande d'attenstation.
  
  :menuselection:`Configuration --> Nouvelles demandes --> Spécificités`.
  Inscrivez une valeur dans le champ `Effort` de chaque spécificité. 
  Il s'agit de valeurs tout-à-fait théoriques, ce n'est que leur valeur 
  relative qui compte.
  
  


Agents disponibles
------------------



