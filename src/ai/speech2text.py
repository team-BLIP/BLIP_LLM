import asyncio
import whisper


class SpeechToText:
    _model = None  # 싱글톤 모델

    def __init__(self):
        if SpeechToText._model is None:
            SpeechToText._model = whisper.load_model('small')
        self.model = SpeechToText._model
    
    async def transcribe_audio(self, file_path: str):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: self.model.transcribe(file_path, language='ko'))
        return result['text']