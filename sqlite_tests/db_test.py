from database import SessionLocal, engine
from models import TvScreenerSignals, Base

db = SessionLocal()
Base.metadata.create_all(engine)
tv_signal = TvScreenerSignals(
    symbol='BNB',
    how_many=3,
)
db.add(tv_signal)
db.commit()

# symbol = TvScreenerSignals.query.filter_by(symbol='BNB').first()
symbol = db.query(TvScreenerSignals).filter_by(symbol='BNB').first()
print(symbol.symbol)
