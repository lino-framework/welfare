Die kommende Version
====================

Neue Features
-------------

- Kliententabelle: Neben dem Parameter "Begleitet durch" gibt es jetzt ein 
  weiteres Feld "und durch".
  
- eId-Karten einlesen. 

- Lino is now able to do `Session-based authentication
  <http://lino-framework.org/blog/2012/1103.html>`_.


Behobene Fehler
---------------

- Wenn man in TIM PAR->IdUsr auf leer setzte oder auf einen 
  Benutzer, den es in Lino nicht gibt, dann schaut watch_tim 
  nach, ob es eine primäre Begleitung für diesen Klienten gibt 
  (mit egal welchem Benutzer) und *löscht* die dann. Logisch. 
  Aber da war noch ein Bug drin: das Löschen dieser Begleitung 
  wurde nicht geloggt, stattdessen kam ein Traceback 
  "IntegrityError (1048, "Column 'object_id' cannot be null")"

- "AJAX-Gehoppel" (`1207 <http://lino-framework.org/blog/2012/1107.html>`_)

- Button "Tabellenkonfiguration speichern" war eine Mausefalle und wurde deshalb bis auf weiteres deaktiviert. Siehe 
  `1206 <http://lino-framework.org/blog/2012/1106.html>`_
  und
  `1207 <http://lino-framework.org/blog/2012/1107.html>`_.
  
- In der Tabelle "Resultate" einer Tx25 erschien manchmal lediglich eine Fehlermeldung 
  "cannot concatenate 'str' and 'instance' objects"