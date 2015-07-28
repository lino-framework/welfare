.. _welfare.specs.polls:

==================
Polls tested tour
==================

A tested tour into the :mod:`lino_welfare.modlib.polls` plugin.

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_polls

    doctest init:
    
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.chatelet.settings.doctests'
    >>> from lino.api.doctest import *

.. contents::
   :depth: 2


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
=========== =========================== ============ ========
 Référence   Titre                       Auteur       État
----------- --------------------------- ------------ --------
 INI         Interview initial           Robin Rood   Publié
 RAE         Recherche active d'emploi   Robin Rood   Publié
=========== =========================== ============ ========
<BLANKLINE>

>>> obj = polls.Poll.get_by_ref('INI')
>>> rt.show(polls.QuestionsByPoll, obj)
=========== ==== ======================================================================================================== =======
 N° de séq   No   Title                                                                                                    Titre
----------- ---- -------------------------------------------------------------------------------------------------------- -------
 1                Pour commencer ma recherche d'emploi, je dois                                                            Oui
 2           1    Avoir une farde de recherche d’emploi organisée                                                          Non
 3           2    Réaliser mon curriculum vitae                                                                            Non
 4           3    Savoir faire une lettre de motivation adaptée au poste de travail visé                                   Non
 5           4    Respecter les modalités de candidature                                                                   Non
 6           5    Me créer une boite e-mail appropriée à la recherche d’emploi                                             Non
 7           6    Créer mon compte sur le site de Forem                                                                    Non
 8           7    Mettre mon curriculum vitae sur le site du Forem                                                         Non
 9           8    Connaître les aides à l’embauche qui me concernent                                                       Non
 10          9    Etre préparé à l’entretien d’embauche ou téléphonique                                                    Non
 11               Est-ce que je sais...                                                                                    Oui
 12          1    Utiliser le site du Forem pour consulter les offres d’emploi                                             Non
 13          2    Décoder une offre d’emploi                                                                               Non
 14          3    Adapter mon curriculum vitae par rapport à une offre ou pour une candidature spontanée                   Non
 15          4    Réaliser une lettre de motivation suite à une offre d’emploi                                             Non
 16          5    Adapter une lettre de motivation par rapport à l’offre d’emploi                                          Non
 17          6    Réaliser une lettre de motivation spontanée                                                              Non
 18          7    Utiliser le fax pour envoyer mes candidatures                                                            Non
 19          8    Utiliser ma boite e-mail pour envoyer mes candidatures                                                   Non
 20          9    Mettre mon curriculum vitae en ligne sur des sites d’entreprise                                          Non
 21          10   Compléter en ligne les formulaires de candidature                                                        Non
 22          11   M’inscrire aux agences intérim via Internet                                                              Non
 23          12   M’inscrire auprès d’agence de recrutement via Internet                                                   Non
 24          13   Utiliser Internet pour faire des recherches sur une entreprise                                           Non
 25          14   Préparer un entretien d’embauche (questions, argumentation du C.V.,…)                                    Non
 26          15   Utiliser Internet pour gérer ma mobilité (transport en commun ou itinéraire voiture)                     Non
 27          16   Utiliser la photocopieuse (ex : copie de lettre de motivation que j’envoie par courrier)                 Non
 28          17   Utiliser le téléphone pour poser ma candidature                                                          Non
 29          18   Utiliser le téléphone pour relancer ma candidature                                                       Non
 30          19   Trouver et imprimer les formulaires de demandes d’aides à l’embauche se trouvant sur le site de l’ONEm   Non
 **465**                                                                                                                   **2**
=========== ==== ======================================================================================================== =======
<BLANKLINE>

>>> obj = polls.Poll.get_by_ref('RAE')
>>> rt.show(polls.QuestionsByPoll, obj)
=========== ==== ======================================================== =======
 N° de séq   No   Title                                                    Titre
----------- ---- -------------------------------------------------------- -------
 1           1    Cherchez-vous du travail actuellement?                   Non
 2           2    Avez-vous un CV à jour?                                  Non
 3           3    Est-ce que vous vous présentez régulièrement au FOREM?   Non
 4           4    Est-ce que vous consultez les petites annonces?          Non
 5           5    Demande à l’entourage?                                   Non
 6           6    Candidature spontanée?                                   Non
 7           7    Antécédents judiciaires?                                 Non
 8                Temps de travail acceptés                                Non
 **36**                                                                    **0**
=========== ==== ======================================================== =======
<BLANKLINE>

This is the list of choice sets:

>>> rt.show(polls.ChoiceSets)
==== ===================== ===================== =====================
 ID   Description           Description (de)      Description (en)
---- --------------------- --------------------- ---------------------
 1    Yes/No                Yes/No                Yes/No
 2    Oui/Peut-être/Non     Yes/Maybe/No          Yes/Maybe/No
 3    That's it!...Never!   That's it!...Never!   That's it!...Never!
 4    -1..+1                -1..+1                -1..+1
 5    Acquis                Acquired              Acquired
 6    1...5                 1...5                 1...5
 7    1...10                1...10                1...10
 8    Temps de travail
==== ===================== ===================== =====================
<BLANKLINE>




Responses
=========


>>> rt.login('romain').show(polls.Responses)
==== ================= =============== ============ ============ =================== =====================
 ID   Auteur            Questionnaire   Date         État         Remarque générale   Partenaire
---- ----------------- --------------- ------------ ------------ ------------------- ---------------------
 1    Alicia Allmanns   INI             03/03/2014   Enregistré                       Ausdemwald Alfons
 2    Alicia Allmanns   RAE             03/03/2014   Enregistré                       Ausdemwald Alfons
 3    Alicia Allmanns   RAE             02/04/2014   Brouillon                        Ausdemwald Alfons
 5    Alicia Allmanns   INI             22/04/2014   Enregistré                       Bastiaensen Laurent
 4    Alicia Allmanns   RAE             02/05/2014   Brouillon                        Ausdemwald Alfons
 6    Alicia Allmanns   RAE             02/05/2014   Enregistré                       Bastiaensen Laurent
==== ================= =============== ============ ============ =================== =====================
<BLANKLINE>

>>> obj = polls.Response.objects.get(id=3)
>>> rt.login('alicia').show(polls.AnswersByResponse, obj)
Question *03/03/2014* 02/04/2014 *02/05/2014* 
<BLANKLINE>
1) Cherchez-vous du travail actuellement? Oui
 ****[Oui]**** **Peut-être** **Non** (**Remarque**)
 Oui
<BLANKLINE>
2) Avez-vous un CV à jour? Peut-être
 **Oui** ****[Peut-être]**** **Non** (**Remarque**)
 Peut-être
<BLANKLINE>
3) Est-ce que vous vous présentez régulièrement au FOREM? Non
 **Oui** **Peut-être** ****[Non]**** (**Remarque**)
 Non
<BLANKLINE>
4) Est-ce que vous consultez les petites annonces? Oui
 ****[Oui]**** **Peut-être** **Non** (**Remarque**)
 Oui
<BLANKLINE>
5) Demande à l’entourage? Peut-être
 **Oui** ****[Peut-être]**** **Non** (**Remarque**)
 Peut-être
<BLANKLINE>
6) Candidature spontanée? Non
 **Oui** **Peut-être** ****[Non]**** (**Remarque**)
 Non
<BLANKLINE>
7) Antécédents judiciaires? Oui
 ****[Oui]**** **Peut-être** **Non** (**Remarque**)
 Oui
<BLANKLINE>
Temps de travail acceptés 3/4
 **temps-plein** ****[3/4]**** **1/2** **quelques heures par semaine** (**Remarque**)
 3/4

>>> rt.login('alicia').show(polls.AnswersByResponse, obj, nosummary=True)
=========================================================== ======================================================================= =============
 Question                                                    Ma réponse                                                              Ma remarque
----------------------------------------------------------- ----------------------------------------------------------------------- -------------
 1) Cherchez-vous du travail actuellement?                   ****[Oui]**** **Peut-être** **Non**
 2) Avez-vous un CV à jour?                                  **Oui** ****[Peut-être]**** **Non**
 3) Est-ce que vous vous présentez régulièrement au FOREM?   **Oui** **Peut-être** ****[Non]****
 4) Est-ce que vous consultez les petites annonces?          ****[Oui]**** **Peut-être** **Non**
 5) Demande à l’entourage?                                   **Oui** ****[Peut-être]**** **Non**
 6) Candidature spontanée?                                   **Oui** **Peut-être** ****[Non]****
 7) Antécédents judiciaires?                                 ****[Oui]**** **Peut-être** **Non**
 Temps de travail acceptés                                   **temps-plein** ****[3/4]**** **1/2** **quelques heures par semaine**
=========================================================== ======================================================================= =============
<BLANKLINE>

When Hubert looks at the same response, he cannot edit it because he
is not the author:

>>> rt.login('hubert').show(polls.AnswersByResponse, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Question *03/03/2014* 02/04/2014 *02/05/2014* 
<BLANKLINE>
1) Cherchez-vous du travail actuellement? Oui
 Oui
 Oui
<BLANKLINE>
2) Avez-vous un CV à jour? Peut-être
 Peut-être
 Peut-être
<BLANKLINE>
3) Est-ce que vous vous présentez régulièrement au FOREM? Non
 Non
 Non
<BLANKLINE>
4) Est-ce que vous consultez les petites annonces? Oui
 Oui
 Oui
<BLANKLINE>
5) Demande à l’entourage? Peut-être
 Peut-être
 Peut-être
<BLANKLINE>
6) Candidature spontanée? Non
 Non
 Non
<BLANKLINE>
7) Antécédents judiciaires? Oui
 Oui
 Oui
<BLANKLINE>
Temps de travail acceptés 3/4
 3/4
 3/4


>>> rt.login('hubert').show(polls.AnswersByResponse, obj, nosummary=True)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
=========================================================== ============ =============
 Question                                                    Ma réponse   Ma remarque
----------------------------------------------------------- ------------ -------------
 1) Cherchez-vous du travail actuellement?                   Oui
 2) Avez-vous un CV à jour?                                  Peut-être
 3) Est-ce que vous vous présentez régulièrement au FOREM?   Non
 4) Est-ce que vous consultez les petites annonces?          Oui
 5) Demande à l’entourage?                                   Peut-être
 6) Candidature spontanée?                                   Non
 7) Antécédents judiciaires?                                 Oui
 Temps de travail acceptés                                   3/4
=========================================================== ============ =============
<BLANKLINE>
