================
Les utilisateurs
================

Profils d'utilisateur
=====================

Pour qu'un utilisateur puisse se connecter, il faut que son
:attr:`user_type <lino.modlib.users.models.User.user_type>` aie une des
valeurs suivantes:

.. py2rst::

    from lino.api import rt
    rt.show('users.UserTypes', stripped=False)
    

Détails techniques
==================

La liste des profils utilisateurs disponible est définie dans
:mod:`lino_welfare.modlib.welfare.user_types` (sauf si
:attr:`user_types_module <lino.core.site.Site.user_types_module`
a été changé).


- Le profil 420 (Agent social (flexible)) :ticket:`2362` a les mêmes
  permissions que le profil 120 (Agent d'insertion flexible) mais
  reçoit moins de notifications. Notamment il voit également les
  onglets PARCOURS – COMPÉTENCES – FREINS - STAGES D’IMMERSION -
  MÉDIATION DE DETTES.

