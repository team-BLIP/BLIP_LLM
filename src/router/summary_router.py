from fastapi import APIRouter, HTTPException, Depends
from Service.meeting_summary import MeetingSummarizer
from router.Schema.response import SummaryResponse
import threading

router = APIRouter()

_summarizer = None
_lock = threading.Lock()  # Lock 추가

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        with _lock:  # Thread-safe 처리
            if _summarizer is None:
                _summarizer = MeetingSummarizer()
    return _summarizer

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_meeting(summarizer: MeetingSummarizer = Depends(get_summarizer)):
    try:
        summary = summarizer.summarize_meeting()
        return {"summary" : summary}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )