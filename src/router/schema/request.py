from pydantic import BaseModel, HttpUrl

class MeetingRequest(BaseModel):
    s3_url: str