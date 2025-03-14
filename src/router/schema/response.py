from pydantic import BaseModel

class SummaryResponse(BaseModel):
    summary : str
    time : str