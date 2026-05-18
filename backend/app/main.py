from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Resume Screening System")

app.include_router(router)
