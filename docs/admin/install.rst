Installing Lino-Welfare
=======================

- First, install Lino (the tramework) as documented 
  in `Quick Start <http://lino-framework.org/tutorials/quickstart.html>`_
  
- Go to your `hgwork` directory and 
  download a copy of the Lino/Welfare repository::

    cd ~/hgwork
    hg clone https://code.google.com/p/lino-welfare/ lino-welfare-dev
    
- Use pip to install this as editable package::

    pip install -e .

- To test whether this worked, you can issue the command::
  
    python -m lino_welfare.modlib.pcsw.settings
    
- In your project's `settings.py`, make sure that you inherit from 
  the right `settings` module::
    
    from lino_welfare.modlib.pcsw.settings import *
    
