.. _welfare.changes: 

========================
Changes in Lino-Welfare
========================

See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino/source/list>`_
(hosted on `Googlecode <http://code.google.com/p/lino>`__).
 


Version 1.1.2 (released 2013-04-22)
===================================

- fixed problems reported by users

  - pdf-Dokument aus Startseite (UsersWithClients) erstellen:
    kommt leider nur ein leeres Dok-pdf bei raus

  - excel-Dokument  aus Startseite erstellen:
    kommt zwar ein Dok bei raus, aber leider nur mit Kode-Zahlen als 
    Titel / nicht die eigentlichen Spalten-Titel, wie in der Übersicht
    Startseite. etwas unpraktisch, da die Titel der Spalten 
    neu eingetippt werden müssen.
    
  - Could not print Tx25 documents
    ("'Site' object has no attribute 'getlanguage_info'")
    
  - (and maybe some more...)

- The `Merge` action on :ref:`welfare.pcsw.Client` and 
  :ref:`welfare.contacts.Company` had disappeared. 
  Fixed.
  
  Also this action is no longer disabled for imported partners.
  
- The new method :meth:`lino.core.model.Model.subclasses_graph`
  generates a graphviz directive which shows this model and the 
  submodels.
  the one and only usage example is visible in the 
  `Lino-Welfare user manual
  <http://welfare-user.lino-framework.org/fr/clients.html#partenaire>`_
  See :blogref:`20130401`.

Version 1.1.1 (released 2013-03-29)
===================================

- Changes before 1.1.1 are not listed here.
  See the developers blog and/or the Mercurial log.

  

