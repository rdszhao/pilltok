import re
import json
import numpy as np
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


def timestr(time: int) -> str:
    return f"{time // 60:02d}:{time % 60:02d}"

def parse_periods(time_period: str, routines: dict, nlp) -> list:
    doc = nlp(time_period)
    matcher = Matcher(nlp.vocab)

    # define the pattern for "every x hours"
    pattern_hours = [
        {'LOWER': 'every'},
        {'IS_DIGIT': True, 'OP': '+'},
        {'LOWER': 'hours'}
    ]
    matcher.add('EVERY_X_HOURS', [pattern_hours])

    # define the pattern for "x times a day"
    pattern_times_a_day = [
        {'IS_DIGIT': True, 'OP': '+'},
        {'LOWER': 'times'},
        {'LOWER': 'a'},
        {'LOWER': 'day'}
    ]
    matcher.add('X_TIMES_A_DAY', [pattern_times_a_day])

    matches = matcher(doc)
    dosage_times = []

    start_time = routines['wakeup_time'] + 30
    end_time = routines['bedtime'] - 30

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        if string_id == 'EVERY_X_HOURS':
            hours = int(span[1].text)
            intervals = np.arange(start_time, end_time, hours * 60)
            dosage_times.extend(intervals.tolist())
        elif string_id == 'X_TIMES_A_DAY':
            times = int(span[0].text)
            # calculate the interval in minutes between each dose
            interval = (end_time - start_time) // (times - 1)
            intervals = [start_time + i * interval for i in range(times)]
            dosage_times.extend(intervals)

    # handle qualitative times like "before bed" or "in the morning"
    lower_time_period = time_period.lower()
    if 'bed' in lower_time_period:
        bedtime_dose = routines['bedtime'] - 30  # assuming 30 mins before bed
        if bedtime_dose >= start_time:  # ensure it fits within the routine times
            dosage_times.append(bedtime_dose)
    if 'morning' in lower_time_period:
        morning_dose = start_time  # use the start_time, which is wakeup time plus buffer
        dosage_times.append(morning_dose)

    # convert entity times to the number of minutes since midnight
    for ent in doc.ents:
        if ent.label_ == 'TIME':
            time_str = ent.text.lower().replace('.', '')
            is_pm = 'pm' in time_str
            nums = [int(num) for num in re.findall(r'\d+', time_str)]
            hour = nums[0]
            minute = nums[1] if len(nums) > 1 else 0
            if hour < 12 and is_pm:
                hour += 12
            time_in_mins = hour * 60 + minute

            if routines['wakeup_time'] <= time_in_mins < routines['bedtime']:
                dosage_times.append(time_in_mins)

    # Deduplicate and sort times, making sure they are within the wakeup and bedtime
    valid_dosage_times = sorted(set([t for t in dosage_times if routines['wakeup_time'] <= t < routines['bedtime']]))

    return valid_dosage_times

def split_medications_and_interactions(medications_list: list) -> tuple:
    new_medications = []
    interactions = {}

    for med in medications_list:
        interaction_details = med.pop('interactions', {})
        interactions[med['name']] = interaction_details
        med['interactions'] = list(interaction_details.keys())
        new_medications.append(med)

    return new_medications, interactions

# !! ENDPOINT !!
def create_schedule(medications: list, routines: dict) -> str:
    model = cp_model.CpModel()

    medications, med_warnings = split_medications_and_interactions(medications)
    medications_dict = {med['name']: med for med in medications}

    schedule_vars = {}
    interaction_vars = {}

    for med in medications:
        med_name = med['name']
        dosage_times = parse_periods(med['time_period'], routines, nlp)
        constrained_times = [t for t in dosage_times if routines['wakeup_time'] <= t < routines['bedtime']]
        med_vars = []
        for dose, time in enumerate(constrained_times):
            var_name = f"{med_name}_dose_{dose}"
            med_var = model.NewIntVar(time, time, var_name)
            med_vars.append(med_var)
        schedule_vars[med_name] = med_vars

    # interaction constraints
    for (med1, doses1), (med2, doses2) in itertools.combinations(schedule_vars.items(), 2):
        interactions = medications_dict[med1].get('interactions', []) + medications_dict[med2].get('interactions', [])
        if med2 in interactions or med1 in interactions:
            for var1, var2 in itertools.product(doses1, doses2):
                # boolean variable that is true if two drugs with an interaction are scheduled at the same time
                interaction_var = model.NewBoolVar(f'{var1.Name()}_{var2.Name()}_interaction')
                model.Add(var1 == var2).OnlyEnforceIf(interaction_var)
                model.Add(var1 != var2).OnlyEnforceIf(interaction_var.Not())
                interaction_vars[(var1, var2)] = interaction_var

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        warnings = []
        interaction_warnings = []
        for (var1, var2), interaction_var in interaction_vars.items():
            if solver.Value(interaction_var):
                med1 = var1.Name().split('_dose_')[0]
                med2 = var2.Name().split('_dose_')[0]
                warnings.append(f"Warning: {med1} and {med2} have an interaction and are scheduled together.")
                interaction_warnings.append({med1: med2})

        return_schedule = {}
        for med_name in schedule_vars.keys():
            return_schedule[med_name] = []
        for med_name, med_vars in schedule_vars.items():
            for dose_num, var in enumerate(med_vars):
                med_time = solver.Value(var)
                time_string = timestr(med_time)
                print(f"{med_name} dose {dose_num + 1} should be taken at {time_string}")
                return_schedule[med_name].append(med_time)

        for warning in warnings:
            print(warning)
        warning_keys = []
        for interaction in interaction_warnings:
            for key, val in interaction.items():
                if {key: val} not in warning_keys:
                    warning_keys.append({key: val})
        outputs = json.dumps({
            'schedule': return_schedule,
            'warning_keys': warning_keys,
            'warnings_dict': med_warnings,
            'medications_dict': medications
        }, indent=True)
        return outputs
        outputs = json.dumps({
            'schedule': return_schedule,
            'warning_keys': list(set(interaction_warnings)),
            'warnings_dict': med_warnings,
            'medications': medications
        }, indent=True)
        return outputs
    else:
        print('no solution found for the given constraints.')

# !! HELPER !!
def get_interaction_warning(interaction_pair: dict, warnings_dict: dict) -> str:
    drug1, drug2 = next(iter(interaction_pair.items()))
    return warnings_dict.get(drug1, {}).get(drug2, "no warning found.")

def timesample(time: int, adherence: int, mean: int, std: int) -> int:
    mean_shift = -1 * mean if adherence == -1 else mean if adherence == 1 else 0
    std_dev = std if (adherence == -1 or adherence == 1) else 0
    new_time = int(np.random.normal(time + mean_shift, std_dev))
    new_time = (new_time // 10) * 10 + (10 if new_time % 10 > 7 else 0)
    new_time = max(0, min(new_time, 1440 - 15))
    return new_time

def create_adherence_record(schedule: dict, adherences: dict) -> dict:
    adherence_record = {}
    for drug, times in schedule.items():
        adherence_record[drug] = {time: adherences[time] for time in times}
    return adherence_record

# !! ENDPOINT !!
def reschedule(schedule: dict, adherences: dict, mean=15, std=15) -> str:
    if type(schedule) is str:
        schedule = json.laods(schedule)
    if type(adherences) is str:
        adherences = json.laods(adherences)

    adherence_record = create_adherence_record(schedule, adherences)

    adjusted_times = {}
    for time, adherence in adherences.items():
        new_time = timesample(time, adherence, mean, std)
        adjusted_times[time] = new_time

    new_schedule = {}
    for drug, times in adherence_record.items():
        new_schedule[drug] = [adjusted_times[time] for time in times]

    return json.dumps(new_schedule, indent=True)

# # %% sample

# medications = [
#     {'name': 'ATENOLOL',
#     'dosage': '100 mg',
#     'time_period': 'TAKE 3 TIMES A DAY',
#     'interactions': {'ALPRAZOLAM': 'Alprazolam may decrease the excretion rate of Amoxicillin which could result in a higher serum level.',
#                     'AMOXICILLIN': 'Amoxicillin may decrease the excretion rate of Warfarin which could result in a higher serum level.'}},
#     {'name': 'AMOXICILLIN',
#     'dosage': '500 MG',
#     # 'time_period': 'TAKE 4 TIMES A DAY',
#     'time_period': 'TAKE 4 TIMES A DAY',
#     'interactions': {'WARFARIN': 'Amoxicillin may decrease the excretion rate of Warfarin which could result in a higher serum level.'}} ]
# 
# routines = {
#     'wakeup_time': 7 * 60,  # 7:00 am
#     'bedtime': 24 * 60,     # 10:00 pm
#     'meals': {
#         'breakfast': 8 * 60,
#         'lunch': 12 * 60,
#         'dinner': 18 * 60
#     }
# }

# # i want to take the schedule json string object and write it to a json file
# schedule = create_schedule(medications, routines)
# with open('ouput.json', 'w') as file:
#     file.write(schedule)
# # %%
# print(ss)
# schedule = create_schedule(medications, routines)
# ss = json.loads(schedule)
# print(ss)

# get_interaction_warning(ss['warning_keys'][0], ss['warnings_dict'])