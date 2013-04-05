.. _welfare.users:

========================
Gestion des utilisateurs
========================


Référence
=========

.. actor:: users.Users
.. actor:: users.Teams
.. actor:: users.Memberships


.. _welfare.users.User.profile:

The profile of a user
---------------------

Each user must have a profile in order to be active. 
Users with an empty :ref:`welfare.users.User.profile` 
field are considered inactive and cannot log in.



Team
====

The permissions do not depend on the Team, 
they depend on the :ref:`welfare.users.UserProfile`.
Belonging to a user group or not has no influence on access permissions


Teams
=============


The table of available :ref:`welfare.users.Team` records on this site.

The demo site has the following teams:

.. py2rst:: settings.SITE.login('rolf').show(users.Teams)



Membership
=============


A membership is when a given :ref:`welfare.users.User` 
belongs to a given :ref:`welfare.users.Team`.



.. _welfare.users.UserProfile:

User Profile
=============

A user profile is a combination of access rights and permission sets. 



.. actor:: lino.UserProfiles


User Profiles
=============

The list of user profiles available on this site. 

In the demo database, alice and hubert share the same profile 
while melanie has a different profile.

.. py2rst:: settings.SITE.login('rolf').show(lino.UserProfiles)




Référence
=========


.. actor:: ui.ContentTypes
