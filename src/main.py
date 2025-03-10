from fastapi import FastAPI
from src.router import summary_router

app = FastAPI()
app.include_router(summary_router.router)

@app.get('/')
def root():
    return 'hello'