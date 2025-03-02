from src.ai.personal_feedback import PersonalFeedback
from src.ai.speech2text import stop_recording, speech_to_text
from fastapi import HTTPException, status, Depends

# class FeedbackService:
#     def __init__(self, personal_feedback : PersonalFeedback, speech2text : Speech2Text):
#         self.personal_feedback = personal_feedback
#         self.speech2text = speech2text
    
#     def feedback(self):
#         try:
#             content = self.speech2text.simulate_call()
#             output = self.personal_feedback.generate_feedback(content=content)
#             return output
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail='개인 피드백을 하는 도중 오류가 발생하였습니다.'
#             )

            


# def get_feedback_service():
#     return FeedbackService(personal_feedback=PersonalFeedback(), speech2text=Speech2Text())

# a = FeedbackService(PersonalFeedback(), Speech2Text())
# b = a.feedback()
# print(b)