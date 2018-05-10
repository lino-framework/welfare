.. _welfare.install:

=======================
Installing Lino Welfare
=======================

Here are a few methods for installing and running a development
version of Lino Welfare in order to evaluate the product and make
demonstrations using the built-in demo databases.

From inside a code repository
=============================

- Install Lino (the framework) as documented in `Installing Lino
  <http://lino-framework.org/dev/install.html>`__.

- Lino Welfare requires some additional system packages (Tidy,
  LibreOffice and UNO)::

    $ sudo apt-get install -y tidy libreoffice python3-uno

  And LO must be running as a server::
    
    $ libreoffice '--accept=socket,host=127.0.0.1,port=8100;urp;' &

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

- Initialize your demo databases as follows::

      $ cd ~/repositories/welfare
      $ inv prep

- Run the web server::

    $ cd ~/repositories/welfare/lino_welfare/projects/eupen
    $ python manage.py runserver

- You might want to replace "eupen" by "chatelet" in above command
  (:ref:`eupen <welfare.specs.eupen>` and :ref:`chatelet
  <welfare.specs.chatelet>` are the two main variants of Lino
  Welfare).
  

Shell scripts for running the server
====================================

In order to automate things, let's now write two shell scripts, one
for every demo site. Create a file :file:`~/eupen.sh` with this
content::
  
    #!/bin/bash
    set -e  # exit on error
    . /home/johndoe/virtualenvs/a/bin/activate
    exec django-admin.py --settings=lino_welfare.projects.eupen.settings.demo runserver 8080

Make it executable::

  $ chmod +x eupen.sh

Do the same for chatelet and any other demo site.  


Installing demo web servers automatically at system startup
===========================================================

On a demo machine you might want to run your sites as a service. We
recommend using `supervisor <http://supervisord.org/>`_ for this::

    $ sudo apt-get install supervisor

Then write a supervisor script
:file:`/etc/supervisor/conf.d/eupen.conf` with this content::
          
      [program:eupen]
      command = /home/johndoe/eupen.sh
      user = johndoe
      umask = 0007

and a similar script for or any other sites.

To activate them, you must restart supervisor::

  $ sudo service supervisor restart

  

Using local projects
====================

You may want to maintain a set of your own configuration contexts.

- Do as above

- Create your project directory containing a :xfile:`settings.py`
  file:

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


    
