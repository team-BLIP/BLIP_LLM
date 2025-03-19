from src.router import meeting_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(meeting_router.router)


@app.get('/')
def root():
    return 'hello'