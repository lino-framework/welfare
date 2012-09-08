Installing Lino/Welfare
=======================

- First, install Lino as documented in `Installing Lino
  <http://packages.python.org/lino/admin/install.html>`_
  
- Download a copy of the Lino/Welfare repository to your snapshots 
  directory::

    cd /var/snapshots
    hg clone https://code.google.com/p/lino-welfare/
    
- Add `/var/snapshots/lino-welfare` to your Python path. 
  To test whether this worked, you can issue the command::
  
    python -m lino_welfare.settings
    
  

- In your project's `settings.py`, inherit from 
  `lino_welfare.settings` by replacing the following line::

    from lino.apps.pcsw.settings import *
    
  by this one::
    
    from lino_welfare.settings import *
    
    