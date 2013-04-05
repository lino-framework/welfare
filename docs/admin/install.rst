.. _welfare.install:

Installing Lino-Welfare
=======================

Development server
------------------

If you need only a development server, 
just install Lino (the framework) as documented 
in :ref:`lino.dev.install`, then:

- Go to your `hgwork` directory and 
  download also a copy of the Lino-Welfare repository::

    cd ~/hgwork
    hg clone https://code.google.com/p/lino-welfare/ welfare
    
- Use pip to install this as editable package::

    pip install -e welfare

- In your project's `settings.py`, make sure that you inherit from 
  the right `settings` module::
    
    from lino_welfare.settings import *


