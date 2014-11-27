.. _welfare.tested.aids:

===========
Social aids
===========

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

>>> ses.show(aids.AidTypes, column_names="name confirmed_by_primary_coach body_template")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================================================= =========================== ===============================
 Bezeichnung                                       Primärbegleiter bestätigt   Textkörper-Vorlage
------------------------------------------------- --------------------------- -------------------------------
 Ausländerbeihilfe                                 Ja                          foreigner_income.body.html
 Dringende Medizinische Hilfe                      Ja                          urgent_medical_care.body.html
 Eingliederungseinkommen                           Ja                          integ_income.body.html
 Erstattung                                        Ja                          certificate.body.html
 Feste Beihilfe                                    Ja                          fixed_income.body.html
 Heizkosten                                        Ja                          heating_refund.body.html
 Kleiderkammer                                     Ja                          clothing_bank.body.html
 Lebensmittelbank                                  Nein                        food_bank.body.html
 Möbellager                                        Ja                          furniture.body.html
 Übernahme von Arzt- und/oder Medikamentenkosten   Ja                          certificate.body.html
 Übernahmeschein                                   Ja                          certificate.body.html
 **Total (11 Zeilen)**                             **10**
================================================= =========================== ===============================
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
<span>Du hast 4 Eintr&#228;ge in <i>Zu unterschreibende Hilfebeschl&#252;sse</i>.</span>


>>> ses.show(aids.MyPendingGrantings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
======================== ========================= ============== ========== ======= ================================
 Klient                   Hilfeart                  Laufzeit von   bis        Autor   Arbeitsablauf
------------------------ ------------------------- -------------- ---------- ------- --------------------------------
 EMONTS-GAST Erna (152)   Heizkosten                30.05.14       31.05.14           **Unbestätigt** → [Bestätigen]
 DUBOIS Robin (179)       Ausländerbeihilfe         05.01.14                          **Unbestätigt** → [Bestätigen]
 DUBOIS Robin (179)       Eingliederungseinkommen   26.02.13                          **Unbestätigt** → [Bestätigen]
 DA VINCI David (165)     Eingliederungseinkommen   27.01.13                          **Unbestätigt** → [Bestätigen]
======================== ========================= ============== ========== ======= ================================
<BLANKLINE>


Hilfebestätigungen
==================

In der Demo-Datenbank gibt es 2 generierte Bescheinigungen pro Hilfeart :

>>> translation.activate('de')
>>> for at in aids.AidType.objects.exclude(confirmation_type='').order_by('id'):
...    M = at.confirmation_type.model
...    qs = M.objects.filter(granting__aid_type=at)
...    obj = qs[0]
...    txt = obj.confirmation_text()
...    txt = ' '.join(txt.split())
...    print("%s : %d" % (unicode(at), qs.count()))
Eingliederungseinkommen : 18
Ausländerbeihilfe : 33
Feste Beihilfe : 3
Erstattung : 3
Übernahmeschein : 3
Übernahme von Arzt- und/oder Medikamentenkosten : 6
Dringende Medizinische Hilfe : 6
Möbellager : 3
Heizkosten : 3
Lebensmittelbank : 3
Kleiderkammer : 4


Grantings by ISIP contract
==========================

The :meth:`welfare.isip.ContractBase.get_aid_type`
method (called from the document template when printing a 
:mod:`welfare.isip.Contract` in Eupen)
works only when 
:meth:`welfare.isip.ContractBase.get_grantings`
returns exactly one granting.
Which is the normal situation.

The demo fixtures generate some exceptions to this general rule.  Here
we see that most contracts have indeed exactly 1 granting:

>>> isip.Contract.objects.all().count()
30

>>> dist = {}
>>> for con in isip.Contract.objects.all():
...     qs = con.get_grantings()
...     k = qs.count()
...     l = dist.setdefault(k, [])
...     l.append(con.id)
>>> print(dist)
{1: [1, 4, 5, 8, 10, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29], 2: [9, 13, 15, 17, 20, 22, 25, 28, 30], 3: [2, 6, 7], 4: [3]}

