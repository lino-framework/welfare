.. _welfare.tested.aids:

============
Beihilfen
============

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_aids

..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
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



Hilfearten
==========

Hier eine Liste der Hilfearten, die Lino kennt:

>>> ses.show(aids.AidTypes, column_names="name_de confirmed_by_primary_coach body_template")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================================================= =========================== ============================
 Bezeichnung (de)                                  Primärbegleiter bestätigt   Body template
------------------------------------------------- --------------------------- ----------------------------
 Ausländerbeihilfe                                 Ja                          foreigner_income.body.html
 DMH-Übernahmeschein                               Ja                          certificate.body.html
 Eingliederungseinkommen                           Ja                          integ_income.body.html
 Erstattung                                        Ja                          certificate.body.html
 Feste Beihilfe                                    Ja                          fixed_income.body.html
 Lebensmittelbank                                  Nein                        food_bank.body.html
 Möbellager                                        Ja                          furniture.body.html
 Heizkosten                                        Ja                          heating_refund.body.html
 Übernahme von Arzt- und/oder Medikamentenkosten   Ja                          certificate.body.html
 Übernahmeschein                                   Ja                          certificate.body.html
 **Total (10 Zeilen)**                             **9**
================================================= =========================== ============================
<BLANKLINE>



Beschlüsse und Bestätigungen
============================

Lino unterscheidet zwischen Hilfe\ *beschlüssen*
(:class:`Granting <welfare.aids.Granting>`) und Hilfe\ *bestätigungen*
(:class:`Confirmation <welfare.aids.Confirmation>`).

Hilfe\ *bestätigungen* sind "Präzisierungen" eines Hilfe\
*beschlusses*.  Beschlüsse sind *prinzipiell*, *langfristig* und
*allgemein*, Bestätigungen sind *detailliert*, *befristet* und
*konkret*.  Der Beschluss ist sozusagen die Erlaubnis oder Grundlage,
Bestätigungen für eine bestimmte Hilfeart auszuhändigen.

Zum Beispiel ist es ein *Beschluss*, wenn jemand
*Eingliederungseinkommen* erhält.  Aber der monatliche Betrag steht
nicht im *Beschluss*, sondern nur in der *Bestätigung*, weil der sich
im Laufe der Zeit ändern kann.

Oder wenn jemand Anrecht auf *Übernahme von Arzt- und
Medikamentenkosten* hat, ist das ein *Beschluss*. Um daraus eine
*Bescheinigung* zu machen, muss man auch *Apotheke* und *Arzt*
angeben.

Bemerkungen
===========

- Es gibt Hilfearten (z.B. “Erstattung”), für die nie eine
  Bescheinigung gedruckt wird. Deren Feld (:attr:`Bescheinigungsart
  <welfare.aids.AidType.confirmation_type>` ist leer.

- Einen “Bestätiger” (:attr:`signer
  <welfare.aids.Confirmable.signer>`) kann es pro Bescheinigung als
  auch pro Beschluss geben.  Bestätiger des Beschlusses ist par défaut
  der Primärbegleiter, Bestätiger einer Bescheinigung ist der des
  Beschlusses.

- Pro Bescheinigung auch die Apotheke sehen und ändern können (d.h.:
  Neue Felder AidType.pharmacy_type und RefundConfirmation.pharmacy.
  (ist allerdings noch nicht vorbelegt aus Klientenkontakt)




Hilfebeschlüsse
===============

Alicia hat 2 Hilfebestätigungen zu unterschreiben. Dies kriegt sie als
Willkommensmeldung unter die Nase gerieben:

>>> ses = rt.login('alicia')
>>> translation.activate('de')
>>> for msg in settings.SITE.get_welcome_messages(ses):
...     print(E.tostring(msg))
<span>Du bist besch&#228;ftigt mit <b>Collard Charlotte (118)</b>.</span>
<span>Du hast 2 Eintr&#228;ge in <i>Zu unterschreibende Hilfebeschl&#252;sse</i>.</span>

>>> ses.show(aids.MyPendingGrantings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================ ================= ============== ===== ======= ================================
 Klient                       Hilfeart          Laufzeit von   bis   Autor   Arbeitsablauf
---------------------------- ----------------- -------------- ----- ------- --------------------------------
 EMONTS-GAST Erna (152)       Möbellager        29.05.14                     **Unbestätigt** → [Bestätigen]
 DOBBELSTEIN Dorothée (124)   Übernahmeschein   26.05.14                     **Unbestätigt** → [Bestätigen]
============================ ================= ============== ===== ======= ================================
<BLANKLINE>


Hilfebestätigungen
==================


>>> translation.activate('de')

Hier eine Liste aller bisher vorgesehenen Bescheinigungstexte:

>>> for at in aids.AidType.objects.exclude(confirmation_type=''):
...    M = at.confirmation_type.model
...    qs = M.objects.filter(granting__aid_type=at)
...    obj = qs[0]
...    txt = obj.confirmation_text()
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

Beispiele
=========


Für die Hilfearten aus obiger Liste, für die eine Vorlage definiert
ist (also für wir nicht bloß den generischen Bestätigungstext haben)
hier die gleichen Texte als HTML:

.. django2rst::

    from __future__ import unicode_literals
    from django.utils import translation
    from atelier.rstgen import header
    ses = rt.login("rolf")
    translation.activate('de')

    for at in aids.AidType.objects.exclude(confirmation_type=''):
        M = at.confirmation_type.model
        qs = M.objects.filter(granting__aid_type=at)
        obj = qs[0]
        ex = obj.printed_by
        if ex:
            print(header(5, unicode(at)))
            print(".. complextable::")
            print("")
            print("  ::")
            print("")
            for ln in ex.body_template_content(ses).splitlines():
                print("    " + ln)
            print("")
            print("  <NEXTCELL>")
            print("")
            print("  .. raw:: html")
            print("")
            for ln in ex.preview(ses).splitlines():
                print("    " + ln)
            print("")
    print("")



