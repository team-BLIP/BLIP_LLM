from fastapi import FastAPI
from src.router import recording_router

app = FastAPI()
app.include_router(recording_router.router)

@app.get('/')
def root():
    return "hello"

