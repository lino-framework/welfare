Konvertierung TIM nach Lino
===========================

Die NISS
--------

- Es kann Klienten ohne NISS geben. 
  Die sind dann allerdings "inoffiziell" bzw. "nicht integriert" bzw. "ohne Akte beim Ministerium".
  In TIM haben diese Klienten entweder eine leere NISS oder eine 0 dort stehen.
  *Lino trägt im Feld `NISS` die Partnernummer ein, wenn es nicht ausgefüllt ist.*
  
- Ein "Numéro bis" ist eine provisorische NISS, 
  die z.B. auch 680000 formatiert ist.
  So eine Bis-Nummer kann also dann auch irgendwann mal ändern.
  

watch_tim
---------

In der :xfile:`settings.py` gibt es folgende Optionen, 
die für die Synchronisierung von Belang sind::


    def is_imported_partner(self,obj):
        if obj.id is None:
            return False
        #if obj.id == 3999:
        #    return False
        return obj.id < 200000 or obj.id > 299999
        
        

    def TIM2LINO_LOCAL(alias,obj):
        """Hook for local special treatment on instances 
        that have been imported from TIM.
        """
        return obj
        
    def TIM2LINO_USERNAME(userid):
        if userid == "WRITE": return None
        return userid.lower()

Die Krankenkassen (Adressen aus ADR mit ADR->Type == 'MUT') 
erscheinen in Lino als :class:`Company`, 
wobei deren `id` beim ersten Import (initdb_tim) 
wie folgt ermittelt wurde:

  id = val(ADR->IdMut) + 199000
  
Die Partner aus TIM kommen nach 
:class:`contacts.Company`, 
nach :class:`contacts.Person`, 
nach :class:`households.Household`
oder
nach :class:`pcsw.Client` je nach folgenden Regeln:

- Wenn PAR->NB2 (NISS), Gesdos-Nr oder PAR->Memo unleer ist, wird es ein Klient.
- Ansonsten, wenn `PAR->Allo` einen der Werte "Eheleute", "Herr und Frau" enthält, dann wird es ein Haushalt.
- Ansonsten, wenn PAR->NoTva leer ist, wird es eine Person,
- Ansonsten wird es eine Firma.

Alle Partner stehen auch in ´contacts.Parter´.
Das jeweilige id entspricht der Partnernummer (PAR->IdPar) 
aus TIM.


Personen und Firmen mit einem id über 200.000 
(und unter 800.000) sind *in Lino* erstellt worden.

`PAR->Allo` geht nach :attr:`Person.title` oder :attr:`Company.prefix`.
Außer wenn `PAR->Allo` es einen der Werte "Eheleute", 
"Herr und Frau" enthält, dann wird es ein Haushalt.



Die Regeln beim Übernehmen der diversen Flags aus TIM sind:

- `newcomer` : `True` wenn Attribut N in TIM gesetzt ist
- `is_deprecated` (Altdaten) : `True` wenn Attribut W in TIM gesetzt ist.
- `is_active` : False wenn Partnerart I (ansonsten True)
- `is_cpas` : True wenn Partnerart S
- `is_senior` : True wenn Partnerart A

Hier eine Liste der möglichen Partnerattribute in TIM:

- H : Versteckt
- W : Warnung bei Auswahl
- R : Schreibgeschützt
- 2 : als Nebenpartner ignorieren
- A : Altfall (automatisch)
- E : Eingeschlafener Debitor (automatisch)
- N : Neuzugang



Der Unterschied zwischen W und A ist lediglich, das A automatisch verteilt wird. 
W ist eigentlich das Gleiche wie inaktiv.






Begleitungen
------------

In TIM haben wir nur PAR->IdUsr, den "hauptverantwortlichen Sozi". 
Lino kann pro Klient mehrere Begleitungen haben.
