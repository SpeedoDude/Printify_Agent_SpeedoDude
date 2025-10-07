import uuid
from datetime import datetime

class JobsManager:
    def __init__(self):
        self.jobs = {}

    def add_job(self, target, args):
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "target": target,
            "args": args,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "result": None
        }
        return job_id

    def get_job(self, job_id):
        return self.jobs.get(job_id)

    def update_job_status(self, job_id, status, result=None):
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status
            self.jobs[job_id]["result"] = result

    def get_failed_jobs(self):
        return [job for job in self.jobs.values() if job['status'] == 'failed']

jobs_manager = JobsManager()
