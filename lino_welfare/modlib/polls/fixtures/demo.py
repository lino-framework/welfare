# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds a series of polls used by intergration agents to interview
their clients who start an "active job search" project ("recherche
active d'emploi").

Adds some fictive responses to these polls.

"""

from __future__ import unicode_literals

from django.conf import settings
from lino.api import dd, rt, _
from lino.utils import Cycler


def demo_polls():

    polls = rt.models.polls

    name = dd.str2kw('name', _("Acquired"))['name']
    acquired = polls.ChoiceSet.objects.get(name=name)

    name = dd.str2kw('name', _("Yes/Maybe/No"))['name']
    yesmaybeno = polls.ChoiceSet.objects.get(name=name)

    robin = settings.SITE.user_model.objects.get(username="robin")

    def poll(ref, choiceset, title, details, questions):
        obj = polls.Poll(
            user=robin,
            ref=ref,
            title=title.strip(),
            details=details.strip(),
            state=polls.PollStates.active,
            questions_to_add=questions,
            default_choiceset=choiceset)
        obj.full_clean()
        obj.save()
        obj.after_ui_save(None, None)
        return obj

    yield poll(
        "INI", acquired,
        "Interview initial", """
À remplir lors de la première entrevue.
""", """
=Pour commencer ma recherche d'emploi, je dois
#Veuillez sélectionner votre réponse pour chaque question
Avoir une farde de recherche d’emploi organisée
Réaliser mon curriculum vitae
#Sinon, faites-vous aider par votre agent d'insertion.
Savoir faire une lettre de motivation adaptée au poste de travail visé
Respecter les modalités de candidature
Me créer une boite e-mail appropriée à la recherche d’emploi
Créer mon compte sur le site de Forem
Mettre mon curriculum vitae sur le site du Forem
Connaître les aides à l’embauche qui me concernent
Etre préparé à l’entretien d’embauche ou téléphonique

=Est-ce que je sais...
#Veuillez sélectionner votre réponse pour chaque question
Utiliser le site du Forem pour consulter les offres d’emploi
Décoder une offre d’emploi
Adapter mon curriculum vitae par rapport à une offre ou pour une candidature spontanée
Réaliser une lettre de motivation suite à une offre d’emploi
Adapter une lettre de motivation par rapport à l’offre d’emploi
Réaliser une lettre de motivation spontanée
Utiliser le fax pour envoyer mes candidatures
Utiliser ma boite e-mail pour envoyer mes candidatures
Mettre mon curriculum vitae en ligne sur des sites d’entreprise
Compléter en ligne les formulaires de candidature
M’inscrire aux agences intérim via Internet
M’inscrire auprès d’agence de recrutement via Internet
Utiliser Internet pour faire des recherches sur une entreprise
Préparer un entretien d’embauche (questions, argumentation du C.V.,…)
Utiliser Internet pour gérer ma mobilité (transport en commun ou itinéraire voiture)
Utiliser la photocopieuse (ex : copie de lettre de motivation que j’envoie par courrier)
Utiliser le téléphone pour poser ma candidature
Utiliser le téléphone pour relancer ma candidature
Trouver et imprimer les formulaires de demandes d’aides à l’embauche se trouvant sur le site de l’ONEm
""")

    rae = poll(
        "RAE",
        yesmaybeno,
        "Recherche active d'emploi", """
Veuillez sélectionner votre réponse pour chaque question
""", """
Cherchez-vous du travail actuellement?
Avez-vous un CV à jour?
Est-ce que vous vous présentez régulièrement au FOREM?
Est-ce que vous consultez les petites annonces?
Demande à l’entourage?
#Demandez-vous à vos connaissances s'ils connaissent quelqu'un qui connait...?
Candidature spontanée?
#Avez-vous fait des candidatures spontanées depuis notre dernière entrevue?
Antécédents judiciaires?
#Avez-vous des antécédents judiciaires qui pourraient \
être préjudiciables à votre recherce d’emploi?
""")

    yield rae
    temps = polls.ChoiceSet(name="Temps de travail")
    yield temps
    for s in """
    temps-plein
    3/4
    1/2
    quelques heures par semaine
    """.splitlines():
        s = s.strip()
        if s:
            yield polls.Choice(choiceset=temps, name=s)
    yield polls.Question(title="Temps de travail acceptés", poll=rae,
                         choiceset=temps, multiple_choices=True)


def demo_responses():

    pcsw = rt.models.pcsw
    polls = rt.models.polls
    PARTNERS = Cycler(pcsw.Client.objects.all())
    alicia = settings.SITE.user_model.objects.get(username="alicia")

    def response(date_offset, isreg, partner, poll):

        kw = dict(poll=poll)
        if isreg:
            kw.update(state=polls.ResponseStates.registered)
        kw.update(date=settings.SITE.demo_date(date_offset))
        kw.update(partner=partner)
        kw.update(user=alicia)
        r = polls.Response(**kw)
        yield r
        i = 0
        for q in polls.Question.objects.filter(poll=poll):
            cs = q.get_choiceset()
            if cs is not None:
                choices = cs.choices.all()
                i = i % choices.count()
                c = choices[i]
                yield polls.AnswerChoice(response=r, question=q, choice=c)
                i += 1

    first = rt.models.polls.Poll.get_by_ref("INI")
    rae = rt.models.polls.Poll.get_by_ref("RAE")

    p = PARTNERS.pop()
    yield response(-80, True, p, first)
    yield response(-80, True, p, rae)
    yield response(-50, False, p, rae)
    yield response(-20, False, p, rae)

    p = PARTNERS.pop()
    yield response(-30, True, p, first)
    yield response(-20, True, p, rae)


def objects():
    yield demo_polls()
    yield demo_responses()
