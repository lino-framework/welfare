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
    in your Lino to see all application-specific userlevels.


