import re
import spacy
from spacy.matcher import Matcher
from ortools.sat.python import cp_model
import itertools

try:
    nlp = spacy.load('en_core_web_sm')
except:
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

def parse_time_period_with_spacy(time_period, routines, nlp=nlp):
    doc = nlp(time_period)
    matcher = Matcher(nlp.vocab)

    # pattern for "every x hours"
    pattern = [
        {'LOWER': 'every'},
        {'IS_DIGIT': True, 'OP': '+'},
        {'LOWER': 'hours'}
    ]
    matcher.add('EVERY_X_HOURS', [pattern])

    # pattern for "x times a day"
    pattern = [
        {'IS_DIGIT': True, 'OP': '+'},
        {'LOWER': 'times'},
        {'LOWER': 'a'},
        {'LOWER': 'day'}
    ]
    matcher.add('X_TIMES_A_DAY', [pattern])

    matches = matcher(doc)
    dosage_times = []

    # handle specific qualitative times like "before bed" or "in the morning"
    morning_dose_time = routines['wakeup_time'] + 30
    lower_time_period = time_period.lower()
    if 'bed' in lower_time_period:
        dosage_times.append(routines['bedtime'] - 30)  # assuming 30 mins before bed
    if 'morning' in lower_time_period:
        dosage_times.append(morning_dose_time)  # assuming 30 mins after waking up

    for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            if string_id == 'EVERY_X_HOURS':
            # if there is a morning dose, align "every x hours" to start at that time
                if morning_dose_time is not None:
                    hours = int(span[1].text)
                    interval_count = (routines['bedtime'] - morning_dose_time) // (hours * 60)
                    intervals = [morning_dose_time + i * (hours * 60) for i in range(interval_count + 1)]
                    dosage_times.extend(intervals)
            elif string_id == 'X_TIMES_A_DAY':
                times = int(span[0].text)
                if morning_dose_time is not None:
                    intervals = [morning_dose_time + i * (1440 // times) for i in range(times)]
                    dosage_times.extend(intervals)

    for ent in doc.ents:
        if ent.label_ == 'TIME':
            # convert ent to a number of minutes since midnight
            time_str = ent.text.lower().replace('.', '')
            is_pm = 'pm' in time_str
            nums = [int(num) for num in re.findall(r'\d+', time_str)]
            hour = nums[0]
            minute = nums[1] if len(nums) > 1 else 0
            if hour < 12 and is_pm:
                hour += 12
            time_in_mins = hour * 60 + minute
            dosage_times.append(time_in_mins)

    # deduplicate and sort times
    dosage_times = sorted(set(dosage_times))

    return dosage_times

def create_schedule(medications, routines):
    model = cp_model.CpModel()
    medications_dict = {med['name']: med for med in medications}

    schedule = {}
    for med in medications:
        dosage_times = parse_time_period_with_spacy(med['time_period'], routines)
        constrained_times = [t for t in dosage_times if routines['wakeup_time'] <= t < routines['bedtime']]
        for dose, time in enumerate(constrained_times):
            schedule[(med['name'], dose)] = model.NewIntVar(time, time, f"{med['name']}_dose_{dose}")

    # constraints for interactions between medications
    for (med1, dose1), (med2, dose2) in itertools.combinations(schedule.keys(), 2):
        if med2 in medications_dict[med1].get('interactions', []):
            model.Add(schedule[(med1, dose1)] != schedule[(med2, dose2)])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        return_schedule = {}
        for med, _ in schedule.keys():
            return_schedule[med] = []
        for (med, dose), var in schedule.items():
            med_time = solver.Value(var)
            time_string = f"{med_time // 60:02d}:{med_time % 60:02d}"
            print(f"{med} dose {dose + 1} should be taken at {time_string}")
            return_schedule[med].append(time_string)
        return return_schedule
    else:
        print('no solution found for the given constraints.')

# sample
# medications = [
#     {
#         'name': 'drug a',
#         'dosage': '200 mg',
#         'time_period': 'every 4 hours',
#         'interactions': ['drug b']
#     },
#     {
#         'name': 'drug b',
#         'dosage': '100 mg',
#         'time_period': 'before bed'
#     },
#     {
#         'name': 'drug c',
#         'dosage': '200 mg',
#         'time_period': 'once in the morning, once before bed'
#     }
# ]

# routines = {
#     'wakeup_time': 7 * 60,  # 7:00 am
#     'bedtime': 22 * 60,     # 10:00 pm
#     'meals': {
#         'breakfast': 8 * 60,
#         'lunch': 12 * 60,
#         'dinner': 18 * 60
#     }
# }

# schedule = create_schedule(medications, routines)