================
Benutzer
================

Benutzerprofile
===============

Damit ein Benutzer sich anmelden kann, muss sein
:ddref:`auth.User.user_type` einen der folgenden Werte enthalten:

.. py2rst::

    from lino.api import rt
    rt.show('auth.UserTypes', stripped=False)
    

Technisches
===========

Technische Details unter :ref:`welfare.specs.users`.

.. Die Liste der Benutzerprofile ist definiert in
   :mod:`lino_welfare.modlib.welfare.roles` (außer wenn
   :attr:`user_types_module
   <lino.core.site.Site.user_types_module>` verändert wurde).
