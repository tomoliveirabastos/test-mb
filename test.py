from services.mercado_bitcoin import MercadoBitcoin
from datetime import datetime, timedelta
import unittest

class TestMercadoBitcoin(unittest.TestCase):
    
    def test_calcular_mms_3(self):
        mb = MercadoBitcoin()

        l = self.mock_mb_payload(300)
        results = mb.calcular_mms(l, [3, 20, 50, 200])
        self.assertTrue(len(results) > 0)


    def test_calcula_subtracao_de_datas_maior_que_365_dias(self):
        mb = MercadoBitcoin()

        r = mb.verifica_timestamp_maior_que_365_dias(1577923200)
        self.assertTrue(r)


    def test_calcula_subtracao_de_datas_menor_que_365_dias(self):
        mb = MercadoBitcoin()

        r = mb.verifica_timestamp_maior_que_365_dias(datetime.now().timestamp())
        self.assertFalse(r)


    def test_calculo_correto_da_media(self):
        mb = MercadoBitcoin()
        media = mb.retorna_media([2, 3])
        self.assertTrue(media == 2.5)


    def mock_mb_payload(self, days: int) -> list[dict]:
        return [
            {
                "close": float(n),
                "high": float(n),
                "low": float(n),
                "open": float(n),
                "timestamp": self.mock_date_timestamp(n),
                "volume": 100 * n
            } for n in range(0, days) 
        ]
    
    def mock_date_timestamp(self, add_day: int) -> int:
        now = datetime.now()
        now = now + timedelta(days=add_day)
        return now.timestamp()

unittest.main()