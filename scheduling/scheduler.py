import re
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

def timestr(time):
    return f"{time // 60:02d}:{time % 60:02d}"

def parse_periods(time_period, routines, nlp=nlp):
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

def initializa(medications, routines):
    model = cp_model.CpModel()
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
                interaction_warnings.append((med1, med2))

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
        return return_schedule, interaction_warnings
    else:
        print('no solution found for the given constraints.')

def flatten_records(adherence_record):
    flat_record = {}
    for _, times in adherence_record.items():
        for time, adherence in times.items():
            flat_record[time] = adherence
    return flat_record

def timegen(time, adherence, mean, std):
    mean_shift = -1 * mean if adherence == -1 else mean if adherence == 1 else 0
    std_dev = std if (adherence == -1 or adherence == 1) else 0
    new_time = int(np.random.normal(time + mean_shift, std_dev))
    new_time = (new_time // 15) * 15 + (15 if new_time % 15 > 7 else 0)
    new_time = max(0, min(new_time, 1440 - 15))
    return new_time

def reschedule(adherence_record):
    flattened_records = flatten_records(adherence_record)

    adjusted_times = {}
    for time, adherence in flattened_records.items():
        new_time = timegen(time, adherence, 15, 15)
        adjusted_times[time] = new_time

    new_schedule = {}
    for drug, times in adherence_record.items():
        new_schedule[drug] = [adjusted_times[time] for time in times]

    return new_schedule

# # %% sample
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
#         'time_period': 'before bed',
#         'interactions': ['drug c']
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

# schedule, warnings = create_schedule(medications, routines)

# adherence_record = {
#     'drug a': {450: 1, 690: 0, 930: 1, 1170: -1},
#     'drug b': {1290: 0},
#     'drug c': {450: 1, 1290: 0}
# }

# reschedule(adherence_record)