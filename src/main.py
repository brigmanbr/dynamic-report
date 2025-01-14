from fastapi import FastAPI
from routes.usage_routes import router as usage_router

app = FastAPI()
app.include_router(usage_router)
