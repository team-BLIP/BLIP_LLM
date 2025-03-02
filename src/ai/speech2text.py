import whisper
import sounddevice as sd
import numpy as np
import queue
import threading
import time

class SpeechToText:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.is_recording = False
    
    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.audio_queue.put(indata.copy())

    def start_recording(self):
        self.is_recording = True
        print('녹음 시작')

        def record():
            with sd.InputStream(samplerate=16000, channels=1, callback=self.audio_callback, dtype='float32'):
                while self.is_recording:
                    sd.sleep(100)

        threading.Thread(target=record).start()
        # 최소 녹음 보장 (0.5초 이상)
        time.sleep(0.5)

    def stop_recording(self):
        print('녹음 종료 대기 중...')
        self.is_recording = False
        time.sleep(0.5)  # 데이터가 다 들어올 때까지 기다림
        print('녹음 종료 완료')

    def speech_to_text(self):
        print('음성 인식 중...')
        model = whisper.load_model('medium')

        audio_data = []
        while not self.audio_queue.empty():
            audio_data.append(self.audio_queue.get())

        if len(audio_data) == 0:
            return '녹음된 데이터가 없습니다.'

        audio_data = np.concatenate(audio_data, axis=0).squeeze()

        result = model.transcribe(audio_data, language='ko', fp16=False)
        return result['text']
