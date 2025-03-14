from fastapi import FastAPI, Request
from services.mercado_bitcoin import MercadoBitcoin
from model_response import MMSResultResponse
import time

app = FastAPI()

# @app.middleware("http")
# async def watch_request(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)

#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
    

@app.get("/{pair}/mms")
async def index(pair: str, from_timestamp: float, to_timestamp: float, range: int) -> list[MMSResultResponse]:
    
    try:
        mb = MercadoBitcoin()
        r = mb.api_candle_mb(pair=pair, range=range, from_timestamp=from_timestamp, to_timestamp=to_timestamp)

        return r
    
    except BaseException as er:
        return {
            "error": str(er)
        }