from fastapi import Depends, HTTPException
from src.ai.meeting_ai import BLIPMeetingAI, MeetingSummary, SpeechToText, MeetingFeedback
import traceback

class BLIPMeetingAIService:
    def __init__(self, blip_meeting_ai: BLIPMeetingAI):
        self.blip_meeting_ai = blip_meeting_ai

    async def meeting(self, file_path: str):
        try:
            summary, feedback = await self.blip_meeting_ai.meeting(file_path)
            return summary, feedback
        except Exception as e:
            error_details = traceback.format_exc()
            raise HTTPException(status_code=500, detail=f"회의 요약 중 오류 발생: {str(e)}\n{error_details}")


async def get_blip_ai(
    speech_to_text: SpeechToText = Depends(lambda: SpeechToText()),
    meeting_summarizer: MeetingSummary = Depends(lambda: MeetingSummary()),
    meeting_feedback : MeetingFeedback = Depends(lambda: MeetingFeedback())
):
    blip_ai = BLIPMeetingAI(speech_to_text=speech_to_text, meeting_summarizer=meeting_summarizer, meeting_feedback=meeting_feedback)
    return BLIPMeetingAIService(blip_meeting_ai=blip_ai)

