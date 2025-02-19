from fastapi import APIRouter, HTTPException
from Service.meeting_summary import MeetingSummarizer
from router.Schema.response import SummaryResponse

router = APIRouter()
summarizer = MeetingSummarizer()

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_meeting():
    try:
        summary = summarizer.summarize_meeting()
        return {"summary" : summary}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )