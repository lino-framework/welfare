Installing Lino-Welfare
=======================

- First, install Lino (the tramework) as documented 
  in `Installing Lino <http://lino-framework.org/admin/install.html>`_
  
- Go to your snapshots directory::

    cd ~/snapshots
    
- To **install a released version**, consult :doc:`/releases` 
  to see which is the latest version, then download it using something 
  like::
  
    wget http://pypi.python.org/packages/source/l/lino-welfare/lino-welfare-1.0.tar.gz
    tar -xvzf lino-welfare-1.0.tar.gz
  
- To **install a development version**, 
  download a copy of the Lino/Welfare repository to your snapshots 
  directory::

    hg clone https://code.google.com/p/lino-welfare/ lino-welfare-dev
    
- Add `~/snapshots/lino-welfare-dev` or `~/snapshots/lino-welfare-1.0`
  to your `Python path <http://lino-framework.org/admin/pythonpath.html>`_. 
  To test whether this worked, you can issue the command::
  
    python -m lino_welfare.modlib.pcsw.settings
    
- In your project's `settings.py`, make sure that you inherit from 
  the right `settings` module::
    
    from lino_welfare.modlib.pcsw.settings import *
    
