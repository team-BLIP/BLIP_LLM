# from fastapi import APIRouter, Depends
# from src.service.feedback_service import FeedbackService, get_feedback_service
# from src.router.schema.response import FeedbackResponse

# router = APIRouter()


# @router.post('/feedback', response_model=FeedbackResponse)
# async def feedback_handler(feedback_service : FeedbackService = Depends(get_feedback_service)):
#     feedback = await feedback_service.feedback()
#     return {'feedback' : feedback}
