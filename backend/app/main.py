from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Resume Screening System")

@app.on_event("startup")
async def startup_event():
    print("server is live")

@app.get("/")
async def root():
    return {"message": "server is live"}

app.include_router(router)
