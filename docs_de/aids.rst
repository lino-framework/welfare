.. _welfare.de.aids:

============
Beihilfen
============


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





Wortschatz
==========

.. glossary::
  :sorted:


  DMH

    Dringende medizinische Hilfe (en: Urgent medical care / fr: Aide
    médicale urgente / nl: Dringende Medische Hulp)

    Die dringende medizinische Hilfe ist eine medizinische Hilfe in
    Form einer finanziellen Beteiligung durch das ÖSHZ an den
    medizinischen Kosten einer Person, die sich illegal in Belgien
    aufhält.  Die DMH ist keine finanzielle Hilfe, die direkt an die
    Person gezahlt wird, sondern möchte Illegalen lediglich den Zugang
    zur medizinischen Hilfe durch die Bezahlung des Arztes, des
    Krankenhauses, des Apothekers sicherstellen.  (Quelle:
    `www.mi-is.be
    <http://www.mi-is.be/en/public-social-welfare-centers/urgent-medicale-care>`_)



Hilfearten
==========

Hier eine Liste der Hilfearten, die Lino kennt:

.. lino2rst::

   rt.show(aids.AidTypes, column_names="name excerpt_title confirmed_by_primary_coach body_template confirmation_type")


Pro Hilfeart muss man sich entscheiden, welche **Bestätigungsart**
benutzt wird, um Bestätigunen ausstellen zu können.


Bestätigungsarten
=================

Lino kennt momentan drei Bestätigungsarten. Es können weitere
hinzugefügt werden, aber dazu wäre entsprechende Programmierung und
eine neue Version nötig.

Hier eine Liste der Bestätigungsarten, die Lino kennt:

.. lino2rst::

   rt.show(aids.ConfirmationTypes, column_names="text et_template")


.. currentmodule:: lino_welfare.modlib.aids.models

:class:`SimpleConfirmation`
:class:`IncomeConfirmation`
:class:`RefundConfirmation`

Kann keinen neuen Arzt erstellen, wenn Art des Arztes leer ist


Vorlagen
========

Beim Generieren einer Bescheinigung werden jeweils *zwei*
Dokumentvorlagen verwendet: die "Hauptvorlage" und die
"Textkörper-Vorlage".

Die **Hauptvorlage** ist ein LibreOffice-Dokument, das mit AppyPod
gerendert wird.  Dort wird das allgemeine Seitenformat definiert,
unter anderem auch das eventuelle Logo.  Normalerweise verwenden alle
Auszüge (nicht nur Hilfebestätigungen) die gleiche Hauptvorlage
"Default.odt".  Man kann diese Vorlage bearbeiten, indem man auf
irgendeinem Auszug, der sie verwendet, auf den Button "Vorlage
bearbeiten" klickt.  Geht natürlich nur wenn
:mod:`lino.modlib.davlink` aktiviert ist und man die entsprechenden
Rechte hat. Beachte auch, dass diese Standard-Hauptvorlage für viele
Dokumente verwendet wird.

"Normalerweise" genauer gesagt: Welche Hauptvorlage zu verwenden ist,
ergibt sich aus der *Auszugsart*, die für die *Bestätigungsart*
definiert ist (die sich ihrerseits aus der *Hilfeart* ergibt).

Die **Textkörper-Vorlage** `body_template` ist ein HTML-Dokument, das
mit *Jinja gerendert wird. Welche Textkörper-Vorlage verwendet wird,
ergibt sich aus der verwendeten *Hilfeart*. Hier die
Standardkonfiguration:

.. lino2rst::

   rt.show(aids.AidTypes, column_names="name body_template")

Eine Beschreibung aller standardmäßig verfügbaren Textkörper-Vorlagen
gibt es in der technischen Dokumentation (:mod:`welfare.aids`).


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
Willkommensmeldung präsentiert:

.. py2rst::

   from lino.api.doctest import *
   from django.utils import translation
   from etgen.html import E
   ses = rt.login('alicia')
   translation.activate('de')
   for msg in settings.SITE.get_welcome_messages(ses):
       print(tostring(msg))



Beispiele
=========

Für die Hilfearten aus obiger Liste, für die eine Textkörpervorlage
definiert ist (also für wir nicht bloß den generischen
Bestätigungstext haben) hier die gleichen Texte als HTML:

.. py2rst::

    from lino.api.doctest import *
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
            print(header(6, "Beispiel"))
            print("")
            print(".. raw:: html")
            print("")
            for ln in ses.get_data_value(ex, 'preview').splitlines():
                print("    " + ln)
            print("")
    
            print(header(6, "Vorlage"))
            print("::")
            print("")
            for ln in ses.get_data_value(ex, 'body_template_content').splitlines():
                print("    " + ln)
            print("")

    print("")



