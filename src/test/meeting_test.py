import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.service.meeting_service import get_blip_ai
from src.main import app
from io import BytesIO
import asyncio
import httpx
from httpx import ASGITransport


# 가짜 음성 요약 서비스 Mocking
test_summary = "이것은 테스트 요약입니다."
mock_meeting_service = AsyncMock()
mock_meeting_service.meeting_summary.return_value = test_summary

# 종속성 오버라이드
def override_get_blip_ai():
    return mock_meeting_service

app.dependency_overrides[get_blip_ai] = override_get_blip_ai
client = TestClient(app)


def test_meeting_summary_success():
    """올바른 오디오 파일 업로드 시 성공하는지 테스트"""
    fake_audio = BytesIO(b"Fake audio data")
    files = {"file": ("test.mp3", fake_audio, "audio/mpeg")}
    
    response = client.post("/summary", files=files)
    
    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json()["summary"] == test_summary
    assert "time" in response.json()


def test_meeting_summary_invalid_file():
    """잘못된 파일 타입 업로드 시 400 에러 반환"""
    fake_text = BytesIO(b"Fake text data")
    files = {"file": ("test.txt", fake_text, "text/plain")}
    
    response = client.post("/summary", files=files)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "오디오 파일만 업로드 가능합니다."


def test_meeting_summary_no_file():
    """파일을 업로드하지 않았을 때 422 에러 반환"""
    response = client.post("/summary")
    
    assert response.status_code == 422  # 필수 필드 누락 시 422 Unprocessable Entity


@pytest.mark.asyncio
async def test_concurrent_meeting_summaries():
    """여러 사용자가 동시에 오디오 파일 업로드 시 정상적으로 처리되는지 테스트"""
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        num_requests = 5  # 동시 요청 개수
        fake_audio = BytesIO(b"Fake audio data")

        async def upload_audio():
            files = {"file": ("test.mp3", fake_audio, "audio/mpeg")}
            return await async_client.post("/summary", files=files)

        tasks = [upload_audio() for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

        for response in responses:
            assert response.status_code == 200
            assert "summary" in response.json()
            assert response.json()["summary"] == test_summary
            assert "time" in response.json()


def test_meeting_summary_internal_server_error():
    """Mock을 이용해 강제 오류 발생 시 500 에러 반환 테스트"""
    mock_meeting_service.meeting_summary.side_effect = Exception("Test error")

    fake_audio = BytesIO(b"Fake audio data")
    files = {"file": ("test.mp3", fake_audio, "audio/mpeg")}
    
    response = client.post("/summary", files=files)
    
    assert response.status_code == 500
    assert "파일 처리 중 오류 발생" in response.json()["detail"]
