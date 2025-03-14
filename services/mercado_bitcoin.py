from functools import reduce
from datetime import datetime, timedelta
import os
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


    def chamar_api_mercado_bitcoin(self, pair: str, range: int, from_timestamp: float, to_timestamp: float):
        '''
        a cloudflare estava bloqueando as requests das libs requests e urllib3
        todo: ver o porque essas requests sao bloqueadas
        '''
        r = os.popen(f"curl 'https://mobile.mercadobitcoin.com.br/v4/{pair}/candle?from={from_timestamp}&to={to_timestamp}&precision={range}d' \
            -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0' \
            --compressed").read()

        return loads(r)


    def api_candle_mb(self, pair: str, range: int, from_timestamp: float, to_timestamp: float = None):
        
        if self.verifica_se_o_pair_esta_correto(pair) == False:
            raise "pair precisa ser ['BRLBTC' ou 'BRLETH']"

        if self.verifica_timestamp_maior_que_365_dias(from_timestamp) == True:
            raise "timestamp de from maior que 365 dias" 

        if to_timestamp == None:
            dd = datetime.now() - timedelta(days=1)
            to_timestamp = dd.timestamp()

        r = self.chamar_api_mercado_bitcoin(pair, range, from_timestamp, to_timestamp)
        return self.calcular_mms(r['candles'], [20, 50, 200])


    def retorna_media(self, valores: list[float]) -> float:

        divisor = len(valores)

        if divisor == 0:
            return 0
        
        s = reduce(lambda x, y: x + y, valores)

        return s / divisor

    def calcular_mms(self, resultados_mb_api: list[dict], days:list[int]) -> list[MMSResult]:

        l = []

        for k, r in enumerate(resultados_mb_api):

            start_position = 0

            mms_result = MMSResult()
            mms_result.timestamp = r["timestamp"]

            for day in days:
                mms_result.__setattr__(f"mms_{day}", None)

                if day > k:
                    continue                
                
                resultados_splice = resultados_mb_api[start_position:k]
                m = self.retorna_media([x['close'] for x in resultados_splice])
                mms_result.__setattr__(f"mms_{day}", m)

            l.append(mms_result)

        return l

    def carregar_candles():
        pass
