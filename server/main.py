from fastapi import FastAPI, HTTPException
from os import environ
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from processmeds import picture_to_image
from scheduler import create_schedule

from pydantic import BaseModel
from typing import List

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageList(BaseModel):
    images: List[str]

@app.get("/")
async def root():
    return {"message": "Hello World"}

routines = {
    'wakeup_time': 7 * 60,  # 7:00 am
    'bedtime': 24 * 60,     # 10:00 pm
    'meals': {
        'breakfast': 8 * 60,
        'lunch': 12 * 60,
        'dinner': 18 * 60
    }
}

@app.post("/meds")
async def meds(image_list: ImageList):
    image_list = image_list.images
    all_stuffs = picture_to_image(image_list)
    processed_stuffs = create_schedule(all_stuffs,routines)
    print(processed_stuffs)
