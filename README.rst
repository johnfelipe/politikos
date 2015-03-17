Politikós
=========

Development
-----------

.. code:: bash

    $ mkvirtualenv politikos
    $ git clone git@github.com:openpolis/politikos.git
    $ cd politikos
    $ cp config/samples.env config/.env
    $ vi config/.env
    $ pip install -r requirements.txt
    $ python project/manage.py syncdb
    $ python project/manage.py runserver

Settings
--------

* DEBUG (on|off)
* SECRET_KEY (random string)
* ALLOWED_HOSTS (comma separated values)
* MAPIT_ENDPOINT (default http://mapit.openpolis.it/)
* POPIT_INSTANCE (default parlamento)
