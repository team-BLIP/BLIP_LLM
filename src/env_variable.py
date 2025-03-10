import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
MEETING_TEXT = os.getenv('MEETING_TEXT')
PERSONAL_TEXT = os.getenv('PERSONAL_TEXT')