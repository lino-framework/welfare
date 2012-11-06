Die kommende Version
====================


Behobene Fehler
---------------

- Wenn man in TIM PAR->IdUsr auf leer setzte oder auf einen 
  Benutzer, den es in Lino nicht gibt, dann schaut watch_tim 
  nach, ob es eine primäre Begleitung für diesen Klienten gibt 
  (mit egal welchem Benutzer) und *löscht* die dann. Logisch. 
  Aber da war noch ein Bug drin: das Löschen dieser Begleitung 
  wurde nicht geloggt, stattdessen kam ein Traceback 
  "IntegrityError (1048, "Column 'object_id' cannot be null")"
