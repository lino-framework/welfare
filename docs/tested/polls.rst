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
==== ===================== ===================== =====================
 ID   Designation           Designation (fr)      Designation (de)
---- --------------------- --------------------- ---------------------
 1    Yes/No                Yes/No                Yes/No
 2    Yes/Maybe/No          Yes/Maybe/No          Yes/Maybe/No
 3    That's it!...Never!   That's it!...Never!   That's it!...Never!
 4    -1..+1                -1..+1                -1..+1
 5    Acquired              Acquis                Acquired
 6    1...5                 1...5                 1...5
 7    1...10                1...10                1...10
 8    Temps de travail
==== ===================== ===================== =====================
<BLANKLINE>


>>> rt.login('romain').show(polls.Polls)
=========== =========================== ================= ===========
 Reference   Title                       Author            State
----------- --------------------------- ----------------- -----------
 INI         Interview initial           Alicia Allmanns   Published
 RAE         Recherche active d'emploi   Caroline Carnol   Published
=========== =========================== ================= ===========
<BLANKLINE>

>>> rt.login('romain').show(polls.Questions)
===================== ===== ======================================================================================================== ================== =========
 Poll                  No.   Title                                                                                                    Choice Set         Heading
--------------------- ----- -------------------------------------------------------------------------------------------------------- ------------------ ---------
 INI                         Pour commencer ma recherche d'emploi, je dois                                                                               Yes
 INI                   1     Avoir une farde de recherche d’emploi organisée                                                                             No
 INI                   2     Réaliser mon curriculum vitae                                                                                               No
 INI                   3     Savoir faire une lettre de motivation adaptée au poste de travail visé                                                      No
 INI                   4     Respecter les modalités de candidature                                                                                      No
 INI                   5     Me créer une boite e-mail appropriée à la recherche d’emploi                                                                No
 INI                   6     Créer mon compte sur le site de Forem                                                                                       No
 INI                   7     Mettre mon curriculum vitae sur le site du Forem                                                                            No
 INI                   8     Connaître les aides à l’embauche qui me concernent                                                                          No
 INI                   9     Etre préparé à l’entretien d’embauche ou téléphonique                                                                       No
 INI                         Est-ce que je sais...                                                                                                       Yes
 INI                   1     Utiliser le site du Forem pour consulter les offres d’emploi                                                                No
 INI                   2     Décoder une offre d’emploi                                                                                                  No
 INI                   3     Adapter mon curriculum vitae par rapport à une offre ou pour une candidature spontanée                                      No
 INI                   4     Réaliser une lettre de motivation suite à une offre d’emploi                                                                No
 INI                   5     Adapter une lettre de motivation par rapport à l’offre d’emploi                                                             No
 INI                   6     Réaliser une lettre de motivation spontanée                                                                                 No
 INI                   7     Utiliser le fax pour envoyer mes candidatures                                                                               No
 INI                   8     Utiliser ma boite e-mail pour envoyer mes candidatures                                                                      No
 INI                   9     Mettre mon curriculum vitae en ligne sur des sites d’entreprise                                                             No
 INI                   10    Compléter en ligne les formulaires de candidature                                                                           No
 INI                   11    M’inscrire aux agences intérim via Internet                                                                                 No
 INI                   12    M’inscrire auprès d’agence de recrutement via Internet                                                                      No
 INI                   13    Utiliser Internet pour faire des recherches sur une entreprise                                                              No
 INI                   14    Préparer un entretien d’embauche (questions, argumentation du C.V.,…)                                                       No
 INI                   15    Utiliser Internet pour gérer ma mobilité (transport en commun ou itinéraire voiture)                                        No
 INI                   16    Utiliser la photocopieuse (ex : copie de lettre de motivation que j’envoie par courrier)                                    No
 INI                   17    Utiliser le téléphone pour poser ma candidature                                                                             No
 INI                   18    Utiliser le téléphone pour relancer ma candidature                                                                          No
 INI                   19    Trouver et imprimer les formulaires de demandes d’aides à l’embauche se trouvant sur le site de l’ONEm                      No
 RAE                   1     Cherchez-vous du travail actuellement?                                                                                      No
 RAE                   2     Avez-vous un CV à jour?                                                                                                     No
 RAE                   3     Est-ce que vous vous présentez régulièrement au FOREM?                                                                      No
 RAE                   4     Est-ce que vous consultez les petites annonces?                                                                             No
 RAE                   5     Demande à l’entourage?                                                                                                      No
 RAE                   6     Candidature spontanée?                                                                                                      No
 RAE                   7     Avez-vous des antécédents judiciaires qui pourraient être préjudiciables à votre recherce d’emploi?                         No
 RAE                         Temps de travail acceptés                                                                                Temps de travail   No
 **Total (38 rows)**                                                                                                                                     **2**
===================== ===== ======================================================================================================== ================== =========
<BLANKLINE>

>>> rt.login('romain').show(polls.Responses)
==== ================= ====== ========= ============ =================== ===========================
 ID   Author            Poll   Date      State        My general remark   Partner
---- ----------------- ------ --------- ------------ ------------------- ---------------------------
 1    Hubert Huppertz   INI    3/3/14    Registered                       Ausdemwald Alfons (115)
 2    Hubert Huppertz   RAE    3/3/14    Registered                       Ausdemwald Alfons (115)
 3    Hubert Huppertz   RAE    4/2/14    Registered                       Ausdemwald Alfons (115)
 5    Hubert Huppertz   INI    4/22/14   Registered                       Bastiaensen Laurent (116)
 4    Hubert Huppertz   RAE    5/2/14    Registered                       Ausdemwald Alfons (115)
 6    Hubert Huppertz   RAE    5/2/14    Registered                       Bastiaensen Laurent (116)
==== ================= ====== ========= ============ =================== ===========================
<BLANKLINE>

>>> obj = polls.Response.objects.get(id=3)
>>> #polls.AnswersByResponse.show(obj)
>>> rt.login('romain').show(polls.AnswersByResponse, obj)
======================================================================================================== ======================================================================= ===========
 Question                                                                                                 My answer                                                               My remark
-------------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------- -----------
 1) Cherchez-vous du travail actuellement?                                                                ****[Yes]**** **Maybe** **No**
 2) Avez-vous un CV à jour?                                                                               **Yes** ****[Maybe]**** **No**
 3) Est-ce que vous vous présentez régulièrement au FOREM?                                                **Yes** **Maybe** ****[No]****
 4) Est-ce que vous consultez les petites annonces?                                                       ****[Yes]**** **Maybe** **No**
 5) Demande à l’entourage?                                                                                **Yes** ****[Maybe]**** **No**
 6) Candidature spontanée?                                                                                **Yes** **Maybe** ****[No]****
 7) Avez-vous des antécédents judiciaires qui pourraient être préjudiciables à votre recherce d’emploi?   ****[Yes]**** **Maybe** **No**
 Temps de travail acceptés                                                                                **temps-plein** ****[3/4]**** **1/2** **quelques heures par semaine**
======================================================================================================== ======================================================================= ===========
<BLANKLINE>
