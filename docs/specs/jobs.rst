.. _welfare.specs.jobs:
.. _welfare.tested.jobs:

===============
The Jobs plugin
===============

.. to test only this document:

    $ doctest docs/specs/jobs.rst
    
    doctest initialization:
    
    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *


The :mod:`lino_welfare.modlib.jobs` plugin provides functionality for
managing *job supplyment* (German *Art-60§7-Konventionen*, French
*Mise à l'emploi*).

A **job supplyment** is when the PCSW arranges a job for a client,
with the aim to bring this person back into the social security system
and the employment process. In most cases, the PSWC acts as the legal
employer.  It can employ the person in its own services (internal
contracts) or put him/her at the disposal of a third party employer
(external contracts). (Adapted from `mi-is.be
<http://www.mi-is.be/en/public-social-welfare-centers/article-60-7>`_).

This plugin needs the :mod:`lino_welfare.modlib.isip` plugin. Job
supplyment projects (:class:`jobs.Contract
<lino_welfare.modlib.jobs.models.Contract>`) are a specialized form of
*ISIP projects* (:class:`isip.Contract
<lino_welfare.modlib.isip.models.Contract>`).

.. contents::
   :local:
   :depth: 1


We log in as Rolf:

>>> ses = rt.login('rolf')

Jobs
====

The central concept added by this module is a table of **jobs**.

>>> with translation.override('de'):
...     ses.show(jobs.Jobs, column_names="function provider sector")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ================================ ==========================
 Funktion          Stellenanbieter                  Sektor
----------------- -------------------------------- --------------------------
 Kellner           BISA                             Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum   Horeca
 Koch              R-Cycle Sperrgutsortierzentrum   Seefahrt
 Koch              Pro Aktiv V.o.G.                 Unterricht
 Küchenassistent   Pro Aktiv V.o.G.                 Medizin & Paramedizin
 Küchenassistent   BISA                             Reinigung
 Tellerwäscher     BISA                             Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum   Transport
================= ================================ ==========================
<BLANKLINE>


Job providers
=============

>>> ses.show(jobs.JobProviders)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================================ ============ ================ ========= ===== ===== =========
 Name                             Adresse      E-Mail-Adresse   Telefon   GSM   ID    Sprache
-------------------------------- ------------ ---------------- --------- ----- ----- ---------
 BISA                             4700 Eupen                                    188   de
 Pro Aktiv V.o.G.                 4700 Eupen                                    191   de
 R-Cycle Sperrgutsortierzentrum   4700 Eupen                                    189   de
================================ ============ ================ ========= ===== ===== =========
<BLANKLINE>

.. _welfare.jobs.Offers:

Job Offers
==========


>>> # settings.SITE.catch_layout_exceptions = False
>>> ses.show(jobs.Offers)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
======================== ================== ========================= ========== ================ ============== =============
 Name                     Stellenanbieter    Sektor                    Funktion   Beginn Auswahl   Ende Auswahl   Beginndatum
------------------------ ------------------ ------------------------- ---------- ---------------- -------------- -------------
 Übersetzer DE-FR (m/w)   Pro Aktiv V.o.G.   Landwirtschaft & Garten   Kellner    22.01.14         02.05.14       01.06.14
======================== ================== ========================= ========== ================ ============== =============
<BLANKLINE>


.. _welfare.jobs.ExperiencesByOffer:

Experiences by Job Offer
------------------------

This table shows the Experiences which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.ExperiencesByOffer, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============ ========== ==================== =================================== ===================
 Beginnt am   Enddatum   Klient               Organisation                        Land
------------ ---------- -------------------- ----------------------------------- -------------------
 07.02.11     07.03.11   LAZARUS Line (144)   Belgisches Rotes Kreuz              Andorra
 04.04.11     04.04.13   JONAS Josef (139)    Pharmacies Populaires de Verviers   Brunei Darussalam
============ ========== ==================== =================================== ===================
<BLANKLINE>



.. _welfare.jobs.CandidaturesByOffer:

Candidatures by Job Offer
-------------------------

This table shows the Candidatures which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.CandidaturesByOffer.request(obj))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============== ======================= ======== ====================
 Anfragedatum   Klient                  Stelle   Kandidatur-Zustand
-------------- ----------------------- -------- --------------------
 02.05.14       MALMENDIER Marc (146)            Inaktiv
 27.06.14       KAIVERS Karl (141)               Arbeitet
============== ======================= ======== ====================
<BLANKLINE>



>>> ses.show(jobs.ContractTypes)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
=========================== ==========
 Bezeichnung                 Referenz
--------------------------- ----------
 Sozialökonomie              art60-7a
 Sozialökonomie - majoré     art60-7b
 Stadt Eupen                 art60-7e
 mit Rückerstattung          art60-7c
 mit Rückerstattung Schule   art60-7d
=========================== ==========
<BLANKLINE>



Show all contracts
------------------

Via :menuselection`Explorer --> DSBE --> Art.60§7-Konventionen` you
can see a list of all job supplyment contracts.

>>> show_menu_path(jobs.Contracts)
Explorer --> DSBE --> Art.60§7-Konventionen

The demo database contains 16 job supplyment contracts:

>>> ses.show(jobs.Contracts)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ============================= =============== ============== ========== ================================================== ================= ===========================
 ID   Klient                        NR-Nummer       Laufzeit von   Enddatum   Stelle                                             Autor             Art
---- ----------------------------- --------------- -------------- ---------- -------------------------------------------------- ----------------- ---------------------------
 1    COLLARD Charlotte (118)       960715 002-61   04.10.12       03.10.13   Kellner bei BISA                                   Alicia Allmanns   Sozialökonomie
 2    EVERTZ Bernd (126)            890722 001-93   14.10.12       13.04.14   Kellner bei R-Cycle Sperrgutsortierzentrum         Alicia Allmanns   mit Rückerstattung Schule
 3    FAYMONVILLE Luc (130*)        890202 001-76   03.11.12       02.11.13   Koch bei R-Cycle Sperrgutsortierzentrum            Alicia Allmanns   Sozialökonomie - majoré
 4    FAYMONVILLE Luc (130*)        890202 001-76   03.11.13       03.11.14   Koch bei Pro Aktiv V.o.G.                          Hubert Huppertz   Sozialökonomie
 5    HILGERS Hildegard (133)       870325 002-29   13.11.12       12.11.14   Küchenassistent bei Pro Aktiv V.o.G.               Alicia Allmanns   Stadt Eupen
 6    LAMBERTZ Guido (142)          810823 001-96   03.12.12       02.12.14   Küchenassistent bei BISA                           Alicia Allmanns   Sozialökonomie - majoré
 7    MALMENDIER Marc (146)         791013 001-77   13.12.12       12.12.13   Tellerwäscher bei BISA                             Alicia Allmanns   mit Rückerstattung
 8    MALMENDIER Marc (146)         791013 001-77   13.12.13       13.12.14   Tellerwäscher bei R-Cycle Sperrgutsortierzentrum   Mélanie Mélard    Stadt Eupen
 9    RADERMACHER Christian (155)   761227 001-93   02.01.13       01.01.14   Kellner bei BISA                                   Alicia Allmanns   Sozialökonomie
 10   RADERMACHER Christian (155)   761227 001-93   02.01.14       02.01.15   Kellner bei R-Cycle Sperrgutsortierzentrum         Mélanie Mélard    mit Rückerstattung Schule
 11   RADERMACHER Fritz (158)       750805 001-25   12.01.13       11.01.15   Koch bei R-Cycle Sperrgutsortierzentrum            Alicia Allmanns   Sozialökonomie - majoré
 12   VAN VEEN Vincent (166)        710528 001-06   01.02.13       31.01.15   Koch bei Pro Aktiv V.o.G.                          Alicia Allmanns   Sozialökonomie
 13   RADERMECKER Rik (173)         730407 001-89   11.02.13       10.02.14   Küchenassistent bei Pro Aktiv V.o.G.               Mélanie Mélard    Stadt Eupen
 14   RADERMECKER Rik (173)         730407 001-89   11.02.14       11.02.15   Küchenassistent bei BISA                           Hubert Huppertz   Sozialökonomie - majoré
 15   DENON Denis (180*)            950810 001-04   03.03.13       02.03.14   Tellerwäscher bei BISA                             Alicia Allmanns   mit Rückerstattung
 16   DENON Denis (180*)            950810 001-04   03.03.14       03.03.15   Tellerwäscher bei R-Cycle Sperrgutsortierzentrum   Hubert Huppertz   Stadt Eupen
==== ============================= =============== ============== ========== ================================================== ================= ===========================
<BLANKLINE>

Use the filter parameters to show e.g. only contracts which were
active on 05.10.2012:

>>> pv = dict(observed_event=isip.ContractEvents.active,
...     start_date=i2d(20121005), end_date=i2d(20121005))
>>> kwargs = dict()
>>> kwargs.update(param_values=pv)
>>> ses.show(jobs.Contracts, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ========================= =============== ============== ========== ================== ================= ================
 ID   Klient                    NR-Nummer       Laufzeit von   Enddatum   Stelle             Autor             Art
---- ------------------------- --------------- -------------- ---------- ------------------ ----------------- ----------------
 1    COLLARD Charlotte (118)   960715 002-61   04.10.12       03.10.13   Kellner bei BISA   Alicia Allmanns   Sozialökonomie
==== ========================= =============== ============== ========== ================== ================= ================
<BLANKLINE>

Use the filter parameters to show e.g. only contracts which started in
October 2012:

>>> pv.update(observed_event=isip.ContractEvents.started,
...     start_date=i2d(20121001), end_date=i2d(20121030))
>>> ses.show(jobs.Contracts, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ========================= =============== ============== ========== ============================================ ================= ===========================
 ID   Klient                    NR-Nummer       Laufzeit von   Enddatum   Stelle                                       Autor             Art
---- ------------------------- --------------- -------------- ---------- -------------------------------------------- ----------------- ---------------------------
 1    COLLARD Charlotte (118)   960715 002-61   04.10.12       03.10.13   Kellner bei BISA                             Alicia Allmanns   Sozialökonomie
 2    EVERTZ Bernd (126)        890722 001-93   14.10.12       13.04.14   Kellner bei R-Cycle Sperrgutsortierzentrum   Alicia Allmanns   mit Rückerstattung Schule
==== ========================= =============== ============== ========== ============================================ ================= ===========================
<BLANKLINE>




Evaluations of a contract
-------------------------

>>> obj = jobs.Contract.objects.get(pk=6)
>>> print(unicode(obj.client))
LAMBERTZ Guido (142)

>>> obj.active_period()
(datetime.date(2012, 12, 3), datetime.date(2014, 12, 2))

>>> obj.update_cal_rset()
ExamPolicy #3 ('Alle 3 Monate')

>>> print(unicode(obj.update_cal_rset().event_type))
Auswertung
>>> print(obj.update_cal_rset().event_type.max_conflicting)
4
>>> settings.SITE.verbose_client_info_message = True
>>> [str(i.start_date) for i in obj.get_existing_auto_events()]
['2013-03-04', '2013-06-04', '2013-09-04', '2013-12-04', '2014-03-04', '2014-06-04', '2014-09-04']
>>> wanted, unwanted = obj.get_wanted_auto_events(ses)
>>> print(ses.response['info_message'])
Generating events between 2013-03-04 and 2014-12-02 (max. 72).
Reached upper date limit 2014-12-02


>>> settings.SITE.site_config.hide_events_before = None

>>> ses.show(cal.EntriesByController.request(obj),
... column_names="when_html summary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================== ==================
 Wann               Kurzbeschreibung
------------------ ------------------
 **Mo. 04.03.13**   Évaluation 1
 **Di. 04.06.13**   Évaluation 2
 **Mi. 04.09.13**   Évaluation 3
 **Mi. 04.12.13**   Évaluation 4
 **Di. 04.03.14**   Évaluation 5
 **Mi. 04.06.14**   Évaluation 6
 **Do. 04.09.14**   Évaluation 7
================== ==================
<BLANKLINE>

Mélanie has two appointments on 2014-09-15 (TODO: this test currently
fails because coaching stories have changed. Currently there's no
similar case in the demo data. See :ticket:`13`):

>>> d = i2d(20140915)
>>> pv = dict(start_date=d, end_date=d)
>>> ses.show(cal.EntriesByDay.request(param_values=pv),
...     column_names="user summary project")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +SKIP
================ =============== =========================
 Managed by       Summary         Client
---------------- --------------- -------------------------
 Mélanie Mélard   Appointment 3   FAYMONVILLE Luc (130*)
 Mélanie Mélard   Appointment 5   JACOBS Jacqueline (137)
================ =============== =========================
<BLANKLINE>

This is because the EventType of these automatically generated
evaluation appointments is configured to allow for up to 4
conflicting events:

>>> e = cal.EntriesByDay.request(param_values=pv).data_iterator[0]
>>> e.event_type
EventType #5 ('Auswertung')
>>> e.event_type.max_conflicting
4


JobsOverview
------------

The :class:`JobsOverview
<lino_welfare.modlib.jobs.models.JobsOverview>` report
helps integration agents to make decisions like:

    - which jobs are soon going to be free, and which candidate(s) should we
      suggest?

Example content:

>>> ses.show(jobs.JobsOverview)
----------------------------
Sozialwirtschaft = "majorés"
----------------------------
<BLANKLINE>
+--------------------------------------------------------------------+--------------------------------------------------------+-------------------------------------+--------------------------------------+
| Stelle                                                             | Arbeitet                                               | Probezeit                           | Kandidaten                           |
+====================================================================+========================================================+=====================================+======================================+
| `Kellner <Detail>`__ bei `BISA <Detail>`__ (1) *Sehr harte Stelle* |                                                        | `RADERMACHER Hedi (161) <Detail>`__ | `ENGELS Edgar (129) <Detail>`__      |
+--------------------------------------------------------------------+--------------------------------------------------------+-------------------------------------+--------------------------------------+
| `Koch <Detail>`__ bei `Pro Aktiv V.o.G. <Detail>`__ (1)            | `VAN VEEN Vincent (166) <Detail>`__ bis 31.01.15 |br|  | `EMONTS-GAST Erna (152) <Detail>`__ | `JACOBS Jacqueline (137) <Detail>`__ |
|                                                                    | `FAYMONVILLE Luc (130*) <Detail>`__ bis 03.11.14       |                                     |                                      |
+--------------------------------------------------------------------+--------------------------------------------------------+-------------------------------------+--------------------------------------+
<BLANKLINE>
------
Intern
------
<BLANKLINE>
+----------------------------------------------------------------------------+------------------------------------------------------+--------------------------------------+------------------------------------+
| Stelle                                                                     | Arbeitet                                             | Probezeit                            | Kandidaten                         |
+============================================================================+======================================================+======================================+====================================+
| `Koch <Detail>`__ bei `R-Cycle Sperrgutsortierzentrum <Detail>`__ (1)      | `RADERMACHER Fritz (158) <Detail>`__ bis 11.01.15    | `AUSDEMWALD Alfons (116) <Detail>`__ | `MEESSEN Melissa (147) <Detail>`__ |
+----------------------------------------------------------------------------+------------------------------------------------------+--------------------------------------+------------------------------------+
| `Küchenassistent <Detail>`__ bei `BISA <Detail>`__ (1) *Sehr harte Stelle* | `LAMBERTZ Guido (142) <Detail>`__ bis 02.12.14 |br|  | `BRECHT Bernd (177) <Detail>`__      | `JONAS Josef (139) <Detail>`__     |
|                                                                            | `RADERMECKER Rik (173) <Detail>`__ bis 11.02.15      |                                      |                                    |
+----------------------------------------------------------------------------+------------------------------------------------------+--------------------------------------+------------------------------------+
<BLANKLINE>
----------------------------------------------
Extern (Öffentl. VoE mit Kostenrückerstattung)
----------------------------------------------
<BLANKLINE>
+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+---------------------------------+--------------------------------------+
| Stelle                                                                                                           | Arbeitet                                              | Probezeit                       | Kandidaten                           |
+==================================================================================================================+=======================================================+=================================+======================================+
| `Küchenassistent <Detail>`__ bei `Pro Aktiv V.o.G. <Detail>`__ (1) *No supervisor. Only for independent people.* | `HILGERS Hildegard (133) <Detail>`__ bis 12.11.14     | `JONAS Josef (139) <Detail>`__  |                                      |
+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+---------------------------------+--------------------------------------+
| `Tellerwäscher <Detail>`__ bei `R-Cycle Sperrgutsortierzentrum <Detail>`__ (1)                                   | `MALMENDIER Marc (146) <Detail>`__ bis 13.12.14 |br|  | `ENGELS Edgar (129) <Detail>`__ | `RADERMACHER Guido (159) <Detail>`__ |
|                                                                                                                  | `DENON Denis (180*) <Detail>`__ bis 03.03.15          |                                 |                                      |
+------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+---------------------------------+--------------------------------------+
<BLANKLINE>
------------------------------------
Extern (Privat Kostenrückerstattung)
------------------------------------
<BLANKLINE>
====================================================== ========== ================================= ==================================
 Stelle                                                 Arbeitet   Probezeit                         Kandidaten
------------------------------------------------------ ---------- --------------------------------- ----------------------------------
 `Tellerwäscher <Detail>`__ bei `BISA <Detail>`__ (1)              `KAIVERS Karl (141) <Detail>`__   `EMONTS Daniel (128) <Detail>`__
====================================================== ========== ================================= ==================================
<BLANKLINE>
--------
Sonstige
--------
<BLANKLINE>
========================================================================== ======================================================= ===================================== =====================================
 Stelle                                                                     Arbeitet                                                Probezeit                             Kandidaten
-------------------------------------------------------------------------- ------------------------------------------------------- ------------------------------------- -------------------------------------
 `Kellner <Detail>`__ bei `R-Cycle Sperrgutsortierzentrum <Detail>`__ (1)   `RADERMACHER Christian (155) <Detail>`__ bis 02.01.15   `FAYMONVILLE Luc (130*) <Detail>`__   `JEANÉMART Jérôme (181) <Detail>`__
========================================================================== ======================================================= ===================================== =====================================
<BLANKLINE>



Printing this report caused a "NotImplementedError: <i> inside
<text:p>" traceback when one of the jobs had a remark.

>>> settings.SITE.default_build_method = "appyodt"
>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> rv = ses.run(obj.do_print)  #doctest: +ELLIPSIS
appy.pod render .../lino/modlib/printing/config/report/Default.odt -> .../media/webdav/userdocs/appyodt/jobs.JobsOverview.odt (language='de',params={'raiseOnError': True, 'ooPort': 8100, 'pythonWithUnoPath': ...}

>>> print(rv['success'])
True
>>> print(rv['open_url'])
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/.../jobs.JobsOverview.odt

This bug was fixed :blogref:`20130423`.
Note: the ``webdav/`` is only there when :attr:`lino.core.site.Site.use_java` is `True`.

