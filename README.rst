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
--------------------------

1. install the app from the root of the project directory::

    pip install --editable .

2. Instruct flask to use the right application::

    export FLASK_APP=guacamole

3. initialize the database with this command::

    flask initdb

4. now you can run guacamole::

    flask run --host 0.0.0.0

The application will greet you on http://localhost:5000/

Installation on Debian Wheezy
-----------------------------

For people installing on Debian Wheezy, you have to install avocado and its
dependencies. This is a shortcut to help people to install the right pieces::

    apt-get install pip python-dev liblzma-dev
    pip install pip --upgrade
    pip install -r requirements-avocado.txt
    pip install -r requirements.txt

With this you should be able to get the application up and running.

Using the REST API with curl
----------------------------

The add_jobs.sh script contains a testing routine for the application. Say you
want to create an environment::

    $ curl http://localhost:5000/environments/ -H "Content-Type:application/json" -d '{"hostname": "foo.bar.com", "operating_system": "CentOS"}' -X POST -v
    Note: Unnecessary use of -X or --request, POST is already inferred.
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > POST /environments/ HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.47.1
    > Accept: */*
    > Content-Type:application/json
    > Content-Length: 57
    >
    * upload completely sent off: 57 out of 57 bytes
    * HTTP 1.0, assume close after body
    < HTTP/1.0 201 CREATED
    < Content-Type: application/json
    < Content-Length: 88
    < Server: Werkzeug/0.11.11 Python/2.7.12
    < Date: Sun, 25 Sep 2016 10:10:47 GMT
    <
    {"current_job": null, "hostname": "foo.bar.com", "id": 5, "operating_system": "CentOS"}
    * Closing connection 0

You can then send a job::

    $ curl http://localhost:${PORT}/jobs/ -H "Content-Type:application/json" -d '{"requester": "lmr", "environment": 1, "test": "gdbtest.py"}' -X POST -v

The test gdb.py takes about 20 seconds, and is good to show that you can get the output of the avocado application in real time::

    $ curl http://localhost:5000/jobs/ -H "Content-Type:application/json" -d '{"requester": "lmr", "environment": 1, "test": "gdbtest.py"}' -X POST -v
    Note: Unnecessary use of -X or --request, POST is already inferred.
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > POST /jobs/ HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.47.1
    > Accept: */*
    > Content-Type:application/json
    > Content-Length: 60
    >
    * upload completely sent off: 60 out of 60 bytes
    * HTTP 1.0, assume close after body
    < HTTP/1.0 201 CREATED
    < Content-Type: application/json
    < Content-Length: 146
    < Server: Werkzeug/0.11.11 Python/2.7.12
    < Date: Sun, 25 Sep 2016 10:12:35 GMT
    <
    {"status": "SCHEDULED", "end": null, "environment": "1", "start": 1474798355.291173, "requester": "lmr", "duration": null, "output": "", "id": 4}

Checking out the status of the job 4::

    $ curl http://localhost:5000/jobs/4
    {"status": "PASS", "environment": "1", "duration": 25.741315126419067, "requester": "lmr", "test": "gdbtest.py", "output": "JOB ID     : ab33bc2f8523a2f63d1e33ca2ddacae80f461787\nJOB LOG    : /home/lmr/avocado/job-results/job-2016-09-25T07.12-ab33bc2/job.log\nTESTS      : 21\n (01/21) gdbtest.py:GdbTest.test_start_exit:  PASS (1.52 s)\n (02/21) gdbtest.py:GdbTest.test_existing_commands_raw:  PASS (0.33 s)\n (03/21) gdbtest.py:GdbTest.test_existing_commands:  PASS (0.42 s)\n (04/21) gdbtest.py:GdbTest.test_load_set_breakpoint_run_exit_raw:  PASS (0.33 s)\n (05/21) gdbtest.py:GdbTest.test_load_set_breakpoint_run_exit:  PASS (0.26 s)\n (06/21) gdbtest.py:GdbTest.test_generate_core:  PASS (0.23 s)\n (07/21) gdbtest.py:GdbTest.test_set_multiple_break:  PASS (0.23 s)\n (08/21) gdbtest.py:GdbTest.test_disconnect_raw:  PASS (4.76 s)\n (09/21) gdbtest.py:GdbTest.test_disconnect:  PASS (2.78 s)\n (10/21) gdbtest.py:GdbTest.test_remote_exec:  PASS (0.56 s)\n (11/21) gdbtest.py:GdbTest.test_stream_messages:  PASS (0.21 s)\n (12/21) gdbtest.py:GdbTest.test_connect_multiple_clients:  PASS (2.58 s)\n (13/21) gdbtest.py:GdbTest.test_server_exit:  PASS (0.40 s)\n (14/21) gdbtest.py:GdbTest.test_multiple_servers:  PASS (4.32 s)\n (15/21) gdbtest.py:GdbTest.test_interactive:  PASS (0.10 s)\n (16/21) gdbtest.py:GdbTest.test_interactive_args:  PASS (0.09 s)\n (17/21) gdbtest.py:GdbTest.test_exit_status:  PASS (0.10 s)\n (18/21) gdbtest.py:GdbTest.test_server_stderr:  PASS (0.35 s)\n (19/21) gdbtest.py:GdbTest.test_server_stdout:  PASS (1.53 s)\n (20/21) gdbtest.py:GdbTest.test_interactive_stdout:  PASS (0.10 s)\n (21/21) gdbtest.py:GdbTest.test_remote:  PASS (1.40 s)\nRESULTS    : PASS 21 | ERROR 0 | FAIL 0 | SKIP 0 | WARN 0 | INTERRUPT 0\nTESTS TIME : 22.58 s\nJOB HTML   : /home/lmr/avocado/job-results/job-2016-09-25T07.12-ab33bc2/html/results.html\n", "id": 4}

Using the web application
-------------------------

The web application has 3 tabs:

* Jobs: Shows a list of jobs, and allows you to create a new job
* Environments: Shows a list of environments, and allows you to create a new environment
* View Job: Shows the details of a job. It queries the job live so you can see the job output unfolding

    .. image:: https://cloud.githubusercontent.com/assets/296807/18814647/84252940-82f0-11e6-804a-5773a2cc0d65.png
        :alt: Jobs
        :width: 100%
        :align: center

    .. image:: https://cloud.githubusercontent.com/assets/296807/18814648/8429119a-82f0-11e6-8865-4864af7f0af8.png
        :alt: Environments
        :width: 100%
        :align: center

    .. image:: https://cloud.githubusercontent.com/assets/296807/18814649/8429dc24-82f0-11e6-855e-fa45cee4fa8f.png
        :alt: Job View
        :width: 100%
        :align: center

[1] http://flask.pocoo.org/

[2] http://flask-restful-cn.readthedocs.io/
