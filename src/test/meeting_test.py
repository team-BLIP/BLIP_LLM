import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import AsyncMock
from src.router.meeting_router import router
from src.service.meeting_service import BLIPMeetingAIService, get_blip_ai

app = FastAPI()
app.include_router(router)

@pytest.fixture
def mock_meeting_service(mocker):
    """BLIPMeetingAIService를 Mocking하여 실제 호출을 막음"""
    mock_service = mocker.AsyncMock(spec=BLIPMeetingAIService)
    mock_service.meeting.return_value = ("요약 결과", "피드백 결과")
    return mock_service

@pytest.fixture
async def async_client(mock_meeting_service):
    """FastAPI 비동기 클라이언트 생성"""
    app.dependency_overrides[get_blip_ai] = lambda: mock_meeting_service  # Mock 주입

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_meeting_ai_success(async_client, mock_meeting_service, mocker):
    """정상적인 S3 URL이 주어졌을 때, 올바른 응답이 반환되는지 테스트"""
    mock_response = mocker.patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock)
    mock_response.return_value.status_code = 200
    mock_response.return_value.content = b"mock audio data"

    response = await async_client.post("/meeting", json={"s3_url": "https://valid-s3-url.com/audio.mp3"})

    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "feedback" in data
    assert "time" in data
    assert data["summary"] == "요약 결과"
    assert data["feedback"] == "피드백 결과"

@pytest.mark.asyncio
async def test_meeting_ai_invalid_url(async_client):
    """잘못된 S3 URL이 주어졌을 때 400 오류를 반환하는지 테스트"""
    response = await async_client.post("/meeting", json={"s3_url": "invalid-url"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "올바른 S3 URL이 아닙니다."

@pytest.mark.asyncio
async def test_meeting_ai_file_download_fail(async_client, mocker):
    """파일 다운로드 실패 시 400 오류를 반환하는지 테스트"""

    # httpx.AsyncClient.get()을 직접 비동기 Mock으로 설정
    async def mock_get(*args, **kwargs):
        raise httpx.HTTPStatusError(
            message="Not Found",
            request=httpx.Request(method="GET", url="https://valid-s3-url.com/audio.mp3"),
            response=httpx.Response(status_code=404)
        )

    mocker.patch.object(httpx.AsyncClient, "get", side_effect=mock_get)

    response = await async_client.post("/meeting", json={"s3_url": "https://valid-s3-url.com/audio.mp3"})

    assert response.status_code == 400
    assert response.json()["detail"] == "S3에서 파일을 가져올 수 없습니다. (HTTP 404)"


@pytest.mark.asyncio
async def test_meeting_ai_internal_error(async_client, mock_meeting_service, mocker):
    """서비스 내부에서 예외 발생 시 500 오류를 반환하는지 테스트"""
    mock_response = mocker.patch.object(httpx.AsyncClient, "get", new_callable=AsyncMock)
    mock_response.return_value.status_code = 200
    mock_response.return_value.content = b"mock audio data"

    # meeting_service.meeting 호출 시 예외 발생하도록 설정
    mock_meeting_service.meeting.side_effect = Exception("내부 오류 발생")

    response = await async_client.post("/meeting", json={"s3_url": "https://valid-s3-url.com/audio.mp3"})

    assert response.status_code == 500
    assert "파일 처리 중 오류가 발생했습니다" in response.json()["detail"]
