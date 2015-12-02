================
Benutzer
================

Benutzerprofile
===============

Damit ein Benutzer sich anmelden kann, muss sein :attr:`profile
<lino.modlib.users.models.User.profile>` einen der folgenden Werte
enthalten:

.. py2rst::

    from lino.api import rt
    rt.show('users.UserProfiles', stripped=False)
    
