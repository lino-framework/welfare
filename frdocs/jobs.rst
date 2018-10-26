===============================
Insertion socio-professionnelle
===============================

Ce module permet de gérer des projects de mise à l'emploi selon les
articles 60§7 et 61 de la loi organique des CPAS.

Si pour des jeunes en-dessous des 25 ans on parle surtout
d'**insertion sociale** et de leur *enseignement*, pour les adultes
nous parlons d'**insertion socio-professionnelle** et nous nous
concentrons à leur trouver un *emploi*.


Les postes de mise à l'emploi
=============================

Le CPAS gère une liste de **postes de mise à l'emploi**.  Ces postes
sont gérés en collaboration avec des entreprises ou institutions
spécialisées à l'accqueil temporaire de personnes à intégrer.
Exemple:

.. py2rst:: 

    from lino.api.doctest import *
    rt.show(jobs.Jobs.request(limit=4))
    
Lino appelle "employant" l'entreprise ou l'organisme dans laquelle le
travail a lieu.

- Article 60§7 : dans une administration publique, asbl, ou entreprise
  d'économie sociale.

- Article 61 : dans une entreprise privée

Le **type** de mise à l'emploi est défini par **poste**. (Tous les
contrats sur un poste donné sont de meme type). La liste des types de
mise à l'emploi est définie dans :menuselection:`Configuration -->
Intégration --> Types de mise à l'emploi`. Par exemple:

.. py2rst:: 

    from lino.api.doctest import *
    rt.show(jobs.ContractType)


- Pour les mises à l’emploi selon l'article 60§7, il faut
  spécifier s'il s'agit d'\ *économie sociale* ou non.
  Vous le faites en cochant la case correspondante dans cette liste.

  La *Mise à l’emploi* comprend deux types de mesures appelées *Art
  60§7* et *Art. 61*.


Candidatures
============   

- Une :class:`welfare.jobs.Candidature` représente le fait qu'un
  bénéficiaire donné voudrait travailler à un *poste de mise à l'emploi
  travail* donné.  Ceci implique entre autres que l'agent d'insertion
  responsable l'estime potentiellement apte à assumer ce travail.

Offres d'emploi externes
========================

Indépendamment de ces postes de mise à l'emploi, le CPAS peut gérer
une liste d'offres d'emploi venant du marché régulier.

