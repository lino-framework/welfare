.. _welfare.tested.cbss:
.. _welfare.specs.cbss:

===============================
CBSS connection in Lino Welfare
===============================

.. to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_cbss

    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.api.doctest import *

The :mod:`lino_welfare.modlib.cbss` plugin adds functionality for
communicating with the *CBSS*.

The **CBSS** (Crossroads Bank for Social Security, French *Banque
Carrefour de la Sécurité Sociale*) is an information system for data
exchange between different Belgian government agencies.  `Official
website <http://www.ksz-bcss.fgov.be>`__

Table of contents:

.. contents::
   :local:


Coverage
========

Lino currently knows the following requests (French chunks of text
collected from various documents issued by http://www.bcss.fgov.be):

.. currentmodule:: lino_welfare.modlib.cbss.models

- :class:`IdentifyPersonRequest` : Identifier la personne par son NISS
  ou ses données phonétiques et vérifier son identité par le numéro de
  carte SIS, de carte d'identité ou par ses données phonétiques.

- :class:`ManageAccessRequest`: Enregistrer, désenregistrer ou
  consulter un dossier dans le registre du réseau de la sécurité
  sociale (registre BCSS) et dans le répertoire sectoriel des CPAS
  géré par la SmalS-MvM.
  
- :class:`RetrieveTIGroupsRequest
  <lino_welfare.modlib.cbss.tx25.RetrieveTIGroupsRequest>`: Obtenir
  des informations à propos d’une personne dans le cadre de l’enquête
  sociale.
  


Plugin configuration
====================

See :class:`lino_welfare.modlib.cbss.Plugin`.


Site configuration
==================

When this plugin is installed, then your :class:`SiteConfig
<lino.modlib.system.models.SiteConfig>` has the following additional
fields:

>>> show_fields(rt.models.system.SiteConfig, 
... "sector cbss_org_unit ssdn_user_id cbss_http_password")
+--------------------+-------------------------+-----------------------------------------------------------------------------------------+
| Internal name      | Verbose name            | Help text                                                                               |
+====================+=========================+=========================================================================================+
| sector             | sector                  | The CBSS sector/subsector of the requesting organization.                               |
|                    |                         | For PCSWs this is always 17.1.                                                          |
|                    |                         | Used in SSDN requests as text of the `MatrixID` and `MatrixSubID`                       |
|                    |                         | elements of `AuthorizedUser`.                                                           |
|                    |                         | Used in ManageAccess requests as default value                                          |
|                    |                         | for the non-editable field `sector`                                                     |
|                    |                         | (which defines the choices of the `purpose` field).                                     |
+--------------------+-------------------------+-----------------------------------------------------------------------------------------+
| cbss_org_unit      | Anfragende Organisation | In CBSS requests, identifies the requesting organization.                               |
|                    |                         | For PCSWs this is the enterprise number                                                 |
|                    |                         | (CBE, KBO) and should have 10 digits and no formatting characters.                      |
|                    |                         |                                                                                         |
|                    |                         | Used in SSDN requests as text of the `AuthorizedUser\OrgUnit` element .                 |
|                    |                         | Used in new style requests as text of the `CustomerIdentification\cbeNumber` element .  |
+--------------------+-------------------------+-----------------------------------------------------------------------------------------+
| ssdn_user_id       | SSDN User Id            | Used in SSDN requests as text of the `AuthorizedUser\UserID` element.                   |
+--------------------+-------------------------+-----------------------------------------------------------------------------------------+
| cbss_http_password | HTTP password           | Used in the http header of new-style requests.                                          |
+--------------------+-------------------------+-----------------------------------------------------------------------------------------+



.. _welfare.specs.cbss.tx25:

Tx25 requests
=============


>>> rt.show(cbss.RetrieveTIGroupsRequests,
...     column_names='user person environment status ticket')
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
================= ========================= ======= ================ ======================================
 Autor             Klient                    T/A/B   Zustand          Ticket
----------------- ------------------------- ------- ---------------- --------------------------------------
 Hubert Huppertz   AUSDEMWALD Alfons (116)   demo    OK               db1521da-3a61-43c0-b500-e96e9dd5c0ee
 Hubert Huppertz   AUSDEMWALD Alfons (116)   demo    OK               770c5e7d-8555-4ddd-9787-4e4f416c3d21
 Hubert Huppertz   AUSDEMWALD Alfons (116)   demo    OK               cd241a8b-2092-4f0c-b9d9-53a3707cdc3d
 Hubert Huppertz   AUSDEMWALD Alfons (116)   demo    Fehlgeschlagen
================= ========================= ======= ================ ======================================
<BLANKLINE>


Since the responses of many CBSS requests contain confidential data
about citizens, we have some rules for accessing this data.

- Only the user who initiated the request can see the results.
- Even the System Administrator cannot print nor see the detail of a
  CBSS request of other users.
- Only a *Security advisor* can see all data. Lino keeps a journal of
  every login as a security advisor.


We retrieve Tx25 no. 1 from the database. User Hubert (the social
agent who issued the request) can see the result:

>>> obj = cbss.RetrieveTIGroupsRequest.objects.get(pk=1)
>>> ses = rt.login('hubert')
>>> with translation.override('de'):
...    ses.show(cbss.RetrieveTIGroupsResult, obj)
============================== ===== ========== ====================================================================================================================================================================
 Gruppe                         TI    Seit       Information
------------------------------ ----- ---------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------
 NR-Nummer                            02.07.68   **68070201351** (Männlich)
 Wohnsitze                      001   18.10.01   **Estland** (136), Fusion: **0**, Sprache: **2**
                                      02.07.68   **Eupen** (63023), Fusion: **0**, Sprache: **2**
 Namen                          010   02.07.68   **Mustermann**, Max Moritz
 Legale Hauptadressen           020   30.07.97   **4700**, **Gülcherstrasse**, Nr. **21**
 Wohnsitz im Ausland            022   30.12.06   Address, PosteDiplomatique **Tallinn** (1418) **Estland** (136) **Estland** (136), **Bussijaama 2**, **10115 Tallinn**, **ESTONIA**
 Nationalitäten                 031   02.07.68   **Belgien** (150)
 Beschäftigungen                070   07.10.00   **Programmierer(in)** (09617) (SC  (9))
 Geburtsort                     100   02.07.68   in **Eupen** (63023), Akte Nr. **00000**
 Abstammung                     110   02.07.68   **Eheliches Kind** (00), von **Mustermann**, Michel Victor Edouard Henri (**33072102106**), und **Ausdemwald**, Anneliese (**34080402453**)
 Zivilstände                    120   07.10.00   **Verheiratet** (20), mit **Kasemets**, Kati (68042700000), in Place1 **Eupen** (63023), Akte Nr. **0098**
 Familienmitglieder             140   19.10.01   **Alleinstehend** (01)
 Familienoberhaupt              141   01.06.68   **Mustermann**, Michel Victor Edouard Henri (**33072102106**), als **Sohn** (03) (bis 30.10.96)
 Führerscheine (altes Modell)   194   06.02.87   **Zuteil.** (00), Kategorien B, Nr. **A043127**, ausgestellt in in **Eupen** (63023)
 Personalausweise               195   26.10.11   **P.A.** (0000) Nr. **591413288107**, gültig bis 19.08.16, ausgestellt in **Tallinn** (1418)
 Reisepässe                     199   23.09.02   Status: **Austel.** (0), Typ **Reisepass** (0), Nr. **EC51643900**, ausgestellt durch **Helsinki** (1262) (Botschaft), Erneuerungsnr.: **00**, gültig bis 22.09.07
 Erstelldatum                   253   05.09.15
 Zuletzt geändert               254   26.10.11
============================== ===== ========== ====================================================================================================================================================================
<BLANKLINE>

Any other user, even a site admin, cannot see the result:

>>> ses = rt.login('rolf')
>>> with translation.override('de'):
...    ses.show(cbss.RetrieveTIGroupsResult, obj, limit=5)
Confidential data

Except for users of the special user type who can see results of all
requests (but the Lino log files keep track of when that user logged
in).


Printing a Tx25
-----------------

>>> ses = rt.login('hubert')
>>> rv = ses.run(obj.do_print)
>>> print(rv['success'])
True
>>> print(rv['open_url'])
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/.../cbss.RetrieveTIGroupsRequest-1.odt



More examples of Tx25 results
=============================

This section is mostly for testing purposes.

>>> ses = rt.login('hubert')
>>> def showit(pk):
...     obj = cbss.RetrieveTIGroupsRequest.objects.get(pk=pk)
...     with translation.override('de'):
...         ses.show(cbss.RetrieveTIGroupsResult, obj)
>>> showit(2)  #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
============================== ===== ========== ===============================================================================================================================================================================
 Gruppe                         TI    Seit       Information
------------------------------ ----- ---------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 NR-Nummer                            07.03.68   **68030700123** (Männlich)
 Wohnsitze                      001   07.03.68   **Eupen** (63023), Fusion: **0**, Sprache: **2**
 Namen                          010   07.03.68   **Mustermann**, Frédéric Franz
 Legale Hauptadressen           020   17.11.04   **4701**, **Aachener Strasse**, Nr. **123**
                                      17.12.98   **4700**, **Binsterweg**, Nr. **12**
                                      02.12.97   **4700**, **Maria-Theresia-Strasse**, Nr. **12**
                                      12.01.97   **4701**, **Feldstrasse**, Nr. **12**
                                      10.05.95   **4700**, **Bahnhofstrasse**, Nr. **1**
                                      25.06.73   **4700**, **Maria-Theresia-Strasse**, Nr. **12**
                                      06.10.70   **4700**, **Obere Ibern**, Nr. **12**
                                      15.06.00   **4700**, **Monschauer Strasse**, Nr. **12**
 Nationalitäten                 031   07.03.68   **Belgien** (150)
 Beschäftigungen                070   06.06.06   **Informatiker(in)** (09620) (SC **(Gehalt.)** (4))
                                      02.12.93   **Angestellte(r)** (20928) (SC **(Gehalt.)** (4))
                                      22.03.84   **Schüler(in)** (04001) (SC  (9))
                                      07.03.80   **Ohne Beruf** (00002) (SC  (9))
 Geburtsort                     100   07.03.68   in **Eupen** (63023), Akte Nr. **00000**
 Abstammung                     110   07.03.68   **Eheliches Kind** (00), von **Mustermann**, Olivier Franz Frédéric (**40032303737**), und **Ausdemwald**, Maria Magdalena (**40010400251**)
 Zivilstände                    120   06.06.06   **Verheiratet** (20), mit **Mergelsberg**, Mélanie Anna (75081900208), in Place1 **Eupen** (63023), Akte Nr. **0055**
                                      08.06.98   **Geschieden** (41), in Tribunal **Entscheid des erstinstanzlichen Gerichtes** (01), Date 08.05.98, Place **Eupen** (63023), Akte Nr. **0063**
                                      30.12.95   **Verheiratet** (20), mit **Keutgens**, Claudia (70042500230), in Place1 **Eupen** (63023), Akte Nr. **0159**
                                      07.03.68   **Unverheiratet** (10)
 Legale Kohabitationen          123   06.06.06   Beendigung: Begründung: **Eheschliessung** (01), in **Eupen** (63023)
                                      20.11.03   Deklaration: 21.11.03, mit **75081900208** **Mergelsberg**, Mélanie Anna, in **Eupen** (63023)
 Familienmitglieder             140   02.12.97   **Alleinstehend** (01) (bis 18.11.03)
                                      30.12.95   **Gemahlin** (02), in Familie mit Vorstand **Keutgens**, Claudia (**70042500230**) (bis 02.12.97)
                                      06.06.06   **Gemahlin** (02), in Familie mit Vorstand **Mergelsberg**, Mélanie Anna (**75081900208**)
                                      10.05.95   **nicht verwandt** (12), in Familie mit Vorstand **Keutgens**, Claudia (**70042500230**) (bis 30.12.95)
                                      18.11.03   **nicht verwandt** (12), in Familie mit Vorstand **Mergelsberg**, Mélanie Anna (**75081900208**) (bis 06.06.06)
 Familienoberhaupt              141   07.03.68   **Mustermann**, Olivier Franz Frédéric (**40032303737**), als **Sohn** (03) (bis 10.05.95)
 Organspenden                   192   27.04.12   **Ausdrückliches Einverständnis** (20), in **Eupen** (63023)
 Führerscheine (altes Modell)   194   01.10.86   **Zuteil.** (00), Kategorien B, Nr. **A043009**, ausgestellt in in **Eupen** (63023)
                                      06.06.86   **Zuteil.** (00), Kategorien AGFS kl. B, Nr. **J000730**, ausgestellt in in **Eupen** (63023)
 Personalausweise               195   09.02.10   **P.A.** (0000) Nr. **591020075668**, gültig bis 16.01.15, ausgestellt in **Eupen** (63023)
                                      19.04.05   **P.A.** (0000) Nr. **590057563866**
                                      05.02.01   **P.A.** (0000) Nr. **427003700404**
                                      10.05.91   **P.A.** (0000) Nr. **427001773336**
                                      18.08.86   **P.A.** (0000) Nr. **427000131309**
                                      22.03.84   **P.A.** (0000) Nr. **AL 093189**, ausgestellt in **Eupen** (63023)
                                      11.03.80   **P.A.** (0000) Nr. **AL 011283**, ausgestellt in **Eupen** (63023)
                                      08.03.68   **P.A. Kd. ** (0060) Nr. **   005749**, ausgestellt in **Eupen** (63023)
 Reisepässe                     199   31.01.11   Status: **Ausstellung** (0), Typ **Reisepass** (0), Nr. **EH960150  **, ausgestellt durch **Eupen** (63023), Erneuerungsnr.: **00**, prodziert: 21.01.11, gültig bis 20.01.16
 Erstelldatum                   253   05.09.15
 Zuletzt geändert               254   27.04.12
============================== ===== ========== ===============================================================================================================================================================================
<BLANKLINE>


>>> showit(3)  #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS +REPORT_UDIFF
======================== ===== ========== ======================================================================================================================================================================================
 Gruppe                   TI    Seit       Information
------------------------ ----- ---------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 NR-Nummer                      26.05.98   **980526 001-51** (Männlich)
 Wohnsitze                001   16.11.15   **Eupen** (63023), Fusion: **0**, Sprache: **2**
                                23.07.92   **Deutschland (Bundesrep.)** (103), Fusion: **0**, Sprache: **2**
                                20.12.91   **Kelmis** (63040), Fusion: **0**, Sprache: **2**
                                20.01.88   **Deutschland (Bundesrep.)** (103), Fusion: **0**, Sprache: **2**
                                09.05.72   **Limbourg** (63046), Fusion: **0**, Sprache: **2**
                                17.12.70   **Membach** (63051), Fusion: **0**, Sprache: **2**
                                20.12.67   **Henri-Chapelle** (63032), Fusion: **0**, Sprache: **2**
 Adressänderungsabsicht   005   16.11.15   Umziehen nach **Eupen** (63023)
                                25.04.72   Wegziehen aus **Membach** (63051)
 Ursprungsländer          006   16.11.15   **Deutschland (Bundesrep.)** (103) **Niederkassel,Bergtraße**
                                20.12.91   **Deutschland (Bundesrep.)** (103) **Niederkassel,Bahnhofstr.7**
 Namen                    010   13.10.53   **Adam**, Albert
 Legale Hauptadressen     020   16.11.15   **4700**, **Hütte**, Nr. **12**
                                20.12.91   **4720**, **Kirchstrasse**, Nr. **33**
                                14.04.82   **4830**, **Rue Oscar Thimus**, Nr. **123**
                                09.05.72   **4830**, **Avenue Victor David**, Nr. **31**
                                17.12.70   **4837**, **Rue du Moulin(MCH)**, Nr. **112** **A000**
 Wohnsitz im Ausland      022   30.05.15   Address, PosteDiplomatique **Berlin** (1202) **Deutschland (Bundesrep.)** (103) **Deutschland (Bundesrep.)** (103), **Kirchstr. 38**, **53859 Niederkassel-Lulsdorf** (bis 16.11.15)
                                16.04.07   Address, PosteDiplomatique **Köln** (1207) **Deutschland (Bundesrep.)** (103) **Deutschland (Bundesrep.)** (103), **Kirchstr. 123**, **53859 Niederkassel**, **GERMANY**
                                13.12.06   Address, PosteDiplomatique **Köln** (1207) **Deutschland (Bundesrep.)** (103) **Deutschland (Bundesrep.)** (103), **Bonner Str. 12**, **53842 Troisdorf**, **GERMANY**
                                22.06.99   Address, PosteDiplomatique **Köln** (1207) **Deutschland (Bundesrep.)** (103) **Adenauerstrasse 12 - 53842 Troisdorf**
                                30.11.81   Address, PosteDiplomatique **Frankfurt am Main** (1204) **Deutschland (Bundesrep.)** (103) ** D 5300 BONN,IN DER WEHRHECKE 12** (bis 08.01.92)
                                05.03.81   Address, PosteDiplomatique **Frankfurt am Main** (1204) **Deutschland (Bundesrep.)** (103) ** 5841 KRAELINGEN,VILMAHOHE 123**
 Postadresse im Ausland   023   30.11.81   Datum: 30.11.81, **D 5300 BONN,IN DER WEHRHEDKE 12 ** (bis 08.01.92)
                                05.03.81   Datum: 05.03.81, **D 5841 KRAELINGEN,VILMAHOHE 123 **
 Nationalitäten           031   13.10.53   **Belgier/in/** (150)
 Beschäftigungen          070   18.02.02   **Kellner(in)** (91401) (SC **(Lohn.)** (3))
                                22.06.99   **Hausfrau** (91102) (SC  (9))
                                20.12.91   **Kabarettier** (30228) (SC **(Selbst.)** (2))
                                01.03.81   **Tagelöhner(in)** (89915) (SC **(Lohn.)** (3))
                                09.05.72   **Ohne Beruf** (00002) (SC  (9))
 Geburtsort               100   13.10.53   in **Raeren** (63061), Akte Nr. **00000**
 Abstammung               110   13.10.53   **Kind** (00), von **Adam**, Ilja Noémie Odette Pascale (**971207 001-67**), und **Adam**, Alicia Hans (**960715 002-61**)
 Zivilstände              120   15.09.94   **Geschieden** (40), mit **Adam**, Andreas (970101 001-73), in Place2 **Deutschland (Bundesrep.)** (103), **Siegburg**, Akte Nr. **0254**
                                04.12.84   **Verheiratet** (20), mit **Adam**, Annette (950221 001-20), in Place2 **Deutschland (Bundesrep.)** (103), **Niederkassel**
                                24.11.83   **Geschieden** (40), in Place2 **Deutschland (Bundesrep.)** (103)
                                03.06.72   **Verheiratet** (20), mit **Adam**, Alfons Laurent Bernard Bruno (900627 002-53), in Place1 **Eupen** (63023)
                                13.10.53   **Unverheiratet** (10)
 Familienmitglieder       140   16.11.15   Housing  (00), **Alleinstehende** (01)
                                04.11.81   **Alleinstehende** (01) (bis 05.01.84)
                                11.02.92   **Sohn** (03), in Familie mit Vorstand **Adam**, Jan Bruno (**890722 001-93**) (bis 23.07.92)
                                11.02.92   **Sohn** (03), in Familie mit Vorstand **Adam**, Kevin (**900108 001-07**) (bis 17.07.92)
                                20.12.91   **Tochter** (03), in Familie mit Vorstand **Adam**, Lars (**921024 001-20**) (bis 16.11.15)
                                20.12.91   **Tochter** (03), in Familie mit Vorstand **Adam**, Monique (**901214 001-01**) (bis 16.11.15)
 Familienoberhaupt        141   05.01.84   **Adam**, Alicia Hans (**960715 002-61**), als **Tochter** (03) (bis 20.12.91)
                                03.06.72   **Adam**, Alfons Laurent Bernard Bruno (**900627 002-53**), als **Gemahlin** (02) (bis 04.11.81)
 Personalausweise         195   14.06.72   **P.A.** (0000) Nr. **AE 123456**, ausgestellt in **Limbourg** (63046)
 Reisepässe               199   25.07.00   Status: **Austel.** (0), Typ **Reisepass** (0), Nr. **AE 234567**, ausgestellt durch **Köln** (1207) (Botschaft), Erneuerungsnr.: **00**, gültig bis 24.07.05
 Wohnsitzänderungen       251   19.11.15
 Erstelldatum             253   12.03.71
 Zuletzt geändert         254   19.11.15
======================== ===== ========== ======================================================================================================================================================================================
<BLANKLINE>


>>> showit(4)  #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
============================= ===== ========== ==========================================================================================================================
 Gruppe                        TI    Seit       Information
----------------------------- ----- ---------- --------------------------------------------------------------------------------------------------------------------------
 NR-Nummer                           26.05.98   **980526 001-51** (Männlich)
 Wohnsitze                     001   13.02.84   **Eupen** (63023), Fusion: **0**, Sprache: **2**
 Namen                         010   13.02.84   **Abbas**, Ambroise
 Adressänderungs-Deklaration   019   14.10.15   **4700(2901) Nöretherstrasse,14**
 Legale Hauptadressen          020   06.01.15   **4700**, **Bergkapellstrasse**, Nr. **12**
                                     24.05.12   **4700**, **Hostert**, Nr. **13**
                                     29.03.11   **4700**, **Hochstrasse**, Nr. **14**
                                     24.04.08   **4700**, **Kaperberg**, Nr. **15**
                                     03.12.02   **4700**, **Herbesthaler Strasse**, Nr. **16** **   B**
                                     14.05.85   **4700**, **Nöretherstrasse**, Nr. **17**
                                     13.02.84   **4700**, **Werthplatz**, Nr. **18**
 Nationalitäten                031   13.02.84   **Belgier/in/** (150)
 Beschäftigungen               070   25.03.06   **Ohne Beruf** (00002) (SC  (9))
 Geburtsort                    100   13.02.84   in **Eupen** (63023), Akte Nr. **00000**
 Abstammung                    110   13.02.84   **Kind** (00), von **Abbas**, Adélaïde Amédée (**971207 001-67**), und **Bah**, Adèle Anastase Agnès (**960715 002-61**)
 Zivilstände                   120   20.01.15   **Geschieden** (41), mit **Adriaen**, Arthur Alix (970101 001-73), in Date 27.11.14, Akte Nr. **0011**
                                     25.03.06   **Verheiratet** (20), mit **Adriaen**, Arthur Alix (970101 001-73), in Place1 **Eupen** (63023), Akte Nr. **0030**
                                     13.02.84   **Unverheiratet** (10)
 Familienoberhaupt             141   24.05.12   **Abbasi**, Augustin (**950221 001-20**), als **nicht verwandt** (12), Housing  (00)
                                     25.03.06   **Adriaen**, Arthur Alix (**970101 001-73**), als **Gemahlin** (02) (bis 24.05.12)
                                     03.12.02   **Adriaen**, Arthur Alix (**970101 001-73**), als **nicht verwandt** (12)
                                     13.02.84   **Abbas**, Adélaïde Amédée (**971207 001-67**), als **Tochter** (03)
 Personalausweise              195   31.08.15   **P.A.** (0000) Nr. **AE 123456**, gültig bis 07.07.25, ausgestellt in **Eupen** (63023)
                                     07.07.15   **Anlage 12-Bescheinigung ** (0120) Nr. **AE 234567**, gültig bis 07.08.15, ausgestellt in **Eupen** (63023)
                                     10.05.10   **P.A.** (0000) Nr. **AE 345678**, gültig bis 21.04.15, ausgestellt in **Eupen** (63023)
                                     26.05.05   **P.A.** (0000) Nr. **AE 456789**
                                     23.05.01   **P.A.** (0000) Nr. **AE 567890**
                                     09.02.96   **P.A.** (0000) Nr. **AE 123456**
                                     13.02.92   **P.A. Kd. ** (0060) Nr. **AE 234567**, ausgestellt in **Eupen** (63023)
                                     14.02.84   **P.A. Kd. ** (0060) Nr. **AE 345678**, ausgestellt in **Eupen** (63023)
 Erstelldatum                  253   14.02.84
 Zuletzt geändert              254   14.10.15
============================= ===== ========== ==========================================================================================================================
<BLANKLINE>
