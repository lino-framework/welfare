Die kommende Version
====================

Bugfixes

- "ich stelle gerade fest, dass ich bei den Benutzern nicht mehr das 
  Benutzerprofil auswählen kann. Die Dropdown-Box geht nicht."
  (:doc:`/blog/2012/1127`)
  
- HTML-Ansicht funktionierte nicht. 
  Meldete stattdesen "'User' object has no attribute 'level'"  
  (:doc:`/blog/2012/1127`)
  
- Dientleiter DSBE konnte Verträge anderer Benutzer nicht löschen.
  (:doc:`/blog/2012/1127`)


Kleinkram

- Der Anwendungsentwickler (d.h. ich) kann jetzt auch pro Modell sagen, 
  welche Felder in der Tabellenansicht versteckt sein sollen. 
  Für die Liste der VSEs habe ich das mal gemacht. Dort kriegt man 
  jetzt mit einem einfachen Klick eine akzeptable Liste als pdf. 
  Dafür muss man "seltener benutzte" Kolonnen erst einschalten, um sie zu sehen.
  (:doc:`/blog/2012/1127`)

- New :class:`ExamPolicies <lino_welfare.modlib.isip.models.ExamPolicies>`
  now has a :attr:`detail_layout <lino.core.actors.Actor.detail_layout>`.
  (:doc:`/blog/2012/1126`)

- :menuselection:`Explorer --> ÖSHZ --> ClientStates`