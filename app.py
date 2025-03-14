from fastapi import FastAPI
from services.mercado_bitcoin import MercadoBitcoin
from model_response import MMSResultResponse

app = FastAPI()

# "from" é uma keyword do python, não é possivel usa-la como variavel
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