from functools import reduce
from datetime import datetime
from db import get_session
import os
from sqlalchemy import text
from model_response import MMSResultResponse
from json import loads

class MMSResult:
    timestamp: int
    pair: str
    mms_20: float
    mms_50: float
    mms_200: float

class MercadoBitcoin:

    def subtrai_timestamp_de_hoje(self, timestamp: float) -> int:
        timestamp = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        sub = now - timestamp
        return abs(sub.days)


    def verifica_timestamp_maior_que_365_dias(self, timestamp: float) -> bool:
        r = self.subtrai_timestamp_de_hoje(timestamp)        
        return r > 365


    def verifica_se_o_pair_esta_correto(self, pair: str) -> bool:
        return pair.upper() in ['BRLBTC', 'BRLETH']


    def chamar_api_mercado_bitcoin(self, pair: str, from_timestamp: float, to_timestamp: float):
        '''
        a cloudflare estava bloqueando as requests das libs requests e urllib3
        todo: ver o porque essas requests sao bloqueadas
        '''
        url = f"curl 'https://mobile.mercadobitcoin.com.br/v4/{pair}/candle?from={int(from_timestamp)}&to={int(to_timestamp)}&precision=1d' \
            -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0' \
            --compressed"
        print(url)
        
        r = os.popen(url).read()

        j = loads(r)

        if j['status_code'] != 100:
            raise Exception(r)

        return j

    def chamar_pelo_banco_de_dados(self, pair, inicio, fim):
        session = get_session()
        
        sql = text('''
            select * from candles where `timestamp` >= :inicio and `timestamp` <= :fim and pair = :pair        
        ''')

        cursor = session.execute(sql, {
            "pair": pair,
            "inicio": inicio,
            "fim": fim
        })

        cursor = [cc._asdict() for cc in cursor]

        return cursor

    def api_candle_mb(self, pair: str, range: int, from_timestamp: float, to_timestamp: float = None) -> list[MMSResultResponse]:
        r = self.chamar_pelo_banco_de_dados(pair, from_timestamp, to_timestamp)
        
        return self.calcular_mms(r, [range], pair)

    def retorna_media(self, valores: list[float]) -> float:

        divisor = len(valores)

        if divisor == 0:
            return 0
        
        s = reduce(lambda x, y: x + y, valores)

        return s / divisor

    def calcular_mms(self, resultados_mb_api: list[dict], days:list[int], pair: str = "BRLBTC") -> list[MMSResultResponse]:

        l = []

        for k, r in enumerate(resultados_mb_api):

            mms_result = MMSResultResponse(
                timestamp=0,
                pair="",
                mms_20=None,
                mms_50=None,
                mms_200=None
            )

            mms_result.timestamp = r["timestamp"]
            mms_result.pair = pair

            for day in days:

                if not hasattr(mms_result, f"mms_{day}"):
                    continue
                
                mms_result.__setattr__(f"mms_{day}", None)

                if day > k:
                    continue
                      
                start_position = abs(k - day)
                resultados_splice = resultados_mb_api[start_position:k]
                m = self.retorna_media([x['close'] for x in resultados_splice])
                mms_result.__setattr__(f"mms_{day}", m)

            l.append(mms_result)

        return l

    def carregar_candles():
        pass
