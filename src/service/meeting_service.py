from fastapi import Depends, HTTPException
from src.ai.meeting_ai import BLIPMeetingAI, MeetingSummary, SpeechToText
import traceback

class BLIPMeetingAIService:
    def __init__(self, blip_meeting_ai: BLIPMeetingAI):
        self.blip_meeting_ai = blip_meeting_ai

    async def meeting_summary(self, file_path: str):
        try:
            summary = await self.blip_meeting_ai.summary(file_path)
            return summary
        except Exception as e:
            error_details = traceback.format_exc()
            raise HTTPException(status_code=500, detail=f"회의 요약 중 오류 발생: {str(e)}\n{error_details}")


async def get_blip_ai(
    speech_to_text: SpeechToText = Depends(lambda: SpeechToText()),
    meeting_summarizer: MeetingSummary = Depends(lambda: MeetingSummary())
):
    blip_ai = BLIPMeetingAI(speech_to_text=speech_to_text, meeting_summarizer=meeting_summarizer)
    return BLIPMeetingAIService(blip_meeting_ai=blip_ai)

