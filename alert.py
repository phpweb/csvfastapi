import time
from fastapi import FastAPI
from test_lavida import LoginOnly

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
