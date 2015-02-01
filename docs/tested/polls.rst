.. _welfare.tested.polls:

==================
Polls 
==================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_polls

A tour into the :mod:`lino_welfare.modlib.polls` plugin.

.. contents::
   :depth: 2


Recurrent polls
===============

A special feature of Lino's polls module are **recurrent polls**.

A recurrent poll is series of questions which the agent will ask their
client repeatedly at different dates. And when they fill in a new
response, they want to see the answers from previous meetings.

For example if they have worked through a poll already two times (a
first time in March and another time in April) and now they are doing
it a third time, they want to see:

=========================== =====  ===== =====================   
Question                    01/03  05/04 03/05
=========================== =====  ===== =====================   
1) Do you bla bla bla?      Yes    Yes   (Yes) (No) (Maybe)
2) And do you bla bla bla?  No     Maybe (Yes) (No) (Maybe)
=========================== =====  ===== =====================   


About this document
===================

.. include:: /include/tested.rst

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.chatelet.settings.doctests'
>>> from lino.api.doctest import *
    
This documents uses the :mod:`lino_welfare.projects.chatelet` test
database:

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.chatelet.settings.doctests

>>> dd.today()
datetime.date(2014, 5, 22)


Configuration data
========================

This is the list of choice sets:

>>> rt.login('romain').show(polls.ChoiceSets)
==== =====================
 ID   Description
---- ---------------------
 1    Yes/No
 2    Yes/Maybe/No
 3    That's it!...Never!
 4    -1..+1
 5    Acquis
 6    1...5
 7    1...10
 8    Temps de travail
==== =====================
<BLANKLINE>

>>> rt.login('romain').show(polls.Polls)
============================ =========================== ================= ========
 Créé                         Allocution                  Auteur            État
---------------------------- --------------------------- ----------------- --------
 2015-02-01 18:13:32.733205   Interview initial           Alicia Allmanns   Publié
 2015-02-01 18:13:32.767200   Recherche active d'emploi   Caroline Carnol   Publié
============================ =========================== ================= ========
<BLANKLINE>

>>> rt.login('romain').show(polls.Questions)
======================= ==== ======================================================================================================== ================== =========
 Questionnaire           No   Title                                                                                                    Liste de choix     Heading
----------------------- ---- -------------------------------------------------------------------------------------------------------- ------------------ ---------
 INI                          Pour commencer ma recherche d'emploi, je dois                                                                               Oui
 INI                     1    Avoir une farde de recherche d’emploi organisée                                                                             Non
 INI                     2    Réaliser mon curriculum vitae                                                                                               Non
 INI                     3    Savoir faire une lettre de motivation adaptée au poste de travail visé                                                      Non
 INI                     4    Respecter les modalités de candidature                                                                                      Non
 INI                     5    Me créer une boite e-mail appropriée à la recherche d’emploi                                                                Non
 INI                     6    Créer mon compte sur le site de Forem                                                                                       Non
 INI                     7    Mettre mon curriculum vitae sur le site du Forem                                                                            Non
 INI                     8    Connaître les aides à l’embauche qui me concernent                                                                          Non
 INI                     9    Etre préparé à l’entretien d’embauche ou téléphonique                                                                       Non
 INI                          Est-ce que je sais...                                                                                                       Oui
 INI                     1    Utiliser le site du Forem pour consulter les offres d’emploi                                                                Non
 INI                     2    Décoder une offre d’emploi                                                                                                  Non
 INI                     3    Adapter mon curriculum vitae par rapport à une offre ou pour une candidature spontanée                                      Non
 INI                     4    Réaliser une lettre de motivation suite à une offre d’emploi                                                                Non
 INI                     5    Adapter une lettre de motivation par rapport à l’offre d’emploi                                                             Non
 INI                     6    Réaliser une lettre de motivation spontanée                                                                                 Non
 INI                     7    Utiliser le fax pour envoyer mes candidatures                                                                               Non
 INI                     8    Utiliser ma boite e-mail pour envoyer mes candidatures                                                                      Non
 INI                     9    Mettre mon curriculum vitae en ligne sur des sites d’entreprise                                                             Non
 INI                     10   Compléter en ligne les formulaires de candidature                                                                           Non
 INI                     11   M’inscrire aux agences intérim via Internet                                                                                 Non
 INI                     12   M’inscrire auprès d’agence de recrutement via Internet                                                                      Non
 INI                     13   Utiliser Internet pour faire des recherches sur une entreprise                                                              Non
 INI                     14   Préparer un entretien d’embauche (questions, argumentation du C.V.,…)                                                       Non
 INI                     15   Utiliser Internet pour gérer ma mobilité (transport en commun ou itinéraire voiture)                                        Non
 INI                     16   Utiliser la photocopieuse (ex : copie de lettre de motivation que j’envoie par courrier)                                    Non
 INI                     17   Utiliser le téléphone pour poser ma candidature                                                                             Non
 INI                     18   Utiliser le téléphone pour relancer ma candidature                                                                          Non
 INI                     19   Trouver et imprimer les formulaires de demandes d’aides à l’embauche se trouvant sur le site de l’ONEm                      Non
 RAE                     1    Cherchez-vous du travail actuellement?                                                                                      Non
 RAE                     2    Avez-vous un CV à jour?                                                                                                     Non
 RAE                     3    Est-ce que vous vous présentez régulièrement au FOREM?                                                                      Non
 RAE                     4    Est-ce que vous consultez les petites annonces?                                                                             Non
 RAE                     5    Demande à l’entourage?                                                                                                      Non
 RAE                     6    Candidature spontanée?                                                                                                      Non
 RAE                     7    Avez-vous des antécédents judiciaires qui pourraient être préjudiciables à votre recherce d’emploi?                         Non
 RAE                          Temps de travail acceptés                                                                                Temps de travail   Non
 **Total (38 lignes)**                                                                                                                                    **2**
======================= ==== ======================================================================================================== ================== =========
<BLANKLINE>

>>> rt.login('romain').show(polls.Responses)
==== ================= =============== ============ ============ =================== ===========================
 ID   Auteur            Questionnaire   Date         État         Remarque générale   Partenaire
---- ----------------- --------------- ------------ ------------ ------------------- ---------------------------
 1    Hubert Huppertz   INI             03/03/2014   Enregistré                       Ausdemwald Alfons (115)
 2    Hubert Huppertz   RAE             03/03/2014   Enregistré                       Ausdemwald Alfons (115)
 3    Hubert Huppertz   RAE             02/04/2014   Enregistré                       Ausdemwald Alfons (115)
 5    Hubert Huppertz   INI             22/04/2014   Enregistré                       Bastiaensen Laurent (116)
 4    Hubert Huppertz   RAE             02/05/2014   Enregistré                       Ausdemwald Alfons (115)
 6    Hubert Huppertz   RAE             02/05/2014   Enregistré                       Bastiaensen Laurent (116)
==== ================= =============== ============ ============ =================== ===========================
<BLANKLINE>

