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

class Routines(BaseModel):
    pass

class Preferences(BaseModel):
    pass

class Medicines(BaseModel):
    pass

class Schedule(BaseModel):
    pass

class ImageList(BaseModel):
    images: List[str]
    userID: str
    routines: Routines

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/preferences/{user_id}")
async def get_preferences(user_id: str):
    preferences = Preferences()
    # TODO: Implement logic to retrieve preferences for the given user_id
    return preferences

@app.get("/medicines/{user_id}")
async def get_medicines(user_id: str):
    medicines = Medicines()
    # TODO: Implement logic to retrieve medicines for the given user_id
    return medicines

@app.get("/schedule/{user_id}")
async def get_schedule(user_id: str):
    schedule = Schedule()
    # TODO: Implement logic to retrieve schedule for the given user_id
    return schedule

class Feedback(BaseModel):
    pass

@app.post("/meds")
async def meds(image_list: ImageList):
    image_list = image_list.images
    all_stuffs = picture_to_image(image_list)
    processed_stuffs = create_schedule(all_stuffs, image_list.routines)
    print(processed_stuffs)

@app.post("/feedback")
async def feedback(feedback: Feedback):
    pass

@app.post("/routines")
async def routines(routines: Routines):
    pass