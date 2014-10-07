===============================
Insertion socio-professionnelle
===============================

Ce module permet de gérer des projects de mise au travail selon les
articles 60§7 et 61 de la loi organique des CPAS.

Si pour des jeunes en-dessous des 25 ans on parle surtout
d'**insertion sociale** et de leur *enseignement*, pour les adultes
nous parlons d'**insertion socio-professionnelle** et nous concentrons
au **travail**.

Aperçu
======

Le CPAS gère une liste d'**endroits de mise au travail**.  Ces
endroits de mise au travail sont généralement des endroits de travail
spécialisés à l'accqueil temporaire de personnes à intégrer.  Exemple:

.. django2rst:: 

    rt.show(jobs.Jobs.request(limit=4))
    

Indépendamment de ces endroits de travail le CPAS peut gérer une liste
d'offres d'emploi venant du marché régulier.

- Une :class:`welfare.jobs.Candidature` représente le fait qu'un
  bénéficiaire donné voudrait travailler à un *endroit de mise au
  travail* donné.  Ceci implique entre autres que l'agent d'insertion
  responsable l'estime potentiellement apte à assumer ce travail.

- Article 60§7 : dans une administration publique, asbl, ou entreprise
  d'économie sociale.

- Article 61 : dans une entreprise privée

- Lino appelle "employant" l'entreprise (Art 61) ou l'organisme (60§7)
  dans laquelle le travail a lieu.

