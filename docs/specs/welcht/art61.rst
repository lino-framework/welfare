.. doctest docs/specs/welcht/art61.rst
.. _welfare.specs.art61:

======================================
``art61`` : Article 61 job supplyments
======================================

The :mod:`lino_welfare.modlib.art61` plugin adds support for managing Article
61 job supplyments.

.. currentmodule:: lino_welfare.modlib.art61

.. contents::
   :depth: 2
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.mathieu.settings.doctests')
>>> from lino.api.doctest import *



What are article 61 job supplyments?
=====================================

A "job supplyment using article 61" (in French "mise au travail en
application de l'article 61") is a project where the PCSW cooperates
with a third-party employer in order to fulfill its duty of supplying
a job for a coached client. (`www.mi-is.be
<http://www.mi-is.be/be-fr/cpas/article-61>`__)

There are different formulas of subsidization:

>>> rt.show('art61.Subsidizations', language="fr")
======= ========= =================
 value   name      text
------- --------- -----------------
 10      activa    Activa
 20      tutorat   Tutorat
 30      region    Région Wallonne
 40      sine      SINE
 50      ptp       PTP
======= ========= =================
<BLANKLINE>


Document templates
==================

.. xfile:: art61/Contract/contract.body.html

  This file is used as :attr:`body_template
  <lino.modlib.excerpts.models.Excerpt.body_template>` on the excerpt
  type used to print a
  :class:`lino_welfare.modlib.art61.models.Contract`.
  The default content is in
  `lino_welfare/modlib/art61/config/art61/Contract/contract.body.html <https://github.com/lino-framework/welfare/blob/master/lino_welfare/modlib/art61/config/art61/Contract/contract.body.html>`__.



The printed document
====================

>>> obj = art61.Contract.objects.get(pk=1)
>>> list(obj.get_subsidizations())
[<art61.Subsidizations.activa:10>]

>>> ar = rt.login('romain')
>>> html = ar.get_data_value(obj.printed_by, 'preview')
>>> soup = BeautifulSoup(html, 'lxml')
>>> for h in soup.find_all('h1'):
...     print(str(h))
<h1>Mise à l'emploi art.61
</h1>

>>> for h in soup.find_all('h2'):
...     print(h)
<h2>Article 1</h2>
<h2>Article 2</h2>
<h2>Article 3</h2>
<h2>Article 4 (sans tutorat)</h2>
<h2>Article 5 (activa)</h2>
<h2>Article 6 (activa)</h2>
<h2>Article 7 (sans tutorat)</h2>
<h2>Article 8</h2>
<h2>Article 9</h2>
<h2>Article 10</h2>
<h2>Article 11</h2>
<h2>Article 12</h2>
<h2>Article 13</h2>
<h2>Article 14</h2>



Art61 job supplyments
=====================

An "Art61 job supplyment" is an agreement between the PCSW and a
private company about one of the clients of the PCSW.

.. class:: Contract

    The Django database model.

    .. method:: get_subsidizations(self)

        Yield a list of all subsidizations activated for this
        contract.


.. class:: ContractsByClient

    Shows the *Art61 job supplyments* for this client.


.. class:: ContractType

This is the homologue of :class:`isip.ContractType
<lino_welfare.modlib.isip.ContractType>` (see there for
general documentation).

The demo database comes with these contract types:

>>> rt.show('art61.ContractTypes')
======================== =================== ====================== ===========
 Désignation              Désignation (de)    Désignation (en)       Référence
------------------------ ------------------- ---------------------- -----------
 Mise à l'emploi art.61   Art.61-Konvention   Art61 job supplyment
======================== =================== ====================== ===========
<BLANKLINE>
