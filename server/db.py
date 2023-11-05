import os
import json
import random
import redis


r = redis.Redis(
	host=os.environ.get('REDIS_HOST'),
	port=os.environ.get('REDIS_PORT'),
	password=os.environ.get('REDIS_PASSWORD')
)

# def send_to_redis(schedule: str, routine: str, adherence: str, user_id: int) -> bool:
# 	try:
# 		r.set(user_id + ':schedule', schedule)
# 		r.set(user_id + ':routine', routine)
# 		r.set(user_id + ':medications', medications)
# 		return True
# 	except Exception as e:
# 		print(e)
# 		return False

def set_schedule(schedule: str, user_id: int) -> bool:
	try:
		r.set(user_id + ':schedule', schedule)
		return True
	except Exception as e:
		print(e)
		return False

def set_routine(routine: str, user_id: int) -> bool:
	try:
		r.set(user_id + ':routine', routine)
		return True
	except Exception as e:
		print(e)
		return False

def set_medications(medications: str, user_id: int) -> bool:
	try:
		r.set(user_id + ':medications', medications)
		return True
	except Exception as e:
		print(e)
		return False

def get_from_redis(user_id: int) -> dict:
    return_dict = {}

    schedule = r.get(f"{user_id}:schedule")
    return_dict['schedule'] = json.loads(schedule) if schedule is not None else {}

    routine = r.get(f"{user_id}:routine")
    return_dict['routine'] = json.loads(routine) if routine is not None else {}

    medications = r.get(f"{user_id}:medications")
    return_dict['medications'] = json.loads(medications) if medications is not None else []

    return return_dict