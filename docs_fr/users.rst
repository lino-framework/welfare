================
Les utilisateurs
================

Profils d'utilisateur
=====================

Pour qu'un utilisateur puisse se connecter, il faut que son
:attr:`profile <lino.modlib.users.models.User.profile>` aie une des
valeurs suivantes:

.. py2rst::

    from lino.api import rt
    rt.show('users.UserTypes', stripped=False)
    

Détails techniques
==================

La liste des profils utilisateurs disponible est définie dans
:mod:`lino_welfare.modlib.welfare.roles` (sauf si
:attr:`user_types_module <lino.core.site.Site.user_types_module`
a été changé).
