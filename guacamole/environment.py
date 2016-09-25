"""
Environment resource entry point for Guacamole.
"""
from flask_restful import abort, reqparse, Resource

from .database import db_session
from .models import Environment as EnvironmentTable


def get_env_parser():
    """
    Parse parameters passed to the HTTP request at the /environments resource.

    :return: Base dict structure holding parameters passed to a request.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('hostname')
    parser.add_argument('operating_system')
    return parser


def serialize_env_table_entry(entry):
    """
    Serialize a SQLAlchemy env model into a python dictionary.

    :param entry: SQLAlchemy model instance.
    :return: Dict with environment table data.
    """
    return {'id': entry.id,
            'hostname': entry.hostname,
            'operating_system': entry.operating_system,
            'current_job': entry.current_job}


class Environment(Resource):
    """
    Shows a single environment and lets you delete an environment.
    """

    @staticmethod
    def abort_if_doesnt_exist(env_id, env):
        if not env:
            abort(404, message="Environment {} doesn't exist".format(env_id))

    def get(self, env_id):
        env_entry = EnvironmentTable.query.filter_by(id=env_id)
        self.abort_if_doesnt_exist(env_id, env_entry.first())
        return serialize_env_table_entry(env_entry)

    def delete(self, env_id):
        env_entry = EnvironmentTable.query.filter_by(id=env_id)
        self.abort_if_doesnt_exist(env_id, env_entry.first())
        env_entry.delete()
        db_session.commit()
        return '', 204


class EnvironmentList(Resource):
    """
    Shows a list of your environments and lets you POST to add new environments.
    """

    def get(self):
        """
        Get all Environments.

        :return: Dict with results and count of results.
        """
        results = [serialize_env_table_entry(entry) for
                   entry in EnvironmentTable.query.all()]
        return {"results": results, "count": len(results)}

    def post(self):
        """
        Create an Environment.

        :return: Dict with newly created job info and HTTP 201.
        """
        parser = get_env_parser()
        args = parser.parse_args()
        env_entry = EnvironmentTable(hostname=args['hostname'],
                                     operating_system=args['operating_system'])
        db_session.add(env_entry)
        db_session.commit()
        env_info = serialize_env_table_entry(env_entry)
        return env_info, 201
