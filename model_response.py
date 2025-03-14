from pydantic import BaseModel
from typing import Optional

class MMSResultResponse(BaseModel):
    timestamp: int
    pair: str
    mms_20: Optional[float] = None
    mms_50: Optional[float] = None
    mms_200: Optional[float] = None
