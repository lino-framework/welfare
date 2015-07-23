.. _welfare.tested.polls:

==================
Polls tested tour
==================

A tested tour into the :mod:`lino_welfare.modlib.polls` plugin.

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_polls

.. contents::
   :depth: 2


About this document
===================

.. include:: /include/tested.rst

This documents uses the :mod:`lino_welfare.projects.chatelet` test
database:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.chatelet.settings.doctests'
>>> from lino.api.doctest import *
    
>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.chatelet.settings.doctests

>>> dd.today()
datetime.date(2014, 5, 22)


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


Configuration
=============

>>> rt.show(polls.Polls)
=========== =========================== ============ ===========
 Reference   Heading                     Author       State
----------- --------------------------- ------------ -----------
 INI         Interview initial           Robin Rood   Published
 RAE         Recherche active d'emploi   Robin Rood   Published
=========== =========================== ============ ===========
<BLANKLINE>


>>> obj = polls.Poll.get_by_ref('INI')
>>> rt.show(polls.QuestionsByPoll, obj)
========= ===== ======================================================================================================== =========
 Seq.No.   No.   Title                                                                                                    Heading
--------- ----- -------------------------------------------------------------------------------------------------------- ---------
 1               Pour commencer ma recherche d'emploi, je dois                                                            Yes
 2         1     Avoir une farde de recherche d’emploi organisée                                                          No
 3         2     Réaliser mon curriculum vitae                                                                            No
 4         3     Savoir faire une lettre de motivation adaptée au poste de travail visé                                   No
 5         4     Respecter les modalités de candidature                                                                   No
 6         5     Me créer une boite e-mail appropriée à la recherche d’emploi                                             No
 7         6     Créer mon compte sur le site de Forem                                                                    No
 8         7     Mettre mon curriculum vitae sur le site du Forem                                                         No
 9         8     Connaître les aides à l’embauche qui me concernent                                                       No
 10        9     Etre préparé à l’entretien d’embauche ou téléphonique                                                    No
 11              Est-ce que je sais...                                                                                    Yes
 12        1     Utiliser le site du Forem pour consulter les offres d’emploi                                             No
 13        2     Décoder une offre d’emploi                                                                               No
 14        3     Adapter mon curriculum vitae par rapport à une offre ou pour une candidature spontanée                   No
 15        4     Réaliser une lettre de motivation suite à une offre d’emploi                                             No
 16        5     Adapter une lettre de motivation par rapport à l’offre d’emploi                                          No
 17        6     Réaliser une lettre de motivation spontanée                                                              No
 18        7     Utiliser le fax pour envoyer mes candidatures                                                            No
 19        8     Utiliser ma boite e-mail pour envoyer mes candidatures                                                   No
 20        9     Mettre mon curriculum vitae en ligne sur des sites d’entreprise                                          No
 21        10    Compléter en ligne les formulaires de candidature                                                        No
 22        11    M’inscrire aux agences intérim via Internet                                                              No
 23        12    M’inscrire auprès d’agence de recrutement via Internet                                                   No
 24        13    Utiliser Internet pour faire des recherches sur une entreprise                                           No
 25        14    Préparer un entretien d’embauche (questions, argumentation du C.V.,…)                                    No
 26        15    Utiliser Internet pour gérer ma mobilité (transport en commun ou itinéraire voiture)                     No
 27        16    Utiliser la photocopieuse (ex : copie de lettre de motivation que j’envoie par courrier)                 No
 28        17    Utiliser le téléphone pour poser ma candidature                                                          No
 29        18    Utiliser le téléphone pour relancer ma candidature                                                       No
 30        19    Trouver et imprimer les formulaires de demandes d’aides à l’embauche se trouvant sur le site de l’ONEm   No
 **465**                                                                                                                  **2**
========= ===== ======================================================================================================== =========
<BLANKLINE>

>>> obj = polls.Poll.get_by_ref('RAE')
>>> rt.show(polls.QuestionsByPoll, obj)
========= ===== ======================================================== =========
 Seq.No.   No.   Title                                                    Heading
--------- ----- -------------------------------------------------------- ---------
 1         1     Cherchez-vous du travail actuellement?                   No
 2         2     Avez-vous un CV à jour?                                  No
 3         3     Est-ce que vous vous présentez régulièrement au FOREM?   No
 4         4     Est-ce que vous consultez les petites annonces?          No
 5         5     Demande à l’entourage?                                   No
 6         6     Candidature spontanée?                                   No
 7         7     Antécédents judiciaires?                                 No
 8               Temps de travail acceptés                                No
 **36**                                                                   **0**
========= ===== ======================================================== =========
<BLANKLINE>

This is the list of choice sets:

>>> rt.show(polls.ChoiceSets)
==== ===================== ===================== =====================
 ID   Designation           Designation (fr)      Designation (de)
---- --------------------- --------------------- ---------------------
 1    Yes/No                Yes/No                Yes/No
 2    Yes/Maybe/No          Oui/Peut-être/Non     Yes/Maybe/No
 3    That's it!...Never!   That's it!...Never!   That's it!...Never!
 4    -1..+1                -1..+1                -1..+1
 5    Acquired              Acquis                Acquired
 6    1...5                 1...5                 1...5
 7    1...10                1...10                1...10
 8    Temps de travail
==== ===================== ===================== =====================
<BLANKLINE>




Responses
=========



>>> rt.login('romain').show(polls.Responses)
==== ================= ====== ========= ============ =================== =====================
 ID   Author            Poll   Date      State        My general remark   Partner
---- ----------------- ------ --------- ------------ ------------------- ---------------------
 1    Alicia Allmanns   INI    3/3/14    Registered                       Ausdemwald Alfons
 2    Alicia Allmanns   RAE    3/3/14    Registered                       Ausdemwald Alfons
 3    Alicia Allmanns   RAE    4/2/14    Draft                            Ausdemwald Alfons
 5    Alicia Allmanns   INI    4/22/14   Registered                       Bastiaensen Laurent
 4    Alicia Allmanns   RAE    5/2/14    Draft                            Ausdemwald Alfons
 6    Alicia Allmanns   RAE    5/2/14    Registered                       Bastiaensen Laurent
==== ================= ====== ========= ============ =================== =====================
<BLANKLINE>

>>> obj = polls.Response.objects.get(id=3)
>>> rt.login('alicia').show(polls.AnswersByResponse, obj)
Question *3/3/14* 4/2/14 *5/2/14* 
<BLANKLINE>
1) Cherchez-vous du travail actuellement? Yes
 ****[Yes]**** **Maybe** **No** (**Remark**)
 Yes
<BLANKLINE>
2) Avez-vous un CV à jour? Maybe
 **Yes** ****[Maybe]**** **No** (**Remark**)
 Maybe
<BLANKLINE>
3) Est-ce que vous vous présentez régulièrement au FOREM? No
 **Yes** **Maybe** ****[No]**** (**Remark**)
 No
<BLANKLINE>
4) Est-ce que vous consultez les petites annonces? Yes
 ****[Yes]**** **Maybe** **No** (**Remark**)
 Yes
<BLANKLINE>
5) Demande à l’entourage? Maybe
 **Yes** ****[Maybe]**** **No** (**Remark**)
 Maybe
<BLANKLINE>
6) Candidature spontanée? No
 **Yes** **Maybe** ****[No]**** (**Remark**)
 No
<BLANKLINE>
7) Antécédents judiciaires? Yes
 ****[Yes]**** **Maybe** **No** (**Remark**)
 Yes
<BLANKLINE>
Temps de travail acceptés 3/4
 **temps-plein** ****[3/4]**** **1/2** **quelques heures par semaine** (**Remark**)
 3/4
<BLANKLINE>
<BLANKLINE>

>>> rt.login('alicia').show(polls.AnswersByResponse, obj, nosummary=True)
=========================================================== ======================================================================= ===========
 Question                                                    My answer                                                               My remark
----------------------------------------------------------- ----------------------------------------------------------------------- -----------
 1) Cherchez-vous du travail actuellement?                   ****[Yes]**** **Maybe** **No**
 2) Avez-vous un CV à jour?                                  **Yes** ****[Maybe]**** **No**
 3) Est-ce que vous vous présentez régulièrement au FOREM?   **Yes** **Maybe** ****[No]****
 4) Est-ce que vous consultez les petites annonces?          ****[Yes]**** **Maybe** **No**
 5) Demande à l’entourage?                                   **Yes** ****[Maybe]**** **No**
 6) Candidature spontanée?                                   **Yes** **Maybe** ****[No]****
 7) Antécédents judiciaires?                                 ****[Yes]**** **Maybe** **No**
 Temps de travail acceptés                                   **temps-plein** ****[3/4]**** **1/2** **quelques heures par semaine**
=========================================================== ======================================================================= ===========
<BLANKLINE>

When Hubert looks at the same response, he cannot edit it because he
is not the author:

>>> rt.login('hubert').show(polls.AnswersByResponse, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Question *3/3/14* 4/2/14 *5/2/14* 
<BLANKLINE>
1) Cherchez-vous du travail actuellement? Yes
 Yes
 Yes
<BLANKLINE>
2) Avez-vous un CV à jour? Maybe
 Maybe
 Maybe
<BLANKLINE>
3) Est-ce que vous vous présentez régulièrement au FOREM? No
 No
 No
<BLANKLINE>
4) Est-ce que vous consultez les petites annonces? Yes
 Yes
 Yes
<BLANKLINE>
5) Demande à l’entourage? Maybe
 Maybe
 Maybe
<BLANKLINE>
6) Candidature spontanée? No
 No
 No
<BLANKLINE>
7) Antécédents judiciaires? Yes
 Yes
 Yes
<BLANKLINE>
Temps de travail acceptés 3/4
 3/4
 3/4
<BLANKLINE>
<BLANKLINE>

>>> rt.login('hubert').show(polls.AnswersByResponse, obj, nosummary=True)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
=========================================================== =========== ===========
 Question                                                    My answer   My remark
----------------------------------------------------------- ----------- -----------
 1) Cherchez-vous du travail actuellement?                   Yes
 2) Avez-vous un CV à jour?                                  Maybe
 3) Est-ce que vous vous présentez régulièrement au FOREM?   No
 4) Est-ce que vous consultez les petites annonces?          Yes
 5) Demande à l’entourage?                                   Maybe
 6) Candidature spontanée?                                   No
 7) Antécédents judiciaires?                                 Yes
 Temps de travail acceptés                                   3/4
=========================================================== =========== ===========
<BLANKLINE>
