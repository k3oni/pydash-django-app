pyDash - v1.4.4  [![Follow @hostechs](https://dev.twitter.com/sites/default/files/images_documentation/bird_blue_32.png)](https://twitter.com/hostechs)    [![View Profile](https://dlc1-s.licdn.com/sites/default/files/InBug-30px-R.png)](http://www.linkedin.com/in/hostechs/)
======


[![Flattr this](http://api.flattr.com/button/flattr-badge-large.png)](http://flattr.com/thing/2630601/k3onipydash-on-GitHub "Flattr this")


A reusable django app for monitoring your linux server.


Supported Python versions:

  - Python 2.x

__[View Demo](http://pydash.hostechs.com/)__

     user: admin
     pass: admin


![pyDash](https://www.yaktab.com/en/2btxew)


Installation
============

Clone the repository to your pc and, assuming that ``pip`` is installed, run the
following commands:

* `` python setup.py sdist ``
* `` pip install dist/django-pydash-app-*.tar.gz ``

Make sure that ``django.contrib.auth`` is installed and working.

Open your project's ``settings.py`` and add ``pydash`` to ``INSTALLED_APPS``:

    INSTALLED_APPS = (
        'pydash',
    )

Open your project's ``urls.py`` and include the ``pydash`` urls.

    urlpatterns = patterns('',
        (r'^pydash/', include('pydash.urls')),
    )

Make sure ``AppDirectoriesFinder`` is enabled in your ``STATICFILES_FINDERS``:

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

Before deploying to a live server, run the following command in order to collect the static files stored in pydash's directory:

    $ python manage.py collectstatic


Settings
========

There are 3 different refresh settings which are measured in `miliseconds`:

     TIME_JS_REFRESH = 30000 #30 seconds
     TIME_JS_REFRESH_LONG = 120000 #120 seconds
     TIME_JS_REFRESH_NET = 2000 #2 seconds

If you wish to override the default settings, simply set those fields with the new values in your application's ``settings.py`` file.

The refresh settings for each table are as follows:

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

Data is returned in JSON and can be easily retrieved as long as the user agent has been authenticated by the web application. For more information about how sessions are managed in Django, please click [here](https://docs.djangoproject.com/en/1.6/topics/http/sessions/).

pyDash has a list of short URLs which you can use to retrieve the specific data:

    /info/uptime/ - Uptime
    /info/platform/hostname/ - Hostname
    /info/platform/osname/ - OS Name
    /info/platform/kernel/ - Kernel
    /info/getcpus/cpucount/ - Number of CPU cores
    /info/getcpus/cputype/ - Type/Name of CPU
    /info/memory/ - Memory Usage
    /info/cpuusage/ - CPU Usage in percentage(%), free and used
    /info/getdisk/ - Disk Usage
    /info/getusers/ - Online Users
    /info/getips/ - IP Addresses
    /info/gettraffic/ - Internet Traffic
    /info/getdiskio/ - Disk Reads/Writes
    /info/proc/ - Running Processes
    /info/loadaverage/ - Load Average
    /info/getnetstat/ - Netstat

To see the format of the JSON returned, you can access any of the URLs from your browser, e.g. `http://demo.pydash.net/info/uptime/` .


OS Support
==========

pyDash was tested and runs under the following OSes:

  - Centos
  - Fedora
  - Ubuntu
  - Debian
  - Raspbian
  - Pidora
  - Arch Linux


It might work under others, but it hasn't been tested yet.



License
=======

**[MIT](https://github.com/k3oni/pydash-django-app/blob/master/LICENSE.md)**



Credits
=======
[Dashboard Template](http://www.egrappler.com/templatevamp-free-twitter-bootstrap-admin-template/),
[Bootstrap](http://getbootstrap.com/),
[Font Awesome](http://fontawesome.io/)
