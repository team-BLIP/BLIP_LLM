from pydantic import BaseModel

class MeetingResponse(BaseModel):
    summary : str
    feedback : str
    time : str