import threading
import time

import pexpect

from .database import db_session
from .models import Environment as EnvironmentTable
from .models import Job as JobTable


class TestRunner(object):

    def __init__(self, test, job_id):
        self.job_id = job_id
        self.test = test
        self.status = 'SCHEDULED'
        self.sp = None
        self.output = ''
        self.start = None
        self.end = None
        self.duration = None
        self.runner_thread = None
        self.output_lock = threading.Lock()

    def _update_status(self, status):
        self.status = status
        job_entry = JobTable.query.filter_by(id=self.job_id).first()
        job_entry.status = status
        db_session.commit()

    def _update_duration(self, duration):
        self.duration = duration
        job_entry = JobTable.query.filter_by(id=self.job_id).first()
        job_entry.duration = duration
        db_session.commit()

    @staticmethod
    def _clear_env_job(env_id):
        environment_entry = EnvironmentTable.query.filter_by(id=env_id).first()
        environment_entry.current_job = None
        db_session.commit()

    def run_blocking(self, env_id):
        self.start = time.time()

        job_entry = JobTable.query.filter_by(id=self.job_id).first()
        child = pexpect.spawn('avocado run %s' % self.test, timeout=None)
        self._update_status('RUNNING')
        while True:
            try:
                child.expect('\n')
                line = child.before
                self.output += line.replace('\r', '\n')
                job_entry.output = self.output
                db_session.commit()
            except pexpect.EOF:
                break
        return_status = child.wait()
        self.end = time.time()
        self._update_duration(self.end - self.start)
        if return_status != 0:
            self._update_status('FAIL')
        else:
            self._update_status('PASS')
        self._clear_env_job(env_id)

    def run(self, env_id):
        self.runner_thread = threading.Thread(target=self.run_blocking,
                                              args=(env_id,))
        self.runner_thread.start()

    def dump(self):
        info_dict = dict()
        info_dict['status'] = self.status
        info_dict['output'] = self.output
        info_dict['start'] = self.start
        info_dict['end'] = self.end
        info_dict['duration'] = self.duration
        return info_dict
