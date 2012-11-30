Nouvelles demandes
==================

Une nouvelle demande est une personne qui arrive au CPAS et demande de l'aide.

L'accueil introduit une fiche client à l'état "Nouvelle Demande".

Lino va alors aider à décider quel assistant social aura la responsabilité 
de s'occuper de la nouvelle demande.

- Pour chaque nouvelle demande il faut remplir le champ 
  `Spécificité` dans l'onglet `Accompagnement` du Client 
  pour indiquer le type de problématique.
  
- Lino affiche alors, dans ce même onglet, une liste des `agents 
  disponibles`_, triés selon la probabilité théorique de devenir 
  candidat pour ce client.
  
  

Configuration
-------------

Avant d'attendre des résultat il faut donner à Lino certaines 
informations de configuration.

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



