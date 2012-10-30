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




Die Partner aus TIM kommen entweder nach 
:class:`contacts.Company`, 
nach :class:`contacts.Person`, 
nach :class:`households.Household`
oder
nach :class:`pcsw.Client`. Die Entscheidung wird nach folgenden Regeln getroffen:

- Wenn PAR->NB2 (NISS) oder Gesdos-Nr unleer, oder wenn Attribut N (Neuzugang) 
  gesetzt ist, wird es ein **Klient**.
- Ansonsten, wenn PAR->NoTva unleer ist, wird es eine **Organisation**.
- Ansonsten, wenn `PAR->Allo` (Anrede) einen der Werte "Eheleute", 
  "Herr und Frau" enthält, dann wird es ein **Haushalt**.
- Ansonsten wird es eine **Person**.

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

Lino kann pro Klient mehrere Begleitungen haben, aber in 
TIM haben wir nur PAR->IdUsr, den "hauptverantwortlichen Sozialarbeiter". 
Das haben wir wie folgt gelöst:

In Lino kann pro Klient immer nur eine Begleitung "primär" sein.
Diese entspricht dem Feld `PAR->IdUsr` aus TIM.
Für importierte Partner wird die primäre Begleitung aus TIM wie folgt synchronisiert:

- von : Erstelldatum des Kunden
- bis : leer
- Benutzer : der in TIM angegebene Benutzer

Auf importierten Klienten sind diese Felder (auf der *primären* Begleitung) 
schreibgeschützt. Auf importierten primären Begleitungen kann lediglich 
der Begleitungsdienst und der Zustand manuell geändert werden.

Das Ankreuzfeld "primär" kann auf importierten Klienten *nie* bearbeitet werden.

Also man kann auf importierten Partnern in Lino zusätzliche Begleitungen 
erstellen, aber diese können nicht primär sein.
An diese sekundären Begleitungen geht watch_tim dann nicht ran.


Krankenkassen
-------------

Die Krankenkassen (Adressen aus ADR mit ADR->Type == 'MUT') 
erscheinen in Lino als Organisation, 
wobei deren `id` beim ersten Import (initdb_tim) 
wie folgt ermittelt wurde:

  id = val(ADR->IdMut) + 199000
  
Krankenakssen werden nicht mehr automatisch synchronisiert.
Also falls des eine in TIM erstellt wird, muss die entsprechende 
Organisation in Lino manuell erstellt werden.

Klientenkontakte
----------------

Die Felder PXS->IdMut (Krankenasse) und PCS->Apotheke (Apotheke) 
werden nach Lino synchronisiert als *Klientenkontakte*.

Importierte Klienten sollten in ihren Klientenkontakten 
deshalb maximal *eine* Krankenkasse und *eine* Apotheke haben.

Ansonsten findet watch_tim, dass er nicht dafür 
zuständig ist und synchronisiert nichts (schreibt lediglich eine Warnung in die system.log)

Alle anderen Klientenkontaktarten sind egal, 
davon dürfen auch importierte Klienten so viele haben wie sie wollen.

Beim Synchronisieren sind folgende Fehlermeldungen denkbar 
(die falls sie auftreten per E-Mail an die Administratoren geschickt werden)::

    ERROR Client #20475 (u"MUSTERMANN Max (20475)") : Pharmacy or Health Insurance 199630 doesn't exist
    ERROR Client #20475 (u"MUSTERMANN Max (20475)") : Pharmacy or Health Insurance 0000086256 doesn't exist

Die erste Meldung bedeutet, dass die Krankenkasse fehlt (Nr. 199xxx sind Krankenkassen), also 
dass man in TIM in der ADR.DBF die Nr 630 raussucht und diese manuell in Lino als Organisation 199630 anlegt.

Die zweite Meldung ist eine fehlende Apotheke. Da reicht es, in TIM mal auf diese 
Apotheke zu gehen und irgendwas zu ändern, um manuell eine Synchronisierung auszulösen.
  
  
  
  