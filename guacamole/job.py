from flask_restful import abort, reqparse, Resource

from .database import db_session
from .models import Environment as EnvironmentTable
from .models import Job as JobTable
from .runner import TestRunner


def get_job_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('requester')
    parser.add_argument('environment')
    parser.add_argument('test')
    return parser


def serialize_job_table_entry(entry):
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
        res = [serialize_job_table_entry(entry) for
               entry in JobTable.query.all()]
        return {"results": res, "count": len(res)}

    def post(self):
        parser = get_job_parser()
        args = parser.parse_args()
        env_id = args['environment']
        env_entry = EnvironmentTable.query.filter_by(id=int(env_id))
        if not env_entry:
            abort(404, message="Environment {} doesn't exist".format(env_id))
        env = env_entry.first()
        if env.current_job is not None:
            abort(404, message="Environment {} is already running a job".format(env_id))
        job_entry = JobTable(requester=args['requester'],
                             environment=args['environment'],
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
