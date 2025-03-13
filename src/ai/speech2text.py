import whisper

class Speech2Text:
    def __init__(self):
        self.model = whisper.load_model('small')
    
    def transcribe(self, file_path : str):
        result = self.model.transcribe(file_path, language='ko')
        return result['text']