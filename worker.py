from services.mercado_bitcoin import MercadoBitcoin
from datetime import datetime, timedelta
from models.candles import Candles
from db import get_session
import sys

days_ = sys.argv[1]

mb = MercadoBitcoin()
pairs = ['BRLBTC', 'BRLETH']
ontem = (datetime.now() - timedelta(days=int(days_)+1)).timestamp()
now = (datetime.now() - timedelta(days=1)).timestamp()

for pair in pairs:
    a = mb.chamar_api_mercado_bitcoin(
        pair=pair,
        from_timestamp=ontem,
        to_timestamp=now
    )

    todos_candles = a['candles']

    session = get_session()

    for candle in todos_candles:
        can = Candles(
            pair=pair,
            high=candle['high'],
            close=candle['close'],
            low=candle['low'],
            open=candle['open'],
            volume=candle['volume'],
            timestamp=candle['timestamp'],
        )
        session.add(can)
        print(candle.keys())
    session.commit()