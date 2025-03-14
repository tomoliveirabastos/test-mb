from models.logs import Logs
from db import get_session

class LogService:

    def register_log(self, logs: Logs):
        session = get_session()
        session.add(logs)
        session.commit()