Guacamole REST API and Web Client for the avocado test runner
=============================================================

Guacamole is a REST API for controlling the avocado test
runner, and also a single page web javascript client to
that rest API. With the web application, you can create
test environments, create test jobs, and also see details
of a particular test job.

Dependencies
------------

Guacamole is a Flask [1] application that uses the Flask-RESTful extension [2]
to provide convenience APIs to build a REST API using Flask. It also persists
to disk using sqlite, using Flask-SQLAlchemy.

For the test runner, you have to install the avocado test framework. There are
packages readily available for Fedora and CentOS, but for Debian and Ubuntu you
might need to install straight from pip::

    * pip install -r requirements-avocado.txt
    * pip install -r requirements.txt

How to run the application
==========================

1. install the app from the root of the project directory::

    pip install --editable .

2. Instruct flask to use the right application::

    export FLASK_APP=guacamole

3. initialize the database with this command::

    flask initdb

4. now you can run guacamole::

    flask run

The application will greet you on http://localhost:5000/

[1] http://flask.pocoo.org/
[2] http://flask-restful-cn.readthedocs.io/