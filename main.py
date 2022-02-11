from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import unicorn_binance_websocket_api
from unicorn_binance_websocket_api import BinanceWebSocketApiManager

app = FastAPI()
ubwa: BinanceWebSocketApiManager = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa.create_stream(['trade', 'kline_1m'], ['btcusdt'], output="UnicornFy")
Schedule = AsyncIOScheduler()
Schedule.start()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "item_price": item.price}


@app.get("/cayir")
async def cayir():
    return {"message": "Hello mello"}


@app.websocket("/ws")
async def roco():
    # ubwa.create_stream(['trade'], ['btcusdt'], output="UnicornFy")
    while True:
        oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
        if oldest_data_from_stream_buffer:
            print(oldest_data_from_stream_buffer)
    # return {"message": "test"}


@app.get("/schedule/show_schedules/", tags=["schedule"])
async def get_scheduled_syncs():
    schedules = []
    for job in Schedule.get_jobs():
        schedules.append({"Name": str(job.id), "Run Frequency": str(job.trigger), "Next Run": str(job.next_run_time)})
    return schedules


@app.get("/schedule/schedule1/", tags=["schedule"])
async def add_chat_job_to_scheduler(time_in_seconds: int = 3):
    schedule1_job = Schedule.add_job(schedule1_function, 'interval', seconds=time_in_seconds, id="schedule1")
    return {"Scheduled": True, "JobID": schedule1_job.id}


@app.get("/schedule/schedule2/", tags=["schedule"])
async def add_schedule2(time_in_hours: int = 24):
    schedule2_job = Schedule.add_job(schedule2_function, 'interval', hours=time_in_hours, id="schedule2")
    return {"Scheduled": True, "JobID": schedule2_job.id}


async def schedule1_function():
    # ubwa.create_stream(['trade'], ['btcusdt'], output="UnicornFy")
    while True:
        oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
        if oldest_data_from_stream_buffer:
            print(oldest_data_from_stream_buffer)
    # return {"message": "test"}


def schedule2_function():
    print('Schedule function 2')


@app.get("/schedule/schedule1del/", tags=["schedule"])
async def remove_schedule1():
    Schedule.remove_job("schedule1")
    return {"Scheduled": False, "JobID": "schedule1 super"}


@app.get("/schedule/schedule2/", tags=["schedule"])
async def remove_schedule2(time_in_hours: int = 24):
    Schedule.remove_job("schedule2")
    return {"Scheduled": False, "JobID": "schedule2"}
