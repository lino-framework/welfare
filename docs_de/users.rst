================
Benutzer
================

Benutzerprofile
===============

Damit ein Benutzer sich anmelden kann, muss sein
:ddref:`users.User.profile` einen der folgenden Werte enthalten:

.. py2rst::

    from lino.api import rt
    rt.show('users.UserProfiles', stripped=False)
    

Technisches
===========

Technische Details unter :ref:`welfare.specs.users`.

.. Die Liste der Benutzerprofile ist definiert in
   :mod:`lino_welfare.modlib.welfare.roles` (außer wenn
   :attr:`user_profiles_module
   <lino.core.site.Site.user_profiles_module>` verändert wurde).
