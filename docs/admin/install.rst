.. _welfare.install:

Installing Lino Welfare
=======================

Development server
------------------

If you need only a development server, 
just install Lino (the framework) as documented 
in :ref:`lino.dev.install`, then:

- Go to your `repositories` directory and 
  download also a copy of the Lino Welfare repository::

    $ cd ~/repositories
    $ git clone https://github.com/lsaffre/lino-welfare.git welfare

- Use pip to install `welfare` as editable package::

    pip install -e welfare

- Lino Welfare needs two Java applets :ref:`davlink` and
  :ref:`eidreader` which are also available from GitHub. Simply clone
  them::

    $ git clone https://github.com/lsaffre/davlink.git
    $ git clone https://github.com/lsaffre/eidreader.git

- Create your project directory and a :xfile:`settings.py` file:

    $ mkdir ~/mysite
    $ cd ~/mysite
    $ nano settings.py

  Paste the following content into your :xfile:`settings.py` file:
    
  .. includeliteral:: settings.py

- Create a :xfile:`media` directory and create symbolic links to your
  local copies of :ref:`davlink` and :ref:`eidreader`::


    $ cd ~/mysite
    $ mkdir media
    $ ln -s ~/repositories/davlink/examples media/davlink
    $ ln -s ~/repositories/eidreader/examples media/eidreader

- Create a :xfile:`manage.py` file in your project directory::

    $ cd ~/mysite
    $ nano settings.py

  Paste the following content into your :xfile:`manage.py` file:
    
  .. includeliteral:: manage.py

- Initialize the database and run the development server::

    $ python manage.py initdb_demo
    $ python manage.py runserver
