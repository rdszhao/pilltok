import os
import json
import random
from  dotenv import load_dotenv

load_dotenv('../.env')

r = redis.Redis(
	host=os.getenv['REDIS_HOST'],
	port=os.getenv['REDIS_PORT'],
	password=os.getenv['REDIS_PASSWORD']
)

def send_to_redis(schedule: str, routine: str, adherence: str, user_id: int) -> bool:
	try:
		r.set(user_id + ':schedule', schedule)
		r.set(user_id + ':routine', routine)
		r.set(user_id + ':medications', medications)
		return True
	except Exception as e:
		print(e)
		return False
	# r.set(user_id + ':schedule', json.dumps(schedule))
	# r.set(user_id + ':routine', json.dumps(routine))
	# r.set(user_id + ':adherence', json.dumps(adherence))

def get_from_redis(user_id: int) -> str:
	schedule = r.get(user_id + ':schedule')
	routine = r.get(user_id + ':routine')
	medications = r.get(user_id + ':medications')
	return_json = {
		'schedule': schedule,
		'routine': routine,
		'medications': medications
	}
	return_json = json.dumps(return_json)
	return return_json
	# schedule = json.loads(r.get(user_id + ':schedule'))
	# routine = json.loads(r.get(user_id + ':routine'))
	# adherence = json.loads(r.get(user_id + ':adherence'))
	# return schedule, routine, adherence