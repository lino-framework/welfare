=========
Über Lino
=========

Technische Informationen
========================

* Lino utilise les technologies Python, Django et ExtJS pour délivrer
  des Rich Internet Applications (RIA) au look « desktop ». 
* Une application Lino fonctionne indépendamment du système
  d’exploitation et de l’endroit géographique
* Lino tourne sur n’importe quel serveur qui offre Apache/mod_wsgi
  (ou un autre serveur web compatible WSGI) et une des bases de données
  MySQL, PostgreSQL, SQLite, Oracle. En pratique nous recommendons Debian
  ou Ubuntu.
* Plusieures instances par serveur possible (par exemple pour
  différentes applications/services et/ou environnement de test)
* Multilingue à trois niveaux : (1) interface utilisateur (2)
  désignations des codes et (3) destinataire d’un document
* Génération automatique de documents de type PDF, MS-Word, OpenOffice
  et autres se basant sur des templates (modèles, gabarits)
* WebDAV automatique intégré afin de pouvoir éditer des documents
  générés et stockés sur le serveur sans que l’utilisateur doive
  intervenir.
* Export des données vers des tableurs (ex Excel), en Hypertext Markup
  Language (HTML) et Portable Document Format (PDF)
* Filtres et fonctions de recherche intuitifs et avancés
* Authentication annuaire LDAP
* Customisation facile
* Système sophistiqué pour définir et modifier les workflows



Geschichte
==========

1995 wurde das ÖSHZ Eupen darüber informiert, dass die Firma, von der
es die Buchhaltungsoftware hatte, und die ebenfalls den Unterhalt
dieser Software garantierte, dass diese Firma ihre Dienstleistungen
einstellen würde.

Um schnellstmöglich eine Lösung zu finden und vor allem in Zukunft
eine solche Situation zu vermeiden, entschied sich das ÖSHZ Eupen, mit
Hilfe einer Eupener Firma maßgeschneiderte Software entwickeln zu
lassen und dies auf Basis eines Frameworks namens `TIM
<http://tim.saffre-rumma.net/115.html>`_.

Bereits im Januar 1996 war "unser TIM" einsatzbereit und schon einige
Monate später fragte sich das anfänglich skeptische Personal, wie es
vorher möglich gewesen war, ohne diese neue Software zu arbeiten, die
all ihre Anforderungen auf "geniale" Weise erfüllte. 

Während den letzten 17 Jahren wurden die Funktionalitäten der Software
kontinuierlich ausgebaut, um den täglichen Anforderungen zu
entsprechen.  Als Beispiele seien unzählige legale Anpassungen, der
Wechsel in ein neues Jahrtausend und zum Euro, finanzielle Änderungen
wie BIC/IBAN und SEPA oder der elektronische Personalausweis genannt.

Trotz enormer Zunahme an Aufgaben in der Finanzabteilung, gelang es
auf Grund der Flexibilität des Frameworks "TIM" und seiner unzähligen
Parametrierungsmöglichkeiten während 15 Jahren ohne zusätzliches
Personal auszukommen.

Seit 2001 ist "TIM" quelloffene Software (Open Source) und somit
kostenlos für jedermann erhältlich. Das Framework wird bis heute
u.a. im ÖSHZ Eupen, ÖSHZ Raeren, ÖSHZ Bütgenbach, SPZ Eupen und in
etlichen KMU diverser Größen eingesetzt."

`Luc Saffre <https://www.linkedin.com/profile/view?id=2682025>`_, der
Entwickler von TIM, suchte über Jahre nach einer zufriedenstellenden
Lösung für einen technischen Nachfolger des Frameworks. Über PHP, Java
usw. kam er dann zu Python/Django und die Erfolgsgeschichte von "Lino"
begann.

Im Jahr 2009 benötigte der Dienst für sozial-berufliche Eingliederung
(DSBE) des ÖSHZ Eupen ein Verwaltungsprogramm.  Angesichts der
exzellenten Erfahrungen mit TIM schien Lino ein Kandidat mit guten
Erfolgsaussichten.  Bereits Anfang 2010 war die neue Anwendung in
Betrieb und dies mit großer Zufriedenheit des DSBE.  Seit mehr als
einem Jahr gibt es auch speziell auf die Schuldnerberatung abgestimmte
Funktionalitäten. Ferner wird zur Zeit ein so genanntes Modul
Sozialsekretariat (Empfangsmodul) entwickelt, das bereits in TIM
besteht und in den ÖSHZ Eupen und Raeren eingesetzt wird. Die gesamten
Module sind Teil einer Lino-Applikation namens 
`Lino Welfare <http://welfare.lino-framework.org>`_.

Neben Lino Welfare gibt es (mindestens) noch zwei weitere
erwähnenswerte Anwendungen, die aus dem Framework entstanden sind:
die Buchhaltung `Lino Così <http://cosi.lino-framework.org>`_ und die
Kursverwaltung `Lino Faggio <http://faggio.lino-framework.org>`_.

Von allen steht eine Demo-Version zur Verfügung, die zeigt, was Lino
alles kann und die ein gutes Bild vermittelt, wie das Framework die
Vorteile einer webbasierten und einer Desktop-Anwendung vereint:
http://www.lino-framework.org/demos.html 

