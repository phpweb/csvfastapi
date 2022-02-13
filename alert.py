import time
from fastapi import FastAPI, BackgroundTasks
from test_lavida import LoginOnly
from send_email import send_email_background

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World ramazan test neci be"}


@app.get("/csv")
async def root():
    start = time.time()
    csv_import = LoginOnly()
    csv_import.download_csv_file_and_set_alerts_volume_15m()
    request_time = time.time() - start
    return {"message": f"CSV has been imported. Time {request_time}"}


@app.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks):
    send_email_background(background_tasks, 'Hello World', 'phpwebentwickler@gmail.com',
                          {'title': 'Hello World', 'name': 'John Doe'})
    return 'Success'
