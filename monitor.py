import subprocess

def get_status(job_id):
    try:
        # # Execute the sacct command to get job details by name
        # result = subprocess.check_output([
        #     'sacct', 
        #     '-j ' + job_id
        # ]).decode('utf-8')
        command = f"sacct -j {job_id} --format=JobID,JobName,State --noheader"
        # run command
        result = subprocess.check_output(command, shell=True).decode('utf-8')
        
        # Split the result by lines and then by spaces to get the job details
        lines = result.strip().split("\n")
        job_statuses = {}
        for line in lines:
            parts = line.split()
            job_id_part = parts[0]
            job_name = parts[1]
            state = parts[2]
            job_statuses[job_id_part] = {"name": job_name, "state": state}
        return job_statuses[str(job_id)]
    except subprocess.CalledProcessError:
        return None

if __name__ == "__main__":
    jobs = list(range(871818, 871823))
    waiting = ["PENDING", "RUNNING"]
    while jobs:
        for job in jobs:
            status = get_status(job)
            if status['state'] not in waiting:
                print(f"job {job} is {status}")
                jobs.remove(job)  
