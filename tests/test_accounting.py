import unittest

from gwf_utilization.accounting import Job, get_jobs, get_jobs_from_string


class TestAccounting(unittest.TestCase):

    def test_job_utilization(self):
        job = Job(
            cores=1,
            nodes=1,
            used_walltime=12,
            allocated_time_per_core=60,
            used_cpu_time=30,
            allocated_memory=512,
            used_memory=256
        )

        self.assertEqual(job.walltime_utilization, 20)
        self.assertEqual(job.cpu_utilization, 50)
        self.assertEqual(job.memory_utilization, 50)

        job = Job(
            cores=16,
            nodes=1,
            used_walltime=12,
            allocated_time_per_core=60,
            used_cpu_time=480,
            allocated_memory=512,
            used_memory=128
        )

        self.assertEqual(job.walltime_utilization, 20)
        self.assertEqual(job.cpu_utilization, 50)
        self.assertEqual(job.memory_utilization, 25)

    def test_get_jobs_from_string(self):
        output = (
            "JobID|State|NCPUS|Elapsed|TotalCPU|Timelimit|ReqMem|MaxRSS|NNodes\n"
            "1|COMPLETED|1|00:02:00|00:06:10|06:00:00|8Gn||1\n"
            "1.batch|COMPLETED|1|00:02:00|00:06:10||8Gn|3324536K|1\n"
            "2|COMPLETED|4|00:00:10|00:00:30|2-00:00:00|4Gn||2\n"
            "2.batch|COMPLETED|4|00:00:10|00:00:30||4Gn|115180K|2\n"
        )

        jobs = list(get_jobs_from_string(output))
        self.assertEqual(len(jobs), 2)

    def test_get_jobs_with_no_job_ids_returns_empty_list(self):
        self.assertEqual(list(get_jobs(job_ids=[])), [])
