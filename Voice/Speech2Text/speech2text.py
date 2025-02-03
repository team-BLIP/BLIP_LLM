import whisper
import os
from dotenv import load_dotenv


class Speech2Text:
    def __init__(self):
        load_dotenv()
        self.audio_file_path = os.getenv("AUDIO_FILE_PATH")
        self.model = whisper.load_model('medium')
    
    def text_generation(self):
        result = self.model.transcribe(self.audio_file_path, language="ko")
        meeting_text = result["text"]

        with open("meeting_text.txt", "w", encoding='utf-8') as f:
            f.write(meeting_text)
