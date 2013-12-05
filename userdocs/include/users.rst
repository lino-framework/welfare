..
  default userdocs for users module, used also by patrols,...

.. contents:: 
   :local:
   :depth: 2



.. actor:: users.User

.. actor:: users.User.profile

  The profile of a user is what defines her or his permissions.
 
  Users with an empty :ddref:`users.User.profile` 
  field are considered inactive and cannot log in.

.. actor:: users.Authority


.. actor:: users.Team

    A :ddref:`users.Team` is a group of users that work together. 
    
    Belonging to a :ddref:`users.Team` or not has no influence on 
    access permissions.
    These depend on your :ddref:`user profile <lino.UserProfiles>`.
    
.. actor:: users.Teams

    For illustration, the demo site has the following teams:

    .. django2rst:: settings.SITE.login().show(users.Teams)



.. actor:: users.Membership

    A membership is when a given :ddref:`users.User` 
    belongs to a given :ddref:`users.Team`.


.. actor:: lino.UserProfiles

    The list of user profiles available on this site. 
    
    Each user profile is a set of user levels 
    (one for each functional group), 
    leading to an individual combination of permissions.
    
    The demo database has defined the following user profiles:

    .. django2rst:: settings.SITE.login().show(lino.UserProfiles,
          column_names='value name text level')

    Note that we show here only the "general" or "system" userlevel.
    Open :menuselection:`Explorer --> System --> User Profiles`
    to see all application-specific userlevels.

