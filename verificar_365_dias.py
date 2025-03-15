from services.mercado_bitcoin import MercadoBitcoin
from datetime import datetime, timedelta
from sqlalchemy import text
from db import get_session
from os import environ
import smtplib

class Verifica365:

    def get_todas_as_datas_de_um_ano_ate_hoje(self) -> list[str]:
        datas = []

        for d in range(1, 365):
            dia_subtraido = (datetime.now() - timedelta(days=d))
            datas.append(dia_subtraido.strftime("%Y-%m-%d"))

        return datas


    def retorna_as_datas_sem_registro_no_banco(self, todos_registros_do_banco: list[str]) -> list[str]:
        todos_dias_365: list[str] = self.get_todas_as_datas_de_um_ano_ate_hoje()
        d : list[str] = filter(lambda _365: _365 not in todos_registros_do_banco, todos_dias_365)        
        return list(d)


    def get_somente_registros_que_nao_esteja_no_banco(self) -> list[str]:
        sql = "select * from candles where `timestamp` >= :inicio and `timestamp` <= :fim"

        hoje = datetime.now().timestamp()
        
        um_ano = (datetime.now() - timedelta(days=365)).timestamp()

        session = get_session()
        
        cursor = session.execute(text(sql), {
            "inicio": um_ano,
            "fim": hoje
        })

        registros: list[str] = [datetime.fromtimestamp(cc._asdict()['timestamp']).strftime("%Y-%m-%d") for cc in cursor]

        faltando = self.retorna_as_datas_sem_registro_no_banco(registros)

        return faltando

    def send_email_de_notificacao(self, message: str):
        s = smtplib.SMTP(environ.get("EMAIL_HOST"), 587)
        s.starttls()
        s.login(environ.get("EMAIL_FROM"), environ.get("EMAIL_PASSWORD"))
        s.sendmail(environ.get("EMAIL_FROM"), environ.get("EMAIL_FROM"), message)
        s.quit()
        

    def notificar():
        v = Verifica365()
        registros = v.get_somente_registros_que_nao_esteja_no_banco()

        if len(registros) > 0:
            message = '''
                nao foi encontrado os registros nessas datas {}
            '''.format(
                ','.join(registros)
            )
            v.send_email_de_notificacao(message)