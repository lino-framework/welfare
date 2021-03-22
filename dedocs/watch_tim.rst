.. _welfare.watch_tim:

=========
watch_tim
=========

Diese Seite ist die offizielle Dokumentation der Synchronisierung von
TIM nach Lino, einer Funktionalität, die ausschließlich im ÖSHZ Eupen
genutzt wird.


.. contents:: 
   :local:
   :depth: 2


Partner und watch_tim
=====================

Sowohl in TIM als auch in Lino gibt es eine Tabelle der **Partner**.
Die Partnernummer ist die Gleiche in TIM wie in Lino.
Im Hintergrund läuft ständig ein Programm namens `watch_tim`, 
das alle Änderungen in TIM automatisch nach Lino synchronisiert.

Partner mit einer Nummer zwischen 200000 und 299999 
sind **in Lino erstellt** worden und existieren also nicht in TIM.
Alle anderen Partner sind **importierte** Partner, und die haben 
die meisten Datenfelder in Lino schreibgeschützt.

Lino *unterteilt* Partner etwas anders als TIM.

TIM unterscheidet vier "Partnerarten":

- S Sozialhilfeempfänger
- A APH-Bewohner
- V Verschiedene
- I Inaktive Partner

Bei der Synchronisierung wird nach folgenden Regeln entschieden, wer
wo hin kommt:

- Wenn mindestens eines der Felder
  `PAR->NB2` (INSS) oder `PAR->NB1` (Gesdos-Nr) 
  unleer ist, oder wenn *Partnerattribut N (Neuzugang)* 
  gesetzt ist, dann wird es ein 
  `Klient <pcsw.Client>`.
  Wobei zu beachten ist, dass `PAR->NB2` (INSS) als leer gilt, wenn es
  nur eine  Null ("0")  enthält.
  Ausnahme: 
  Wenn `PAR->NoTva` unleer ist und `PAR->NB2` (INSS) leer,
  dann wird es *trotzdem kein* Klient 
  (sondern eine Organisation, s.h. nächster Punkt).
  
- **Ansonsten**, wenn `PAR->NoTva` unleer ist, wird es eine 
  `Organisation <contacts.Company>`.
- **Ansonsten**, wenn `PAR->Allo` (Anrede) einen der Werte "Eheleute", 
  "Herr und Frau" enthält, dann wird es ein 
  `Haushalt <households.Household>`
- Ansonsten wird es eine `Person <contacts.Person>`.

Zusatzregel:

- um Klient oder Person werden zu können, muss ein Partner außerdem
  auch einen *Vornamen* haben, d.h. `PAR->Firme` muss mindestens ein
  Leerzeichen enthalten.  Hat er das nicht, wird er zum einfachen
  Partner, und eventuelle Information in `PAR->NB1` oder `PAR->NB2`
  werden ignoriert.
  

Ob eine Organisation auch Kursanbieter
(:class:`welfare.courses.CourseProvider`) und/oder Stellenabieter
(:class:`welfare.jobs.JobProvider`) ist, wird lediglich in Lino (durch
Ankreuzen des antsprechenden Feldes im Detail-Fenster) entschieden.
TIM kennt diese Information nicht.

Partnerattribute
----------------

Hier eine Liste der möglichen Partnerattribute in TIM, und was Lino daraus macht.

====== ====================================== ========================================
Attrib Bezeichnung in TIM                     in Lino
====== ====================================== ========================================
H      Versteckt                              wird ignoriert
W      Warnung bei Auswahl                    `veraltet` im Reiter `Sonstiges`
R      Schreibgeschützt                       wird ignoriert
2      als Nebenpartner ignorieren            wird ignoriert
A      Altfall (automatisch)                  wird ignoriert
E      Eingeschlafener Debitor (automatisch)  wird ignoriert
N      Neuzugang                              Klient im Bearbeitungszustand "Neuantrag"
====== ====================================== ========================================

**Partnerattribut W** bewirkt in Lino das Gleiche 
wie **Partnerart "Inaktive"**, nämlich dass dieser Partner 
das Feld `veraltet` angekreuzt kriegt.

Das **Partnerattribut A** (Altfall) aus TIM ist eine rein buchhalterische 
Information (Partner hat seit dd.mm.yyyy keine buchhalterische Bewegung gehabt), 
die momentan in Lino nicht importiert wird. 
Falls sie mal in Lino sichtbar werden soll, 
sollte sie als ein eigenes schreibgeschütztes Ankreuzfeld da stehen.

Hier einige mögliche Überraschungseffekte

- Ein existierender Klient kann in Lino verschwunden scheinen, 
  weil er versehentlich als veraltet  markiert wurde
  (siehe `Veraltete Partner`_).
  (siehe `Partnerattribute`_).
  Also nachprüfen, ob er in TIM das **Partnerattribut W** gesetzt hat. 
  Oder gar unter Partnerart "Inaktive" steht.

- "Ich sehe in "meiner" Liste in Lino einen bestimmten aus TIM importierten 
  Klienten, den ich schon seit Langem nicht mehr begleite."
  --> Um einen aus TIM importierten Klienten 
  nicht mehr "in meiner Liste" zu sehen, muss in TIM entweder 
  das Feld `PAR->IdUser` geändert, 
  die Partnerart auf Inaktiv gesetzt
  oder das Partnerattribut W eingeschaltet werden.


Anrede
------

`PAR->Allo` geht nach :attr:`Person.title` oder :attr:`Company.prefix`.
Außer wenn `PAR->Allo` es einen der Werte "Eheleute", 
"Herr und Frau" enthält, dann wird es ein Haushalt.

`PAR->Name2` wird ins Feld "Adresszeile vor Straße" importiert.


Die INSS
--------

- Es kann Klienten ohne INSS geben. 
  Die sind dann allerdings "inoffiziell" bzw. "nicht integriert" bzw. "ohne Akte beim Ministerium".
  In TIM haben diese Klienten entweder eine leere INSS oder eine 0 dort stehen.
  Die 0 wird als "leer" übertragen, denn 
  in Lino kann es nicht zwei Klienten mit der gleichen INSS geben.
  
- Lino lässt auch ungültige INSS zu.
  
- Ein "Numéro bis" ist eine provisorische INSS, 
  die z.B. auch 680000 formatiert ist.
  So eine Bis-Nummer kann also dann auch irgendwann mal ändern.


Bearbeitungszustand
-------------------

Der Bearbeitungszustand eines Klienten kann sein:

- **Neuantrag** : 
  Die Person hat Antrag auf Begleitung gestellt. 
  Antrag wird überprüft und der Klient muss einem Sachbearbeiter 
  oder Sozi zugewiesen werden.
  
  Im Detail-Reiter 
  :screen:`Neuanträge <pcsw.Client.detail.newcomers>`
  kann man einem Neuzugang 
  einen **Begleiter zuweisen**, wodurch der Klient ins Stadium "Begleitet" wechelt.
  
- **Abgelehnt** : 
  Die Prüfung des Antrags hat ergeben, dass diese Person kein Anrecht 
  auf Begleitung durch unser ÖSHZ hat.
  
- **Begleitet** :
  Es gibt im ÖSHZ mindestens eine Person, die "sich um die Person kümmert".
  Damit ein Klient im Status "Begleitet" sein kann, muss mindestens 
  eine aktive Begleitung existieren.

- **Ehemalig** :
  War mal begleitet, aber jetzt nicht mehr. 
  Es existieren Begleitungen, aber keine davon ist *aktiv*.
  Falls es ein importierter Partner ist, 
  hatte er in TIM entweder das Attribut `W (Warnung bei Auswahl)`
  oder die Partnerart `I (Inaktive)`.

  
  
  
.. graphviz:: 
   
   digraph foo {
      newcomer -> refused [label="Neuantrag ablehnen"];
      newcomer -> coached [label="Begleiter zuweisen"];
      refused -> newcomer [label="Neuantrag wiederholen"];
      coached -> newcomer [label="Begleitung abbrechen"];
      coached -> former [label="Begleitung beenden"];
      
      newcomer [label="Neuantrag"];
      refused [label="Abgelehnt"];
      former [label="Ehemalig"];
      coached [label="Begleitet"];
   }


Bemerkung:
Wie alle Partner haben auch Klienten (im Reiter "Sonstiges") 
ein Ankreuzfeld "veraltet",
das unabhängig vom Bearbeitungszustand_ existiert. 
Siehe `Veraltete Partner`_.



Veraltete Partner
-----------------

Bei importierten Partnern ist 
das Ankreuzfeld 
`veraltet <contacts.Partner.is_obsolete>`
schreibgeschützt.
Es ist eingeschaltet, wenn diese Person in TIM 
entweder in **Partnerart "Inaktive"** steht oder 
das **Partnerattribut W** eingeschaltet hat. 



Sonstiges
---------

Im Reiter :guilabel:`Sonstiges` gibt es drei Ankreuzfelder 

- Sozialhilfeempfänger (`is_cpas`) : Angekreuzt , wenn in TIM Partnerart S war.
- Altenheim (`is_senior`) : Angekreuzt , wenn in TIM Partnerart A war.
- veraltet (`is_obsolete`) : Angekreuzt , wenn in TIM Partneraattribut W gesetzt war.


.. Dubletten
  Der Klient wurde versehentlich als Dublette eines existierenden 
  Klienten angelegt (und darf jedoch nicht mehr gelöscht werden, 
  weil Dokumente mit der Partnernummer existieren).
  In Lino setzt man solche Klienten einfach in den 
  Bearbeitungszustand "Ungültig".


Begleitungen
============

Eine **Begleitung** ist, wenn sich ein bestimmter Mitarbeiter des ÖSHZ 
um einen bestimmten Klienten während einer bestimmten Periode 
"kümmert".
Ein Klient kann mehrere Begleitungen auf einmal haben, 
z.B. eine im ASD und eine andere im DSBE.

Begleitungen werden entweder manuell erzeugt 
durch `Einfügen` in der Tabelle "Begleitungen",
oder indirekt durch das **Zuweisen** eines verfügbaren Begleiters.

Die Felder **von** und **bis** einer Begleitung definieren die **Begleitungsperiode**.
Das Feld `von` einer Begleitung kann nicht leer sein.
Ein leeres Feld `bis` einer Begleitung bedeutet, dass das Ende nicht bekannt ist.
Eine Begleitung ist (an einem gegebenen Datum `heute`) aktiv,
wenn `von` **<=** `heute` und `bis` entweder leer oder **>=** `heute` ist.


Primäre Begleitung
------------------

Lino kann pro Klient mehrere Begleitungen haben,
aber in TIM haben wir nur den "hauptverantwortlichen Sozialarbeiter" (`PAR->IdUsr`). 
Deshalb gibt es das Konzept der **primären** Begleitung.
In Lino kann pro Klient eine Begleitung primär sein.
Diese entspricht dem Feld `PAR->IdUsr` aus TIM.

Für die primäre Begleitung eines *importierten* Klienten gilt:

- Die Felder `primär`, `bis` und `Benutzer` sind schreibgeschützt und wie folgt belegt:

  - `primär` = angekreuzt
  - `Benutzer` : der in TIM angegebene Benutzer
  - `bis` : entweder leer (wenn es eine aktive Begleitung ist) 
    oder 01.01.1990 (wenn es ein Neuzugang oder ehemaliger Klient ist)
  
  Diese Angaben können also nur über TIM verändert werden.

- Die Felder `von` und `Dienst` dagegen können manuell geändert werden, 
  und `watch_tim` geht dann nicht mehr daran.
  Beim ersten Erstellen gibt `watch_tim` ihnen folgende Werte:

  - `Dienst` = Begleitdienst des Begleiters zu diesem Zeitpunkt
  - `von` = Erstelldatum des Partners in TIM
  
Also man kann auf importierten Klienten in Lino zusätzliche Begleitungen 
erstellen, aber diese können nicht primär sein.
An diese sekundären Begleitungen geht `watch_tim` nicht ran.

.. _welfare.clients.CoachingType:

Begleitungsdienst
-----------------

Jede Begleitung findet zwingend im Rahmen eines bestimmten 
**Dienstes** statt.
    

Regeln
------
  
- Ein Neuantrag kann keine Begleitungen haben. 
  (Ein Klient mit Begleitungen, selbst abgeschlossene, 
  kann nicht wieder zum Neuantrag werden. 
  Höchstens zu einem Ehemaligen.)
  
- Wenn ein Klient ins Stadium Ehemalig wechselt, werden automatisch 
  alle laufenden Begleitungen beendet.
  Ein Ehemaliger kann keine *laufenden* Begleitungen haben.
  
- Nur Benutzer mit einem unleeren Feld 
  `Begleitungsart (Dienst)` in den Benutzereinstellungen
  dürfen manuell Begleitungen erstellen.
  
- Importierte Klienten haben eine importierte primäre 
  Begleitung, die nicht geändert werden kann.
  

Krankenkassen und Apotheken (Klientenkontakte)
==============================================

Die Felder PXS->IdMut (Krankenkasse) und PXS->Apotheke (Apotheke)
werden nach Lino synchronisiert als `Klientenkontakte
<coachings.ClientContact>`.

*Importierte* Klienten sollten in ihren 
`Klientenkontakten <coachings.ClientContact>`
deshalb maximal *eine* Krankenkasse und *eine* Apotheke haben.
Sonst findet `watch_tim`, dass er nicht dafür 
zuständig ist und synchronisiert nichts 
(schreibt lediglich eine Warnung in die `system.log`)

Alle anderen Klientenkontaktarten sind egal, 
davon dürfen auch importierte Klienten so viele haben wie sie wollen.

Apotheken sind in TIM normale Partner, aber 
Krankenkassen sind Adressen aus `ADR` mit `ADR->Type == 'MUT'`.
Sie erscheinen in Lino als Organisation, 
werden aber nicht mehr automatisch synchronisiert.
Also falls des eine in TIM erstellt wird, muss die entsprechende 
Organisation in Lino manuell erstellt werden.
Dabei ist zu beachten, dass das `id` einer Krankenasse 
beim ersten Import (`initdb_tim`) 
wie folgt ermittelt wurde:

  id = val(ADR->IdMut) + 199000


Beim Synchronisieren sind folgende Fehlermeldungen denkbar 
(die falls sie auftreten per E-Mail an die Administratoren geschickt werden)::

    ERROR Client #20475 (u"MUSTERMANN Max (20475)") : Pharmacy or Health Insurance 199630 doesn't exist
    ERROR Client #20475 (u"MUSTERMANN Max (20475)") : Pharmacy or Health Insurance 0000086256 doesn't exist

Die erste Meldung bedeutet, dass die Krankenkasse fehlt (Nr. 199xxx sind Krankenkassen), also 
dass man in TIM in der ADR.DBF die Nr 630 raussucht und diese manuell in Lino als Organisation 
199630 anlegt.

Die zweite Meldung ist eine fehlende Apotheke. Da reicht es, in TIM mal auf diese 
Apotheke 86256 zu gehen und irgendwas zu ändern, 
um manuell eine Synchronisierung auszulösen.
Kann auch sein, dass es in TIM keinen Partner 86256 gibt 
(TIM lässt es fälschlicherweise zu, Apotheken zu löschen die anderswo referenziert werden): 
dann muss der Klient 20475 sein Feld PXS->Apotheke auf 
leer gesetzt bekommen (oder auf eine andere existierende 
Apotheke).
  

Technisches
===========

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



Cannot create Client 0000023756 from PXS
----------------------------------------

Die Meldung kommt, wenn in TIM in der PXS eines Partners etwas 
verändert wurde, und dieser Partner in Lino nicht existiert 
(was anormal ist, aber z.B. durch frühere Bugs oder Pannen kommen kann).
Zu tun: manuell für diesen Partner in der PAR etwas verändern, um 
eine Synchronisierung zu triggern.



