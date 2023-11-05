from os import environ
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
load_dotenv()
from processmeds import picture_to_image
from scheduler import create_schedule, reschedule
from db import get_from_redis, set_schedule, set_routine, set_medications

from pydantic import BaseModel
from typing import List, Dict


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Meals(BaseModel):
    breakfast: int
    lunch: int
    dinner: int

class Routines(BaseModel):
    user_id: str
    wakeup_time: int
    bedtime: int
    meals: Meals

class Medication(BaseModel):
    name: str
    dosage: str
    time_period: str
    interactions: Dict[str, str]

class Medications(BaseModel):
    user_id: str
    data: List[Medication]

class FullSchedule(BaseModel):
    schedule: Dict[str, List[int]]
    warning_keys: List[Dict]
    warning_dict: Dict[str, Dict[str, str]]

class Feedback(BaseModel):
    user_id: str
    adherence: Dict[int, int]

class ImageList(BaseModel):
    images: List[str]
    userID: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/routine/{user_id}")
async def get_routine(user_id: str):
    results = get_from_redis(user_id)
    return results['routine']

@app.get("/medications/{user_id}")
async def get_medications(user_id: str):
    results = get_from_redis(user_id)
    return results['medications']

@app.get("/schedule/{user_id}")
async def get_schedule(user_id: str):
    results = get_from_redis(user_id)
    return results['schedule']

@app.post("/meds")
async def meds(image_list: ImageList):
    image_list = image_list
    image = image_list.images
    # step 1: get user_id
    user_id = image_list.userID
    results = get_from_redis(user_id)
    previous_medication = results['medications']
    print(previous_medication)

    # step 2: get new meds
    new_meds = picture_to_image(image)
    
    # step 3: combine new meds with previous meds
    all_medications = previous_medication + new_meds
    
    # step 4: get routines and create schedule
    routines = results['routine']
    new_schedule = create_schedule(all_medications, routines)
    print(new_schedule)
    # step 5: set schedule in redis 
    set_schedule(new_schedule, user_id)
    
    # step 6: set new meds in redis
    all_medications = json.dumps(all_medications)
    set_medications(all_medications, user_id)
    
    # step 7: return ok
    return Response(content=None, status_code=status.HTTP_200_OK)

@app.post("/reschedule")
async def reschedule(feedback: Feedback):
    user_id = feedback.user_id
    adherence = feedback.adherence
    # get schedule from redis
    results = get_from_redis(user_id)
    schedule = results['schedule']
    reschedule_schedule = reschedule(schedule, adherence)
    reschedule_schedule = json.dumps(reschedule_schedule)
    set_schedule(reschedule_schedule, user_id)
    return Response(content=None, status_code=status.HTTP_200_OK)

@app.post("/routines")
async def routines(routines: Routines):
    user_id = routines.user_id
    routine = {
        'wakeup_time': routines.wakeup_time,
        'bedtime': routines.bedtime,
        'meals': routines.meals.dict()
    }
    routine = json.dumps(routine)
    set_routine(routine, user_id)
    return Response(content=None, status_code=status.HTTP_200_OK)

@app.post("/medications")
async def medications(medications: Medications):
    # step 1: get user_id
    user_id = medications.user_id

    # step 3: get routines and create schedule
    routines = get_from_redis(user_id)['routine']

    # step 4: create schedule
    schedule = create_schedule(medications, routines)

    # step 2: get medications
    medications = json.dumps(medications.data)
    set_medications(medications, user_id)

    # step 5: set schedule in redis
    schedule = json.dumps(schedule)
    set_schedule(schedule, user_id)
    
    return Response(content=None, status_code=status.HTTP_200_OK)