from fastapi import APIRouter, Depends, HTTPException
from src.service.meeting_service import BLIPMeetingAIService, get_blip_ai
from src.router.schema.response import MeetingResponse
from src.router.schema.request import MeetingRequest
import os
import time
import httpx
import logging
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/meeting', response_model=MeetingResponse)
async def meeting_ai(
    request: MeetingRequest,
    meeting_service: BLIPMeetingAIService = Depends(get_blip_ai),
):
    s3_url = str(request.s3_url)  # HttpUrl → str 변환

    # URL 유효성 검사
    parsed_url = urlparse(s3_url)
    if parsed_url.scheme not in ["http", "https"]:
        raise HTTPException(status_code=400, detail="올바른 S3 URL이 아닙니다.")

    # 임시 파일 생성 및 명시적 close (Windows 호환)
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        file_path = temp_file.name
        temp_file.close()

    try:
        start_time = time.perf_counter()  # 성능 측정 시작

        # 파일 다운로드
        async with httpx.AsyncClient() as client:
            response = await client.get(s3_url)
            response.raise_for_status()

        # 파일 저장
        with open(file_path, "wb") as buffer:
            buffer.write(response.content)

        if not os.path.exists(file_path):
            logger.warning(f"파일이 저장되지 않음: {file_path}")

        # 음성 요약 & 피드백 처리
        summary, feedback = await meeting_service.meeting(file_path=file_path)
        elapsed_time = time.perf_counter() - start_time
        elapsed_min, elapsed_sec = divmod(elapsed_time, 60)

        return MeetingResponse(
            summary=summary,
            feedback=feedback,
            time=f"{int(elapsed_min)}분 {int(elapsed_sec)}초"
        )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            detail = "S3 presigned URL이 만료되었거나 권한이 없습니다."
        else:
            detail = f"S3에서 파일을 가져올 수 없습니다. (HTTP {e.response.status_code})"
        logger.error(detail, exc_info=True)
        raise HTTPException(status_code=400, detail=detail)

    except httpx.RequestError as e:
        logger.error(f"S3 요청 오류: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="S3 파일을 가져오는 중 네트워크 오류가 발생했습니다.")

    except Exception as e:
        logger.error(f"파일 처리 중 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류가 발생했습니다: {str(e)}")

    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"임시 파일 삭제 완료: {file_path}")
            except Exception as cleanup_error:
                logger.warning(f"임시 파일 삭제 중 오류 발생: {cleanup_error}", exc_info=True)
