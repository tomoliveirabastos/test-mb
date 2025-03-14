from pydantic import BaseModel

class MMSResultResponse(BaseModel):
    timestamp: int
    pair: str
    mms_20: float
    mms_50: float
    mms_200: float
