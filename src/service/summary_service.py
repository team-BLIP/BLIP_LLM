from fastapi import HTTPException, Depends
from src.ai.summary import MeetingSummary

class SummaryService:
    def __init__(self, meeting_summary: MeetingSummary):
        self.meeting_summary = meeting_summary

    def summary_meeting(self, contents: str):
        try:
            output = self.meeting_summary.generate_text(contents)
            return output
        except Exception as e:
            print(f"[Error] 회의 요약 중 오류 발생: {e}")  # 혹은 로깅 사용
            raise HTTPException(status_code=500, detail="회의 요약 중 오류가 발생했습니다.")

def get_summary_meeting(meeting_summary: MeetingSummary = Depends()):
    return SummaryService(meeting_summary)