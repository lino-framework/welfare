================
Les utilisateurs
================


.. py2rst::

    #import lino
    #lino.startup('lino_welfare.projects.chatelet.demo.settings')
    from lino.api import rt
    rt.show('users.UserProfiles', header_level=2, stripped=False)
