"""
Job resource entry point for Guacamole.
"""
from flask_restful import abort, reqparse, Resource

from .database import db_session
from .models import Environment as EnvironmentTable
from .models import Job as JobTable
from .runner import TestRunner


def get_job_parser():
    """
    Parse parameters passed to the HTTP request at the /jobs resource.

    :return: Base dict structure holding parameters passed to a request.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('requester')
    parser.add_argument('environment')
    parser.add_argument('test')
    return parser


def serialize_job_table_entry(entry):
    """
    Serialize a SQLAlchemy env model into a python dictionary.

    :param entry: SQLAlchemy model instance.
    :return: Dict with environment table data.
    """
    return {'id': entry.id,
            'requester': entry.requester,
            'environment': entry.environment,
            'test': entry.test,
            'status': entry.status,
            'output': entry.output,
            'duration': entry.duration}


class JobInfo(object):

    def __init__(self, job_id, requester, environment):
        self.id = job_id
        self.requester = requester
        self.environment = environment
        self.runner = None

    def set_runner(self, runner):
        self.runner = runner

    def dump(self):
        """
        Serialize Job information into a dict, convenient for REST API usage.

        :return: Dict with job information.
        """
        info_dict = dict()
        info_dict['id'] = self.id
        info_dict['requester'] = self.requester
        info_dict['environment'] = self.environment
        runner_info_dict = self.runner.dump()
        info_dict.update(runner_info_dict)
        return info_dict


class Job(Resource):
    """
    Shows a single job and lets you delete a job.
    """

    @staticmethod
    def abort_if_doesnt_exist(job_id, job_entry):
        if not job_entry:
            abort(404, message="Job {} doesn't exist".format(job_id))

    def get(self, job_id):
        job_entry = JobTable.query.filter_by(id=job_id)
        self.abort_if_doesnt_exist(job_id, job_entry.first())
        return serialize_job_table_entry(job_entry.first())

    def delete(self, job_id):
        job_entry = JobTable.query.filter_by(id=job_id)
        self.abort_if_doesnt_exist(job_id, job_entry.first())
        job_entry.delete()
        db_session.commit()
        return '', 204


class JobList(Resource):
    """
    Shows a list of your jobs, and lets you POST to add new jobs.
    """
    def get(self):
        """
        Get all Jobs.

        :return: Dict with results and count of results.
        """
        res = [serialize_job_table_entry(entry) for
               entry in JobTable.query.all()]
        return {"results": res, "count": len(res)}

    def _validate_env(self, env_id):
        try:
            env_id = int(env_id)
        except ValueError:
            e_msg = "Invalid Environment ID {}".format(env_id)
            abort(404, message=e_msg)
        env_entry = EnvironmentTable.query.filter_by(id=env_id)
        env = env_entry.first()
        if not env:
            e_msg = "Environment {} doesn't exist".format(env_id)
            abort(404, message=e_msg)
        if env.current_job is not None:
            e_msg = "Environment {} is already running a job".format(env_id)
            abort(404, message=e_msg)
        return env_id, env

    def post(self):
        """
        Create a Job.

        :return: Dict with newly created job info and HTTP 201.
        """
        parser = get_job_parser()
        args = parser.parse_args()
        env_id, env = self._validate_env(args['environment'])
        job_entry = JobTable(requester=args['requester'],
                             environment=env_id,
                             test=args['test'])
        db_session.add(job_entry)
        db_session.commit()
        env.current_job = job_entry.id
        db_session.commit()
        test_runner = TestRunner(test=args['test'], job_id=job_entry.id)
        test_runner.run(env_id=env_id)
        job_info = JobInfo(job_id=job_entry.id,
                           requester=args['requester'],
                           environment=args['environment'])
        job_info.set_runner(test_runner)
        return job_info.dump(), 201
