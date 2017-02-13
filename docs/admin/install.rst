.. _welfare.install:

Installing Lino Welfare
=======================

Here are a few methods for installing and running a development
version of Lino Welfare in order to evaluate the product and make
demonstrations using the built-in demo databases.

From inside a code repository
=============================

- Install Lino (the framework) as documented in
  :ref:`lino.dev.install`.

- Go to your :xfile:`~/repositories` directory and clone some more
  repositories::

    $ cd ~/repositories
    $ git clone https://github.com/lino-framework/xl.git xl
    $ git clone https://github.com/lsaffre/lino-cosi.git cosi
    $ git clone https://github.com/lsaffre/lino-welfare.git welfare

- Use pip to install them (note that the ordering is important here)::

    pip install -e xl
    pip install -e cosi
    pip install -e welfare

- Initialize your demo databases as follows:

      $ cd ~/repositories/welfare
      $ inv prep

- How to run demo server::

    $ cd ~/repositories/welfare/lino_welfare/projects/eupen
    $ python manage.py runserver

  Alternatively you can do the same using a single command::

    $ django-admin.py runserver --settings=lino_welfare.projects.eupen.settings.demo

  You might want to replace "eupen" by "chatelet" in above commands
  ("eupen" and "chatelet" are the two main variants of Lino Welfare)

  

Using local projects
====================

You may want to maintain a set of your own configuration contexts.

- Do as above

- Create your project directory and a :xfile:`settings.py` file:

    $ mkdir ~/mysite
    $ cd ~/mysite
    $ nano settings.py

  Paste the following content into your :xfile:`settings.py` file:
    
  .. literalinclude:: settings.py

- Create a :xfile:`manage.py` file in your project directory::

    $ cd ~/mysite
    $ nano settings.py

  Paste the following content into your :xfile:`manage.py` file:
    
  .. literalinclude:: manage.py

- Initialize the database and run the development server::

    $ python manage.py prep
    $ python manage.py runserver


Java applets
============

- Certain functionalities require two Java applets :ref:`davlink` and
  :ref:`eidreader` which are also available from GitHub. Simply clone
  them::

    $ git clone https://github.com/lsaffre/davlink.git
    $ git clone https://github.com/lsaffre/eidreader.git


    
