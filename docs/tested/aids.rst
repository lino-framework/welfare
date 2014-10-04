.. _welfare.tested.aids:

============
Beihilfen
============

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_aids

.. include:: /include/tested.rst

..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.docs.settings.test'
    >>> from bs4 import BeautifulSoup
    >>> from lino.utils import i2d
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.runtime import *
    >>> from django.test import Client
    >>> from django.utils import translation
    >>> import json
    >>> client = Client()




>>> ses = rt.login('rolf')
>>> translation.activate('de')

Die Demo-Datenbank ist datiert auf den 22. Mai 2014:

>>> print(dd.fdl(dd.demo_date()))
22. Mai 2014

Beschlüsse und Bestätigungen
============================

Hilfe\ *bestätigungen* (:class:`welfare.aids.Confirmation`) sind
"Konkretisierungen" oder "Präzisierungen" eines Hilfe\ *beschlusses*
(:class:`welfare.aids.Granting`). Der Beschluss ist sozusagen die
Erlaubnis oder Grundlage, Bestätigungen für eine bestimmte Hilfeart
auszuhändigen.  Beschlüsse sind *langfristig* und *allgemein*,
Bestätigungen sind *befristet* und *konkret*.

Zum Beispiel steht der monatliche Betrag eines
*Eingliederungseinkommens* nicht im *Beschluss*, sondern nur in der
*Bestätigung*, weil der sich im Laufe der Zeit ändern kann.

Oder wenn jemand Anrecht auf *Übernahme von Arzt- und
Medikamentenkosten* hat, ist das ein *Beschluss*. Um daraus eine
*Bescheinigung* zu machen, muss man auch *Apotheke* und *Arzt*
angeben.


Hilfearten
==========

Hier eine Liste der Hilfearten, die Lino kennt:

>>> ses.show(aids.AidTypes, column_names="name confirmed_by_primary_coach")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
========================= ================================= ================================================= ===========================
 Bezeichnung               Bezeichnung (fr)                  Bezeichnung (de)                                  Primärbegleiter bestätigt
------------------------- --------------------------------- ------------------------------------------------- ---------------------------
 Ausländerbeihilfe         Aide aux immigrants               Ausländerbeihilfe                                 Ja
 DMH-Übernahmeschein       DMH-Übernahmeschein               DMH-Übernahmeschein                               Ja
 Eingliederungseinkommen   Revenu d'intégration              Eingliederungseinkommen                           Ja
 Erstattung                Remboursement                     Erstattung                                        Ja
 Feste Beihilfe            Revenu fixe                       Feste Beihilfe                                    Ja
 Food bank                 Banque alimentaire                Lebensmittelbank                                  Nein
 Heizkosten                                                                                                    Ja
 Medical costs             Remboursement de frais médicaux   Übernahme von Arzt- und/oder Medikamentenkosten   Ja
 Möbellager                                                                                                    Ja
 Übernahmeschein           Übernahmeschein                   Übernahmeschein                                   Ja
 **Total (10 Zeilen)**                                                                                         **9**
========================= ================================= ================================================= ===========================
<BLANKLINE>


Hilfebeschlüsse (:class:`welfare.aids.Granting`)
================================================

Alicia hat 2 Hilfebestätigungen zu unterschreiben. Dies kriegt sie als
Willkommensmeldung unter die Nase gerieben:

>>> ses = rt.login('alicia')
>>> translation.activate('de')
>>> for msg in settings.SITE.get_welcome_messages(ses):
...     print(E.tostring(msg))
<span>Du bist besch&#228;ftigt mit <b>Collard Charlotte (117)</b>.</span>
<span>Du hast 2 Eintr&#228;ge in <i>Zu unterschreibende Hilfebest&#228;tigungen</i>.</span>

>>> ses.show(aids.MyPendingGrantings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================ ================= ============== ===== ======= ================================
 Klient                       Hilfeart          Laufzeit von   bis   Autor   Arbeitsablauf
---------------------------- ----------------- -------------- ----- ------- --------------------------------
 EMONTS-GAST Erna (151)       Möbellager        29.05.14                     **Unbestätigt** → [Bestätigen]
 DOBBELSTEIN Dorothée (123)   Übernahmeschein   26.05.14                     **Unbestätigt** → [Bestätigen]
============================ ================= ============== ===== ======= ================================
<BLANKLINE>


Hilfebestätigungen
=======================================================


>>> translation.activate('de')

Hier eine Liste aller bisher vorgesehenen Bescheinigungstexte:

>>> for at in aids.AidType.objects.exclude(confirmation_type=''):
...    M = at.confirmation_type.model
...    qs = M.objects.filter(granting__aid_type=at)
...    obj = qs[0]
...    txt = obj.confirmation_text(ses)
...    txt = ' '.join(txt.split())
...    print("%s : %s" % (unicode(at), txt))
Eingliederungseinkommen : vom <b>23. Mai 2014</b> bis zum <b>24. Mai 2014</b> das durch Gesetz vom 26. Mai 2002 eingeführte <b>Eingliederungseinkommen</b> in Höhe von <b>123,00 €/Monat</b> (Kategorie: <b>Zusammenlebend</b>) bezieht.
Ausländerbeihilfe : vom <b>24. Mai 2014</b> bis zum <b>25. Mai 2014</b> eine laut Gesetz vom 2. April 1965 eingeführte <b>Sozialhilfe für Ausländer</b> in Höhe von <b>234,00 €/Monat</b> (Kategorie: <b>Alleinstehend</b>) bezieht
Feste Beihilfe : vom <b>25. Mai 2014</b> bis zum <b>26. Mai 2014</b> eine feste Beihilfe bezieht.
Erstattung : vom <b>26. Mai 2014</b> bis zum <b>27. Mai 2014</b> Erstattung erhält.
Übernahmeschein : vom <b>27. Mai 2014</b> bis zum <b>28. Mai 2014</b> Übernahmeschein erhält.
Übernahme von Arzt- und/oder Medikamentenkosten : für den Zeitraum vom <b>28. Mai 2014</b> bis zum <b>29. Mai 2014</b> Anrecht auf Übernahme folgender <b>Arzt- und/oder Medikamentenkosten</b> durch das ÖSHZ hatte: <ul><li><b>Arzthonorare</b> in Höhe der LIKIV-Tarife für die Visite beim Arzt <b>Waltraud Waldmann</b>. </li><li><b>Arzneikosten</b> für die durch <b>Waltraud Waldmann</b> verschriebenen und <b>Apotheke Reul</b> ausgehändigten Medikamente. </li></ul> Falls weitere Behandlungen notwendig sind, benötigen wir unbedingt einen Kostenvoranschlag. Danke.
DMH-Übernahmeschein : vom <b>29. Mai 2014</b> bis zum <b>30. Mai 2014</b> DMH-Übernahmeschein erhält.
Möbellager : vom <b>30. Mai 2014</b> bis zum <b>31. Mai 2014</b> Möbellager erhält.
Heizkosten : vom <b>31. Mai 2014</b> bis zum <b>1. Juni 2014</b> Heizkosten erhält.
Lebensmittelbank : vom <b>1. Juni 2014</b> bis zum <b>2. Juni 2014</b> aus Gründen der sozial-finanziellen Lage Anrecht auf eine Sozialhilfe in Naturalien durch Nutzung der Lebensmittelbank hatte.


Diese Texte sind generiert aus Vorlagen, die in der Datenbank stehen.
Die Hilfeart "Eingliederungseinkommen" zum Beispiel hat folgende Vorlage:

>>> at = aids.AidType.objects.get(short_name="EiEi")
>>> print(at.get_confirmation_template())
{{when}} das durch Gesetz vom 26. Mai 2002 eingeführte
<b>Eingliederungseinkommen</b>
{%- if obj.amount %}
in Höhe von <b>{{decfmt(obj.amount)}} €/Monat</b>
{% endif -%}
{%- if obj.category %}
(Kategorie: <b>{{obj.category}}</b>)
{% endif -%}
{{iif(past, "bezogen hat", "bezieht")}}.
<BLANKLINE>


Für die Hilfearten aus obiger Liste, für die eine Vorlage definiert
ist (also für wir nicht bloß den generischen Bestätigungstext haben)
hier die gleichen Texte als HTML:

.. django2rst::

    from django.utils import translation
    ses = rt.login("robin")
    translation.activate('de')
    print(".. raw:: html")
    print("")
    print("  <ul>")
    for at in aids.AidType.objects.exclude(confirmation_type=''):
        if at.get_confirmation_template():
            M = at.confirmation_type.model
            qs = M.objects.filter(granting__aid_type=at)
            obj = qs[0]
            txt = obj.confirmation_text(ses)
            txt = ' '.join(txt.split())
            print("  <li><b>%s</b> : (Hiermit bestätigen wir dass (Name)) %s</li>" % (unicode(at), txt))
    print("  </ul>")
    print("")


