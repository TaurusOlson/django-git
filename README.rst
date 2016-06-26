==========
django-git
==========

**django-git** is a simple Django app to:

- show all the Git projects stored in a local directory
- give a detail view of each project (dashboard)
  * number of commits 
  * number of days since the last commit 
  * number of hours spent on the project 
  * when the commits were made 


---------------

* `Installation`_
* `Quick start`_
* `Contribute`_
* `Tests`_
* `License`_

---------------


Installation
------------

Requirements:

* Python 3
* Django 1.9
* pygit2 
* pygal
* pytz

Install with pip::

    pip install django-git


Quick start
-----------

1. In settings.py, add 'git' to your INSTALLED_APPS like this::

    INSTALLED_APPS = [
        ...
        'git',
    ]

2. and specify the path to your Git repositories::

    PROJECTS_DIR = "path/to/git_repositories"

If necessary, set your database configuration. For example, for PostgreSQL::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '<dbname>',
            'USER': '<username>',
            'HOST': '<host>'
        }
    }

3. In urls.py, include the git URLconf in your project this::

    from django.conf.urls import url, include

    urlpatterns = [
        ...
        url(r'^git/', include('git.urls')),
    ]

3. Run the following command to create the git models::
   
   python manage.py migrate 
   
4. Update the Git projects::

   python manage.py updategitprojects

4. Start the development server::

   python manage.py runservser
   
and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/git to see your Git projects


Tests
-----

Run the tests with::

    python runtests.py


Contribute
----------

The project is still in its early stage. There are probably many aspects to
improve and bugs to fix.
Feel free to send pull requests.


License
-------

MIT. See LICENSE for more details.
