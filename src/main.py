from fastapi import FastAPI
from routes import usage_router

app = FastAPI()
app.include_router(usage_router)
