.. doctest docs/specs/b2c.rst
.. _welfare.specs.b2c:

=============================================
Import bank statements (SEPA  BankToCustomer)
=============================================

This document describes the functionality implemented by the
:mod:`lino_cosi.lib.b2c` module.

..  doctest initialization:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *

    >>> ses = rt.login('rolf')
    >>> translation.activate('de')

.. contents::
   :local:
   :depth: 2


>>> rt.show(b2c.Accounts)
================================= ===== ================== ===================================== ================================ ==================
 IBAN                              BIC   Last transaction   Partner                               Name Inhaber                     Kontobezeichnung
--------------------------------- ----- ------------------ ------------------------------------- -------------------------------- ------------------
 AL73552891583236787384690218            07.09.15           *Belgisches Rotes Kreuz*              Garage Mergelsberg
 AL66383778998922195726400092            07.09.15           *Rumma & Ko OÜ*                       Reinhards Baumschule
 AD5257784281812851432256                07.09.15           *Bäckerei Ausdemwald*                 Auto École Verte
 AT233377816198914246                    07.09.15           *Bäckerei Mießen*                     Evers Eberhart
 AZ72AOZV21841200481951294949            07.09.15           *Bäckerei Schmitz*                    Kaivers Karl
 BH50GDHO00603036234521                  07.09.15           *Garage Mergelsberg*                  Lazarus Line
 BH29GWOZ41746150114337                  07.09.15           *Donderweer BV*                       Malmendier Marc
 BE83540256917919                        07.09.15           *Van Achter NV*                       Emonts-Gast Erna
 BE62315236188996                        07.09.15           *Hans Flott & Co*                     Radermacher Berta
 BE94532216847099                        07.09.15           *Bernd Brechts Bücherladen*           Radermacher Fritz
 BE96553733406075                        07.09.15           *Reinhards Baumschule*                Radermacher Hans
 BA086304331850728340                    07.09.15           *Moulin Rouge*                        di Rupo Didier
 BR2701798507625253316527482W6           07.09.15           *Auto École Verte*                    Radermecker Rik
 BR8916505915221714901465542D6           07.09.15           *Arens Andreas*                       Denon Denis
 BG33WODO90876019575940                  07.09.15           *Arens Annette*                       AS Express Post
 BG89NKTJ64315412156435                  07.09.15           *Altenberg Hans*                      IIZI kindlustusmaakler AS
 BG45LMDF68752666847493                  07.09.15           *Ausdemwald Alfons*                   Leffin Electronics
 MK42869572001783450                     07.09.15           *Bastiaensen Laurent*                 R-Cycle Sperrgutsortierzentrum
 CY94595189933551887423183914            07.09.15           *Collard Charlotte*                   Brocal Catherine
 CY67178463066674360903454329            07.09.15           *Charlier Ulrike*                     Baguette Stéphanie
 CZ9233597294072726325676                07.09.15           *Chantraine Marc*                     Gerkens Gerd
 CZ6595671096439786778328                07.09.15           *Dericum Daniel*                      Oikos
 DK4827862790127019                      07.09.15           *Demeulenaere Dorothée*               Gerkens-Kasennova
 DK1358026849419971                      07.09.15           *Dobbelstein-Demeulenaere Dorothée*   Jeanémart-Thelen
 DK0905734385914385                      07.09.15           *Dobbelstein Dorothée*                Frisch Ludwig
 DO64127641001569019111921598            07.09.15           *Ernst Berta*                         Frisch Bernd
 DO40144771611278919843152876            08.09.15           *Evertz Bernd*                        Frisch Peter
 DO34894434296388176648298583            07.09.15           *Evers Eberhart*                      Frisch Clara
 DO87947053138589917553903987            07.09.15           *Emonts Daniel*                       Frisch Dennis
 EE436294797788261706                    07.09.15           *Engels Edgar*                        Frisch Melba
 EE386024163501444960                    07.09.15           *Faymonville Luc*                     Frisch-Frogemuth
 KW17RZFN7035889356330572874320          07.09.15           *Gernegroß Germaine*                  Zweith Petra
 MT48FZJE39412800316166455316545         07.09.15           *Groteclaes Gregory*                  Jousten Jan
 MC8574374915374698884193509             08.09.15           *Hilgers Hildegard*                   Lahm Lisa
================================= ===== ================== ===================================== ================================ ==================
<BLANKLINE>

>>> obj = rt.models.contacts.Partner.objects.get(name="Belgisches Rotes Kreuz")
>>> rt.show(sepa.AccountsByClient, obj)
========== ============================== ========== ======== =========== ==============
 Kontoart   IBAN                           BIC        Primär   Verwaltet   Kontoauszüge
---------- ------------------------------ ---------- -------- ----------- --------------
 Giro       AL73552891583236787384690218              Nein     Nein        *07.09.15*
 Giro       BE39088213644919               GKCCBEBB   Ja       Nein
========== ============================== ========== ======== =========== ==============
<BLANKLINE>

>>> pa = sepa.Account.objects.filter(partner=obj)[0]
>>> ia = b2c.Account.objects.get(iban=pa.iban)
>>> rt.show(b2c.StatementsByAccount, ia)
====================== ============== ============ ============== ========== =========
 Auszugsnummer          Alter Saldo    Beginnt am   Neuer Saldo    Enddatum   Währung
---------------------- -------------- ------------ -------------- ---------- ---------
 2015/0104              2 378,68       04.09.15     2 308,68       07.09.15   EUR
 **Total (1 Zeilen)**   **2 378,68**                **2 308,68**
====================== ============== ============ ============== ========== =========
<BLANKLINE>

Now let's look at the transactions in this statement:

>>> stmt = b2c.Statement.objects.get(account=ia)
>>> rt.show(b2c.TransactionsByStatement, stmt)
+----------------------+------------+---------------------------------------------------+----------------------------------------------------------------------+
| Ausführungsdatum     | Betrag     | Gegenpartei                                       | Meldung                                                              |
+======================+============+===================================================+======================================================================+
| 07.09.15             | -70,00     | AL52238964890057847269894484 (BIC:GKCCBEBB) |br|  | |br|                                                                 |
|                      |            | **Donderweer BV**,  |br|                          | eref::  |br|                                                         |
|                      |            | ,                                                 | **Ordre permanent** Valuta: **07.09.15** Buchungsdatum: **07.09.15** |
+----------------------+------------+---------------------------------------------------+----------------------------------------------------------------------+
| **Total (1 Zeilen)** | **-70,00** |                                                   |                                                                      |
+----------------------+------------+---------------------------------------------------+----------------------------------------------------------------------+
<BLANKLINE>

Note that **Ordre permanent** is in French (not English) because we do
not yet find the officeal German translations for the Beglian bank
transaction codes (see :mod:`lino_cosi.lib.b2c.febelfin`)
