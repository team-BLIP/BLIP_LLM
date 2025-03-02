from src.ai.speech2text import SpeechToText
from fastapi import HTTPException
import threading
import sounddevice as sd

class RecordingService:
    def __init__(self):
        self.speech_to_text = SpeechToText()
    
    def start(self):
        try:
            if not self.speech_to_text.is_recording:
                self.speech_to_text.start_recording()
                return '녹음을 시작했습니다.'
            return '이미 녹음 중입니다.'
        except Exception:
            raise HTTPException(status_code=400, detail='녹음 시작 중 오류 발생')

    def stop(self):
        if self.speech_to_text.is_recording:
            self.speech_to_text.stop_recording()
            return '녹음을 종료했습니다.'
        return '녹음 중이 아닙니다.'

    def speech2text(self):
        try:
            return self.speech_to_text.speech_to_text()
        except Exception:
            raise HTTPException(status_code=400, detail='텍스트 변환 중 오류 발생')
