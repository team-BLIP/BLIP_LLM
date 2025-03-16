import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.service.meeting_service import get_blip_ai
from src.main import app
from io import BytesIO
import asyncio
import httpx
from httpx import ASGITransport

# 가짜 음성 요약 및 피드백 서비스 Mocking
test_summary = "이것은 테스트 요약입니다."
test_feedback = "이것은 테스트 피드백입니다."
mock_meeting_service = AsyncMock()
mock_meeting_service.meeting.return_value = test_summary, test_feedback

# 종속성 오버라이드
def override_get_blip_ai():
    return mock_meeting_service

app.dependency_overrides[get_blip_ai] = override_get_blip_ai
client = TestClient(app)


def test_meeting_ai_success():
    """올바른 오디오 파일 업로드 시 성공하는지 테스트 (요약 + 피드백)"""
    fake_audio = BytesIO(b"Fake audio data")
    files = {"file": ("test.mp3", fake_audio, "audio/mpeg")}

    response = client.post("/meeting", files=files)

    assert response.status_code == 200
    data = response.json()
    
    assert "summary" in data
    assert data["summary"] == test_summary
    assert "feedback" in data
    assert data["feedback"] == test_feedback
    assert "time" in data  # 실행 시간 포함


def test_meeting_ai_invalid_file():
    """잘못된 파일 타입 업로드 시 400 에러 반환"""
    fake_text = BytesIO(b"Fake text data")
    files = {"file": ("test.txt", fake_text, "text/plain")}

    response = client.post("/meeting", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "오디오 파일만 업로드 가능합니다."


def test_meeting_ai_no_file():
    """파일을 업로드하지 않았을 때 422 에러 반환"""
    response = client.post("/meeting")

    assert response.status_code == 422  # FastAPI의 기본 동작에 맞춰 422로 유지
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_concurrent_meeting_ai_requests():
    """여러 사용자가 동시에 오디오 파일 업로드 시 정상적으로 처리되는지 테스트 (요약 + 피드백)"""
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        num_requests = 5  # 동시 요청 개수

        async def upload_audio():
            fake_audio = BytesIO(b"Fake audio data")  # 각 요청마다 새로운 BytesIO 객체 생성
            files = {"file": ("test.mp3", fake_audio, "audio/mpeg")}
            return await async_client.post("/meeting", files=files)

        tasks = [upload_audio() for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

        for response in responses:
            assert response.status_code == 200
            data = response.json()
            
            assert "summary" in data
            assert data["summary"] == test_summary
            assert "feedback" in data
            assert data["feedback"] == test_feedback
            assert "time" in data


def test_meeting_ai_internal_server_error():
    """Mock을 이용해 강제 오류 발생 시 500 에러 반환 테스트 (요약 + 피드백)"""
    mock_meeting_service.meeting.side_effect = Exception("Test error")  # 예외 발생 설정

    fake_audio = BytesIO(b"Fake audio data")
    files = {"file": ("test.mp3", fake_audio, "audio/mpeg")}

    response = client.post("/meeting", files=files)

    assert response.status_code == 500
    assert "파일 처리 중 오류 발생" in response.json()["detail"]
