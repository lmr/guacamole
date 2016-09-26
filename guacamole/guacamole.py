# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2016 Lucas Meneghel Rodrigues
# Lucas Meneghel Rodrigues <lookkas@gmail.com>

"""
Guacamole rest API and web client for avocado.
"""
from flask import Flask, render_template
from flask_restful import Api

from . import database
from . import environment
from . import job
from . import version

app = Flask(__name__)
api = Api(app)


@app.cli.command('initdb')
def initdb_command():
    """
    Creates the database tables.
    """
    database.init_db()
    print('Initialized the database.')


@app.route('/')
def index():
    """
    Application root (web interface).
    """
    return render_template('index.html')


api.add_resource(version.Version, '/version/')
api.add_resource(environment.EnvironmentList, '/environments/')
api.add_resource(environment.Environment, '/environments/<env_id>')
api.add_resource(job.JobList, '/jobs/')
api.add_resource(job.Job, '/jobs/<job_id>')


if __name__ == '__main__':
    app.run(debug=True, port=5040)
