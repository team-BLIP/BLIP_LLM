from fastapi import APIRouter, Depends
from src.service.recording_service import RecordingService
from functools import lru_cache

router = APIRouter()

@lru_cache() #추후 user마다 RecordingService를 줘서 개발할 예정
def get_recording_service():
    return RecordingService()

@router.get('/start')
async def start(recording_service: RecordingService = Depends(get_recording_service)):
    message = recording_service.start()
    return {'message': message}

@router.post('/end')
async def end(recording_service: RecordingService = Depends(get_recording_service)):
    recording_service.stop()
    result = recording_service.speech2text() #결과값을 레포지토리에 저장할 예정
    return {'result': result}
