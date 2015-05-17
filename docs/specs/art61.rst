.. _welfare.tested.art61:

==========================
Article 61 job supplyments
==========================

.. How to test only this document:

  $ python setup.py test -s tests.SpecsTests.test_art61

This document is an overview of the functionality provided by
:mod:`lino_welfare.modlib.art61`.

.. contents::
   :depth: 2
   :local:


A tested document
=================

This document is being tested using doctest with the following
initializations:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.chatelet.settings.doctests'
>>> from lino.api.doctest import *


What are article 61 job supplyments?
=====================================

A "job supplyment using article 61" (in French "mise au travail en
application de l'article 61") is a project where the PCSW cooperates
with a third-party employer in order to fulfill its duty of supplying
a job for a coached client. (`www.mi-is.be
<http://www.mi-is.be/be-fr/cpas/article-61>`__)

There are different formulas of subsidization:

.. py2rst::

    from lino.api import rt
    rt.show('art61.Subsidizations', language="fr")


Document templates
==================

.. xfile:: art61/Contract/contract.body.html

  This file is used as :attr:`body_template
  <lino.modlib.excerpts.models.Excerpt.body_template>` on the excerpt
  type used to print a
  :class:`lino_welfare.modlib.art61.models.Contract`.
  The default content is in 
  :srcref:`lino_welfare/modlib/art61/config/art61/Contract/contract.body.html`.



The printed document
====================

>>> obj = art61.Contract.objects.get(pk=1)
>>> list(obj.get_subsidizations())
[<Subsidizations.activa:10>]

>>> ar = rt.login('romain')
>>> html = obj.printed_by.preview(ar)
>>> soup = BeautifulSoup(html)
>>> for h in soup.find_all('h1'):
...     print(h)
<h1>Art61 job supplyment#1 (Robin DUBOIS)
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

