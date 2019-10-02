.. doctest docs/specs/cbss.rst
.. _cbss:
.. _welfare.specs.cbss:

================================
CBSS connection for Lino Welfare
================================

.. doctest init:

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from etgen.html import E
>>> from lino.api.doctest import *

The :mod:`lino_welfare.modlib.cbss` plugin adds functionality for
communicating with the *CBSS*.

.. currentmodule:: lino_welfare.modlib.cbss


The **CBSS** (Crossroads Bank for Social Security, French *Banque
Carrefour de la Sécurité Sociale*) is an information system for data
exchange between different Belgian government agencies.  `Official
website <http://www.ksz-bcss.fgov.be>`__

Lino currently knows the following CBSS services:

- :class:`IdentifyPersonRequest` : Identifier la personne par son NISS
  ou ses données phonétiques et vérifier son identité par le numéro de
  carte SIS, de carte d'identité ou par ses données phonétiques.

- :class:`ManageAccessRequest`: Enregistrer, désenregistrer ou
  consulter un dossier dans le registre du réseau de la sécurité
  sociale (registre BCSS) et dans le répertoire sectoriel des CPAS
  géré par la SmalS-MvM.

- :class:`RetrieveTIGroupsRequest`: Obtenir des informations à propos
  d’une personne dans le cadre de l’enquête sociale.
  See :ref:`tx25`.

Only the last one is being used on a regular base.


Configuration
=============

When this plugin is installed, the local system administrator must
configure certain settings.

The following *plugin attributes* can be set in your :meth:`get_plugin_configs
<lino.core.site.Site.get_plugin_configs>`:

>>> dd.plugins.cbss.cbss_live_requests
False

>>> dd.plugins.cbss.cbss_environment
'test'

And your :class:`SiteConfig <lino.modlib.system.SiteConfig>` has the following
additional fields:

>>> show_fields(rt.models.system.SiteConfig,
... "sector cbss_org_unit ssdn_user_id cbss_http_password")
+--------------------+-------------------------+----------------------------------------------------------------------------------------+
| Internal name      | Verbose name            | Help text                                                                              |
+====================+=========================+========================================================================================+
| sector             | sector                  | The CBSS sector/subsector of the requesting organization.                              |
|                    |                         | For PCSWs this is always 17.1.                                                         |
|                    |                         | Used in SSDN requests as text of the `MatrixID` and `MatrixSubID`                      |
|                    |                         | elements of `AuthorizedUser`.                                                          |
|                    |                         | Used in ManageAccess requests as default value                                         |
|                    |                         | for the non-editable field `sector`                                                    |
|                    |                         | (which defines the choices of the `purpose` field).                                    |
+--------------------+-------------------------+----------------------------------------------------------------------------------------+
| cbss_org_unit      | Anfragende Organisation | In CBSS requests, identifies the requesting organization.                              |
|                    |                         | For PCSWs this is the enterprise number                                                |
|                    |                         | (CBE, KBO) and should have 10 digits and no formatting characters.                     |
|                    |                         |                                                                                        |
|                    |                         | Used in SSDN requests as text of the `AuthorizedUser\OrgUnit` element .                |
|                    |                         | Used in new style requests as text of the `CustomerIdentification\cbeNumber` element . |
+--------------------+-------------------------+----------------------------------------------------------------------------------------+
| ssdn_user_id       | SSDN User Id            | Used in SSDN requests as text of the `AuthorizedUser\UserID` element.                  |
+--------------------+-------------------------+----------------------------------------------------------------------------------------+
| cbss_http_password | HTTP password           | Used in the http header of new-style requests.                                         |
+--------------------+-------------------------+----------------------------------------------------------------------------------------+


Permissions
===========

>>> ContentType = rt.models.contenttypes.ContentType
>>> RetrieveTIGroupsRequest = rt.models.cbss.RetrieveTIGroupsRequest
>>> kw = dict(fmt='json', limit=10, start=0)
>>> json_fields = 'count rows title success no_data_text'

>>> mt = ContentType.objects.get_for_model(RetrieveTIGroupsRequest).pk
>>> print(RetrieveTIGroupsRequest.objects.get(pk=1).user.username)
hubert
>>> demo_get('rolf', 'api/cbss/RetrieveTIGroupsResult',
...     json_fields, 0, mt=mt, mk=1, **kw)
>>> demo_get('hubert', 'api/cbss/RetrieveTIGroupsResult',
...     json_fields, 18, mt=mt, mk=1, **kw)
>>> demo_get('patrick', 'api/cbss/RetrieveTIGroupsResult',
...     json_fields, 18, mt=mt, mk=1, **kw)



Models
======

.. class:: Sector

    Default values filled from
    :mod:`lino_welfare.modlib.cbss.fixtures.sectors`.

.. class:: Purpose

    Codes qualité (Hoedanigheidscodes).
    This table is usually filled with the official codes
    by :mod:`lino_welfare.modlib.cbss.fixtures.purposes`.


.. class:: IdentifyPersonRequest

    A request to the IdentifyPerson service.

.. class:: ManageAccessRequest

    A request to the ManageAccess service.

    Registering a person means that this PCSW is going to maintain a
    dossier about this person.  Users commonly say "to integrate" a
    person.

    Fields include:


    .. attribute:: sector

        Pointer to :class:`Sector`.

    .. attribute:: purpose

        Pointer to :class:`Purpose`.

    .. attribute:: action

        The action to perform.  This must be one of the values in
        :class:`lino_welfare.modlib.cbss.choicelists.ManageActions`

    .. attribute:: query_register

        The register to be query.
        This must be one of the values in
        :class:`lino_welfare.modlib.cbss.choicelists.QueryRegisters`


.. class:: RetrieveTIGroupsRequest

    A request to the RetrieveTIGroups service (aka Tx25)
