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

Le CPAS gère une liste d':ddref:`jobs.Jobs` (de mise au travail).
Ces endroits de mise au travail sont généralement des endroits de travail 
spécialisés à l'accqueil temporaire de personnes à intégrer.
Exemple:

.. django2rst:: 

    settings.SITE.login('romain').show(jobs.Jobs.request(limit=4))
    

Indépendamment de ces endroits de travail le CPAS peut gérer une 
liste d':ddref:`jobs.Offers` du marché normal.

Une :ddref:`jobs.Candidature` 
représente le fait qu'un :ddref:`pcsw.Client` donné
voudrait travailler à un :ddref:`jobs.Job` donné.
Ceci implique entre autres que l'agent d'insertion responsable
l'estime potentiellement apte à assumer ce travail.

Eine Kandidatur ist "wenn ein :ddref:`pcsw.Client` sich für 
eine :ddref:`jobs.Job` bewirbt".
Das beinhaltet u.a. auch die Information, dass der verantwortliche 
Begleiter die Person als für diese Stelle geeignet einstuft.

Si un :ddref:`pcsw.Client` introduit une
:ddref:`jobs.Candidature`, 
l'agent d'insertion note que 

Une telle Candidature peut référer soit à un Endroit soit à une Offre.

Et puis on fera un :ddref:`jobs.Contract`.

Référence
=========

.. actor:: jobs.Job
.. actor:: jobs.JobProvider
.. actor:: jobs.Contract
.. actor:: jobs.Candidature
.. actor:: jobs.Regime
.. actor:: jobs.Sector
.. actor:: jobs.Function
.. actor:: jobs.Schedule
.. actor:: jobs.Offer
.. actor:: jobs.Study
.. actor:: jobs.Experience
.. actor:: jobs.JobType
.. actor:: jobs.ContractType



.. actor:: jobs.JobsOverview

    This list helps you to make decisions like:

    - which jobs are soon going to be free, and which candidate(s) should we
      suggest?
    - bla bla

    Example (using fictive demo data):

    .. django2rst:: 

        settings.SITE.login('rolf').show(jobs.JobsOverview)
        

.. actor:: jobs.StudiesByPerson

.. actor:: jobs.ExperiencesByPerson
