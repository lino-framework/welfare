.. _welfare.whitepaper:

==============================
Fiche technique Lino pour CPAS
==============================

Vocabulaire: "Lino" est un `framework
<https://fr.wikipedia.org/wiki/Framework>`_ (une bibliotheque de
modules pour créer des applications).  "Lino pour CPAS" (anglais "Lino
Welfare") est une application qui a été faite avec Lino. Il existe
d'autres applications Lino qui n'ont rien à voir avec les CPAS.


Charactéristiques du framework
------------------------------

- Lino utilise les technologies Python, Django et ExtJS pour délivrer 
  des Rich Internet Applications (RIA) au look « desktop ».
- Une application Lino fonctionne indépendamment du système d’exploitation 
  et de l’endroit géographique
- Lino tourne sur n’importe quel serveur qui offre Apache/mod_wsgi 
  (ou un autre serveur web compatible WSGI) et une des bases de 
  données MySQL, PostgreSQL, SQLite, Oracle. 
  En pratique nous recommendons Debian ou Ubuntu.
- Plusieures instances par serveur possible (par exemple pour différentes 
  applications/services et/ou environnement de test)
- Multilingue à trois niveaux : 
  (1) interface utilisateur 
  (2) désignations des codes et (3) destinataire d’un document
- Génération automatique de documents de type PDF, MS-Word, OpenOffice et autres se basant sur des templates (modèles, gabarits)
- WebDAV automatique intégré afin de pouvoir éditer des documents générés et stockés sur le serveur sans que l’utilisateur doive intervenir.
- Export des données vers des tables  en `.pdf`, `.xls` ou `.csv`
- Filtres et fonctions de recherche intuitifs et avancés
- Authentication en utilisant votre annuaire LDAP
- Il est facile de créer des adaptations sur mesure
- Système sophistiqué pour définir et modifier les workflows 

Fonctionnalités générales secrétariat
-------------------------------------

- Gestion des contacts des personnes et organisations
- Calendrier
- Messagerie électronique
- Gestion des envois (courriers, mails, SMS, ...)
- Les utilisateurs peuvent donner procuration à leurs collègue de 
  travailler et effectuer certaines actions en leur nom.

Fonctionnalités spécifiques aux CPAS
------------------------------------

- Les données signalétiques spécifiques aux CPAS (bénéficiaires,
  ménages,...)  sont intégrées de manière transparente dans la gestion
  générale des contacts.
  
- Un même bénéficiaire peut être accompagné par plusieurs agents dans
  des services différents. Nous parlons d'interventions et
  d'intervenants.

- Lecture des données de la carte d'identité électronique (eID)
  

Historique bénéficiaire
-----------------------

- Gestion des documents scannés (permis de conduire, de résidence, de
  travail,...).  Rappel optionnel si la date de fin de validité
  approche.
  
- Les travailleurs sociaux notent chaque événement.  Traçabilité par
  exemple des appels téléphoniques, des contacts internes et externe
  avec bénéficiaire, collègues ou partenaires, courriers, ...
  
Service d’insertion socio-professionnelle
-----------------------------------------

- Gestion des données relatives au CV (formations, expériences
  professionnelles, connaissances des langues, compétences, ...)
  Possibilité de recherche avancée sur base de ces critères.
  
- Gestion des PIIS: saisie, création automatique et impression du
  contrat papier, consultation, analyse statistique, rappels
  automatique des évaluations intermédiaires à prévoir
  
- Gestion des projets de mise à l'emploi (articles 60§7 et 61):
  saisie, création automatique et impression de la convention papier,
  consultation, analyse statistique, rappels automatique des
  évaluations intermédiaires à prévoir

- Gestion des partenaires art. 60§7

- Gestions des offres d’emploi vacants 


Ateliers internes
-----------------

- Planning et calendrier des ateliers
- Inscription des bénéficiaires aux ateliers
- Gestion des présences

Cours de langues
----------------

- Gestion des organisations externes organisant des cours de langue
- Par bénéficiaire saisir des demandes de cours
- Par organisation une liste des candidats
- Gestion de l’offre et de la demande


Nouvelles demandes
------------------

- Gestion des spécialités attribuées aux agents sociaux.
- Proposition automatique des agents sociaux compétents selon
  les spécificités de la demande et attribution selon la disponibilité

Médiation de dettes
-------------------

Interface d’encodage des données (dépenses, revenus, obligations,
répartition au marc-le-franc) et création automatique d’un budget
mensuel individuel ou par ménage.


Accueil
-------

- Visitors are checked in at a reception desk and
  attributed to the responsible social agent.
  Then they wait in a lounge until the agent receives them.
  After the consultation the agent checks them out.
- The social agents can consult from their desktop at any time the live 
  list of waiting visitors.
- The reception clerk verifies the client's contact data
  and can read the client's eID card into the database.
- The reception clerk can consult the calendar of a given social agent 
  to make an appointment for a client,
- The reception clerk can quickly print attestations from a 
  configurable set of templates.
  

Connexion BCSS
--------------

- Données légales RN (IdentifyPerson)
- Intégration (ManageAccess)
- Registre National avec historique (Tx25)


Connexion SEPA
--------------

- Lino importe les extraits de compte des clients dont le compte est
  géré par le CPAS.
- Les agents sociaux peuvent consulter ces données à tout moment.
