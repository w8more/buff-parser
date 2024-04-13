import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.item.router import router as item_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    # "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item_router)