pyDash - v1.4.4
===============

A reusable django app for monitoring your linux server.

Supported Python versions:

-  Python 2.x

Requirements:

-  Django >= 1.5

Installation
============

Clone the repository to your pc and, assuming that ``pip`` is installed,
run the following commands:

-  ``python setup.py sdist``
-  ``pip install dist/django-pydash-app-*.tar.gz``

Make sure that ``django.contrib.auth`` is installed and working.

Open your project’s ``settings.py`` and add ``pydash`` to
``INSTALLED_APPS``:

::

    INSTALLED_APPS = (
        'pydash',
    )

Open your project’s ``urls.py`` and include the ``pydash`` urls.

::

    urlpatterns = patterns('',
        (r'^pydash/', include('pydash.urls')),
    )

Make sure ``AppDirectoriesFinder`` is enabled in your
``STATICFILES_FINDERS``:

::

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

Before deploying to a live server, run the following command in order to
collect the static files stored in pydash’s directory:

::

    $ python manage.py collectstatic

Settings
========

There are 3 different refresh settings which are measured in
``miliseconds``:

::

     TIME_JS_REFRESH = 30000 #30 seconds
     TIME_JS_REFRESH_LONG = 120000 #120 seconds
     TIME_JS_REFRESH_NET = 2000 #2 seconds

If you wish to override the default settings, simply set those fields
with the new values in your application’s ``settings.py`` file.

The refresh settings for each table are as follows:

::

    Memory Usage - TIME_JS_REFRESH
    Load Average - TIME_JS_REFRESH
    CPU Usage - TIME_JS_REFRESH
    Traffic Usage - TIME_JS_REFRESH_NET
    Disk Reads/Writes - TIME_JS_REFRESH_NET
    Uptime - TIME_JS_REFRESH_LONG
    Disk Usage - TIME_JS_REFRESH_LONG
    Online Users - TIME_JS_REFRESH_LONG
    Processes - TIME_JS_REFRESH_LONG
    Netstat - TIME_JS_REFRESH_LONG

Remote data retrieval
=====================

pyDash allows you to retrieve data remotely.

Data is returned in JSON and can be easily retrieved as long as the user
agent has been authenticated by the web application.

pyDash has a list of short URLs which you can use to retrieve the
specific data:

::

    /info/uptime/ - Uptime
    /info/platform/hostname/ - Hostname
    /info/platform/osname/ - OS Name
    /info/platform/kernel/ - Kernel
    /info/getcpus/cpucount/ - Number of CPU cores
    /info/getcpu

Issues
======

Report any issues/bugs at `https://github.com/k3oni/pydash-django-app <https://github.com/k3oni/pydash-django-app>`_
