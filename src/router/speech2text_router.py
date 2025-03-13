from fastapi import APIRouter, Depends, File, UploadFile
from src.service.speech2text_service import Speech2TextService, get_speech_to_text
from pydantic import BaseModel

router = APIRouter()

@router.post('/speech2text')
async def speech_to_text(file : UploadFile = File(...), speech2text : Speech2TextService = Depends(get_speech_to_text)):
    file_path = f"uploaded_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    result = speech2text.create_text(file_path=file_path)
    return result