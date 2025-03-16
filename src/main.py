from src.router import meeting_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(meeting_router.router)

@app.get('/')
def root():
    return 'hello'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)