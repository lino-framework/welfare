.. _welfare.users:

=====
Users
=====

.. actor:: users.User


.. actor:: users.Team

    A :ddref:`users.Team` is a group of users that work together more tightly than 
    others. The demo site has the following teams:

    .. django2rst:: settings.SITE.login('rolf').show(users.Teams)

    The permissions do not depend on the Team, 
    they depend on the :ddref:`profile <lino.UserProfiles>`.
    Belonging to a :ddref:`users.Team` or not has no influence on access permissions



.. actor:: users.Membership

    A membership is when a given :ddref:`users.User` 
    belongs to a given :ddref:`users.Team`.




.. actor:: lino.UserProfiles

    The list of user profiles available on this site. 
    Each user profile is a combination of access rights and permission sets. 

    In the demo database, alice and hubert share the same profile 
    while melanie has a different profile.

    .. django2rst:: settings.SITE.login('rolf').show(lino.UserProfiles)


