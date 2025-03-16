from pydantic import BaseModel

class SummaryResponse(BaseModel):
    summary : str
    feedback : str
    time : str