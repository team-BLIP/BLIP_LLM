from src.ai.meeting_summary import MeetingSummary
from src.ai.speech2text import SpeechToText

class BLIPMeetingAI:
    def __init__(self, speech_to_text: SpeechToText, meeting_summarizer: MeetingSummary):
        self.speech_to_text = speech_to_text
        self.meeting_summarizer = meeting_summarizer
    
    async def _transcribe(self, file_path: str):
        return await self.speech_to_text.transcribe_audio(file_path)

    async def _summarize(self, text: str):
        return await self.meeting_summarizer.generate_text(text)

    async def summary(self, file_path: str):
        speech2text = await self._transcribe(file_path)
        meeting_summary = await self._summarize(speech2text)
        return meeting_summary
