#!/bin/bash
PORT='5000'
curl http://localhost:${PORT}/environments/ -H "Content-Type:application/json" -d '{"hostname": "foo.bar.com", "operating_system": "CentOS"}' -X POST -v
curl http://localhost:${PORT}/environments/ -H "Content-Type:application/json" -d '{"hostname": "baz.bar.com", "operating_system": "Debian"}' -X POST -v
curl http://localhost:${PORT}/environments/ -H "Content-Type:application/json" -d '{"hostname": "boo.bar.com", "operating_system": "Fedora"}' -X POST -v
curl http://localhost:${PORT}/environments/3 -X DELETE -v
curl http://localhost:${PORT}/jobs/ -H "Content-Type:application/json" -d '{"requester": "lmr", "environment": 1, "test": "gdbtest.py"}' -X POST -v
curl http://localhost:${PORT}/jobs/ -H "Content-Type:application/json" -d '{"requester": "lmr", "environment": 1, "test": "gdbtest.py"}' -X POST -v
curl http://localhost:${PORT}/jobs/ -H "Content-Type:application/json" -d '{"requester": "lmr", "environment": 2, "test": "gdbtest.py"}' -X POST -v
curl http://localhost:${PORT}/jobs/
curl http://localhost:${PORT}/environments/
