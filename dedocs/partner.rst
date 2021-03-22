.. _welfare.de.partner:

=======
Partner
=======



.. contents::
   :local:


.. currentmodule:: lino_welfare.modlib.contacts

.. doctest init
    >>> from lino import startup
    >>> startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from lino.api.doctest import *
    



Ein **Partner** ist eine `natürliche
<http://de.wikipedia.org/wiki/Nat%C3%BCrliche_Person>`_ oder
`juristische <http://de.wikipedia.org/wiki/Juristische_Person>`_
Person (*personne physique ou morale*), für die wir in Lino mindestens
den Namen speichern. Ein Partner kann also alles Mögliche sein: ein
Klient, ein Lieferant, eine öffentliche Dienststelle, eine
Kontaktperson in einer Firma, ...

Lino unterscheidet folgende **Arten von Partnern**:

.. lino2rst::
   
   with dd.translation.override('de'):
       contacts.Partner.print_subclasses_graph()



Veraltete Partner
=================


Das Attribut "veraltet" (:attr:`welfare.contacts.Partner.is_obsolete`)
bedeutet :

- die Daten dieses Partners werden nicht mehr gepflegt, 
- alle Angaben verstehen sich als "so war es, bevor dieser Partner 
  aufhörte, uns zu interessieren".

Veraltete Partner werden normalerweise in Listen ignoriert, als wären
sie gelöscht.  Um sie trotzdem zu sehen, muss das Ankreuzfeld `Auch
veraltete Klienten` (bzw. `Auch veraltete Partner`) im Parameter-Panel
der Liste angekreuzt werden.


