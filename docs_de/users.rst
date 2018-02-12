================
Benutzer
================

Benutzerarten
===============

Damit ein Benutzer sich anmelden kann, muss das Feld
:ddref:`users.User.user_type` ausgefüllt sein.  Es gibt folgende
Benutzerarten:

.. lino2rst::

    rt.show(users.UserTypes, column_names="value text remark", stripped=False)
    
    

Technisches
===========

Technische Details unter :ref:`welfare.specs.users`.

.. Die Liste der Benutzerprofile ist definiert in
   :mod:`lino_welfare.modlib.welfare.roles` (außer wenn
   :attr:`user_types_module
   <lino.core.site.Site.user_types_module>` verändert wurde).

