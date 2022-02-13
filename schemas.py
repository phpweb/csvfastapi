from datetime import date
from pydantic import BaseModel


class TvScreenerSignals(BaseModel):
    id: int
    symbol: str
    date: date
    how_many: int

    class Config:
        orm_mode = True
