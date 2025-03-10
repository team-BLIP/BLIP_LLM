from fastapi import APIRouter, Depends
from src.service.summary_service import SummaryService, get_summary_meeting
from enum import Enum

router = APIRouter()

from src.env_variable import MEETING_TEXT

with open(MEETING_TEXT, encoding='utf-8') as f:
         meeting_text = f.read()

@router.post('/summary')
def summary(summary_service : SummaryService = Depends(get_summary_meeting)):
    msummary = summary_service.summary_meeting(contents=meeting_text)
    return msummary