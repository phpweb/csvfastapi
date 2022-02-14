import time
from typing import Optional
from fastapi import FastAPI, BackgroundTasks
from test_lavida import LoginOnly
from send_email import send_email_background
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = FastAPI()
Schedule = AsyncIOScheduler()
Schedule.start()


@app.get("/")
async def root():
    return {"message": "Hello World ramazan test neci be"}


@app.get("/csv")
async def root(background_tasks: BackgroundTasks):
    start = time.time()
    csv_import = LoginOnly()
    email_message_list = csv_import.download_csv_file_and_set_alerts_volume_15m()
    request_time = time.time() - start
    email_sent = None
    if len(email_message_list) > 0:
        send_email_background(background_tasks, '15 minutes', 'phpwebentwickler@gmail.com', email_message_list)
        email_sent = True
    return {"message": f"CSV has been imported. Time {request_time} email sent={email_sent}"}


@app.get("/schedule/show_schedules/", tags=["schedule"])
async def get_scheduled_syncs():
    schedules = []
    for job in Schedule.get_jobs():
        schedules.append({"Name": str(job.id), "Run Frequency": str(job.trigger), "Next Run": str(job.next_run_time)})
    return schedules


@app.get("/start_schedule/{job_id}", tags=["schedule"])
async def scheduled_task_start(job_id: str, interval: Optional[int] = 15):
    function_mappings = {
        'download_volume_15m': download_volume_15m,
    }
    scheduled_job = Schedule.add_job(function_mappings[job_id], 'interval', seconds=interval, id=job_id)
    return {"Scheduled": True, "JobID": scheduled_job.id}


async def download_volume_15m():
    print('download_volume_15m is running')
    csv_import = LoginOnly()
    email_message_list = csv_import.download_csv_file_and_set_alerts_volume_15m()
    if len(email_message_list) > 0:
        background_tasks = BackgroundTasks()
        send_email_background(background_tasks, '15 minutes', 'phpwebentwickler@gmail.com', email_message_list)


@app.get("/del_schedule/{job_id}", tags=["schedule"])
async def remove_scheduled_job(job_id: str):
    Schedule.remove_job(job_id)
    return {"Scheduled": False, "JobID": job_id}
