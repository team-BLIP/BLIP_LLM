from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from src.service.meeting_service import BLIPMeetingAIService, get_blip_ai
from src.router.schema.response import SummaryResponse
import os
import uuid
from tempfile import gettempdir
import time

router = APIRouter()

@router.post('/meeting', response_model=SummaryResponse)
async def meeting_ai(
    meeting_service: BLIPMeetingAIService = Depends(get_blip_ai), 
    file: UploadFile = File(...)
):
    allowed_types = {"audio/mpeg", "audio/wav", "audio/mp3", "audio/x-wav"}

    # 파일 MIME 타입 검사
    if not file.content_type or file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="오디오 파일만 업로드 가능합니다.")
    
    # 임시 디렉토리 생성
    temp_dir = os.path.join(gettempdir(), "speech2text")
    os.makedirs(temp_dir, exist_ok=True)

    # 파일 저장
    file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
    
    try:
        start_time = time.time()
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # 음성 요약과 피드백을 수행
        summary, feedback = await meeting_service.meeting(file_path=file_path)
        end_time = time.time()
        return {'summary' : summary,'feedback':feedback, 'time' : f"{(end_time-start_time)//60}분 {(end_time-start_time)%60}초"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류 발생: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
