from fastapi import HTTPException, Depends
from src.ai.speech2text import Speech2Text

class Speech2TextService:
    def __init__(self, speech2text : Speech2Text):
        self.speech2text = speech2text
    def create_text(self, file_path : str):
        try:
            result = self.speech2text.transcribe(file_path=file_path)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail='텍스트로 변환 중 오류가 발생하였습니다.')

def get_speech_to_text(speech2text : Speech2Text = Depends()):
    return Speech2TextService(speech2text)