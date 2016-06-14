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

We retrieve Tx25 no. 1 from the database:


>>> obj = cbss.RetrieveTIGroupsRequest.objects.get(pk=1)
>>> obj
RetrieveTIGroupsRequest #1 ('Tx25-Anfrage #1')

So far this was standard Django API. To use Lino's extended API we 
first need to "log in" as user `rolf` 
using the :meth:`login <lino.core.site.Site.login>` method:


Here is the textual representation of the "Result" panel 
(only the first lines, this is just a test after all):

>>> ses = rt.login('hubert')
>>> with translation.override('de'):
...    ses.show(cbss.RetrieveTIGroupsResult.request(obj, limit=5))
====================== ===== ========== ==================================================
 Gruppe                 TI    Seit       Information
---------------------- ----- ---------- --------------------------------------------------
 NR-Nummer                    02.07.68   **68070201351** (Männlich)
 Wohnsitze              001   18.10.01   **Estland** (136), Fusion: **0**, Sprache: **2**
                              02.07.68   **Eupen** (63023), Fusion: **0**, Sprache: **2**
 Namen                  010   02.07.68   **Mustermann**, Max Moritz
 Legale Hauptadressen   020   30.07.97   **4700**, **Gülcherstrasse**, Nr. **21**
====================== ===== ========== ==================================================
<BLANKLINE>

>>> ses = rt.login('rolf')
>>> with translation.override('de'):
...    ses.show(cbss.RetrieveTIGroupsResult.request(obj, limit=5))
Confidential data


Printing a Tx25
-----------------


>>> rv = ses.run(obj.do_print)
>>> print(rv['success'])
True
>>> print(rv['open_url'])
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/.../cbss.RetrieveTIGroupsRequest-1.odt


Security aspects
================

Since the responses of many CBSS requests contain confidential data
about citizens, we have some rules for accessing this data.

- Only the user who initiated the request can see the results.
- Even the System Administrator cannot print nor see the detail of a
  CBSS request of other users.
- Only a *Security advisor* can see all data. Lino keeps a journal of
  every login as a security advisor.

