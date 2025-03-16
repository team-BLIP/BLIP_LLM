from src.ai.meeting_summary import MeetingSummary
from src.ai.speech2text import SpeechToText
from src.ai.meeting_feedback import MeetingFeedback

class BLIPMeetingAI:
    def __init__(self, speech_to_text: SpeechToText, meeting_summarizer: MeetingSummary, meeting_feedback : MeetingFeedback):
        self.speech_to_text = speech_to_text
        self.meeting_summarizer = meeting_summarizer
        self.meeting_feedback = meeting_feedback
    
    async def _transcribe(self, file_path: str):
        return await self.speech_to_text.transcribe_audio(file_path)

    async def _summarize(self, text: str):
        return await self.meeting_summarizer.generate_text(text)
    
    async def _feedback(self, text: str):
        return await self.meeting_feedback.generate_text(text)

    async def meeting(self, file_path: str):
        speech2text = await self._transcribe(file_path)
        meeting_summary = await self._summarize(speech2text)
        meeting_feedback = await self._feedback(speech2text)
        return meeting_summary, meeting_feedback
