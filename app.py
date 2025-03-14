from fastapi import FastAPI, Request, Response
from services.mercado_bitcoin import MercadoBitcoin
from model_response import MMSResultResponse
from services.log_service import LogService
from models.logs import Logs
import time

app = FastAPI()

@app.middleware("http")
async def watch_request(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)

    log = Logs(
        method=request.method,
        url=request.url,
        response=""
    )

    log_service = LogService()
    log_service.register_log(log)

    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/{pair}/mms", status_code=200)
async def index(pair: str, from_timestamp: float, to_timestamp: float, range: int, res: Response) -> list[MMSResultResponse]| dict:    
    mb = MercadoBitcoin()

    if mb.verifica_se_o_pair_esta_correto(pair) == False:
        res.status_code = 400
        return {
            "erro": "pair precisa ser ['BRLBTC' ou 'BRLETH']"
        }

    if mb.verifica_timestamp_maior_que_365_dias(from_timestamp) == True:
        res.status_code = 400
        return {
            "error": "timestamp de from maior que 365 dias"
        }

    if range not in [20, 50, 200]:
        res.status_code = 400
        return {
            "error": "o range so pode ser esse [20, 50, 200]"
        }

    if to_timestamp == None:
        dd = datetime.now() - timedelta(days=1)
        to_timestamp = dd.timestamp()

    r = mb.api_candle_mb(pair=pair, range=range, from_timestamp=from_timestamp, to_timestamp=to_timestamp)

    return r

