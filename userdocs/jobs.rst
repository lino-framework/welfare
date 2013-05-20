.. _welfare.jobs:

===============================
Insertion socio-professionnelle
===============================

Ce module permet de gérer des projects 
de mise au travail selon les articles 60§7 et 61 de 
la loi organique des CPAS.

Si pour des jeunes en-dessous des 25 ans on 
parle surtout d':ref:`welfare.isip` 
et de leur *enseignement*, 
pour les adultes nous 
parlons d'**insertion socio-professionnelle**
et nous concentrons au **travail**.

Aperçu
======

Le CPAS gère une liste d':ref:`welfare.jobs.Jobs` (de mise au travail).
Ces endroits de mise au travail sont généralement des endroits de travail 
spécialisés à l'accqueil temporaire de personnes à intégrer.
Exemple:

.. django2rst:: 

    settings.SITE.login('romain').show(jobs.Jobs.request(limit=4))
    

Indépendamment de ces endroits de travail le CPAS peut gérer une 
liste d':ref:`welfare.jobs.Offers` du marché normal.

Une :ref:`Candidature <welfare.jobs.Candidatures>` 
représente le fait qu'un :ref:`Client <welfare.pcsw.Clients>` donné
voudrait travailler à un :ref:`Endroit <welfare.jobs.Jobs>` donné.
Ceci implique entre autres que l'agent d'insertion responsable
l'estime potentiellement apte à assumer ce travail.

Eine Kandidatur ist "wenn ein :ref:`welfare.pcsw.Client` sich für 
eine :ref:`welfare.jobs.Job` bewirbt".
Das beinhaltet u.a. auch die Information, dass der verantwortliche 
Begleiter die Person als für diese Stelle geeignet einstuft.

Si un :ref:`Client <welfare.pcsw.Client>` introduit une
:ref:`Candidature <welfare.jobs.Candidatures>`, 
l'agent d'insertion note que 

Une telle Candidature peut référer soit à un Endroit soit à une Offre.

Et puis on fera un :ref:`Contract <welfare.jobs.Contracts>`.

Référence
=========

.. actor:: jobs.Jobs
.. actor:: jobs.JobProviders
.. actor:: jobs.Contracts
.. actor:: jobs.Candidatures
.. actor:: jobs.Regimes
.. actor:: jobs.Sectors
.. actor:: jobs.Functions
.. actor:: jobs.Schedules
.. actor:: jobs.Offers
.. actor:: jobs.Studies
.. actor:: jobs.StudiesByPerson
.. actor:: jobs.Experiences
.. actor:: jobs.ExperiencesByPerson
.. actor:: jobs.JobTypes
.. actor:: jobs.ContractTypes



.. actor:: jobs.JobsOverview

Ceci est la vieille version du document, elle sera remplacée par
:ref:`welfare.jobs.NewJobsOverview`

.. actor:: jobs.NewJobsOverview


This list helps you to make decisions like:

- which jobs are soon going to be free, and which candidate(s) should we
  suggest?
- bla bla

Example (using fictive demo data):

.. django2rst:: 

    settings.SITE.login('rolf').show(jobs.NewJobsOverview)
    
