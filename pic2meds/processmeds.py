from googleapiclient.discovery import build
import os
from base64 import b64encode
import sys
import requests
from dotenv import load_dotenv

# Function to call the Vision API with an image file
def detect_text_from_image(image, service):
    #content = b64encode(image).decode()
    content = image.decode()
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': content
            },
            'features': [{
                'type': 'TEXT_DETECTION'
            }]
        }]
    })
    response = service_request.execute()

    # Extract the first text annotation (which is typically the whole text)
    for result in response['responses']:
        text_annotations = result.get('textAnnotations', [])
        if text_annotations:
            return text_annotations[0]['description']
    return None


# Function to call the Vision API with an image file
def detect_text(image_path, service):
    with open(image_path, 'rb') as image_file:
        content = b64encode(image_file.read()).decode()

    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': content
            },
            'features': [{
                'type': 'TEXT_DETECTION'
            }]
        }]
    })
    response = service_request.execute()

    # Extract the first text annotation (which is typically the whole text)
    for result in response['responses']:
        text_annotations = result.get('textAnnotations', [])
        if text_annotations:
            return text_annotations[0]['description']
    return None


# Extract dosage information from labels
def extract_dosage(label_words):
  for i in range(len(label_words)):
    if label_words[i] == 'M':
      dose = label_words[i - 1] + " MG"

    elif label_words[i] in ['MG', 'MCG']:
      dose = label_words[i - 1] + " " + label_words[i]

    elif label_words[i] == '5MG':
       dose = '5 MG' 
  return dose

def extract_info(text, medicines):
    split_file_contents = text.split()
    #Parsing drug names
    for word in split_file_contents:
      if check_drug_in_rxnorm(word):
        if len(word) <= 2:
          continue

        else:
          medicines[word] = extract_dosage(split_file_contents)
          return True

    return False

def check_drug_in_rxnorm(drug_name):
    # URL for the RxNorm API concept search
    api_url = f'https://rxnav.nlm.nih.gov/REST/drugs.json?name={drug_name}'

    # Make the API request
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the 'drugGroup' key exists and if 'conceptGroup' is in the response
        if 'drugGroup' in data and 'conceptGroup' in data['drugGroup']:
            # Check if there are any RxNorm concepts for the drug name
            if data['drugGroup']['conceptGroup']:
                # If there are concepts, the drug name is recognized
                return True
            else:
                # If there are no concepts, the drug name is not recognized
                return False
        else:
            # If the 'conceptGroup' key is missing, the drug name is not recognized
            return False
    else:
        # If the request was not successful, print the error
        return False

#def pics2meds(image_list):

   # Construct the Vision API service object
#Functions to check a list of drugs for any interactions between them
#Contains a helper function to find the RXCUID for a string representing a drug
def get_rxcui(drug_name):
    """Get the RxNorm Concept Unique Identifier (RxCUI) for a drug."""
    api_url = f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        rxcui = data.get('idGroup', {}).get('rxnormId', [None])[0]
        return rxcui
    return None

def check_drug_interactions(drug_list):
    """Check for interactions between drugs in the provided list."""
    # Convert drug names to RxCUIs
    rxcuis = [get_rxcui(drug) for drug in drug_list]
    rxcuis = [rxcui for rxcui in rxcuis if rxcui is not None]  # Filter out any None values

    if len(rxcuis) < 2:
        return "Need at least two drugs to check for interactions."

    # Create a comma-separated string of RxCUIs
    rxcui_str = '+'.join(rxcuis)

    # Call the interaction API
    api_url = f'https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={rxcui_str}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        interaction_data = data.get('fullInteractionTypeGroup', [])

        if not interaction_data:
            return None

        interactions = []
        for group in interaction_data:
            for interaction_type in group.get('fullInteractionType', []):
                for interaction in interaction_type.get('interactionPair', []):
                    interactions.append({
                        'description': interaction.get('description')
                        #'severity': interaction.get('severity')
                        #'interaction': interaction.get('interactionConcept', [])
                    })
        return interactions
    else:
        return f"Error: {response.status_code}"
#Given the list of drugs find tuples of drugs
def get_drug_interacting_pairs(drug_list):
    """Return a list of tuples with drug pairs that have interactions."""
    interacting_pairs = []

    # Convert drug names to RxCUIs
    drug_rxcuis = {drug: get_rxcui(drug) for drug in drug_list}

    # Filter out drugs for which RxCUI was not found
    drug_rxcuis = {drug: rxcui for drug, rxcui in drug_rxcuis.items() if rxcui is not None}

    if len(drug_rxcuis) < 2:
        return interacting_pairs  # Cannot have interactions with less than two drugs

    # Create a comma-separated string of RxCUIs
    rxcui_str = '+'.join(drug_rxcuis.values())

    # Call the interaction API
    api_url = f'https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={rxcui_str}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        interaction_data = data.get('fullInteractionTypeGroup', [])

        for group in interaction_data:
            for interaction_type in group.get('fullInteractionType', []):
                for interaction_pair in interaction_type.get('interactionPair', []):
                    interacting_drugs = interaction_pair.get('interactionConcept', [])
                    if len(interacting_drugs) == 2:
                        # Extract the drug names from the interaction pair
                        drug_names = [
                            interacting_drugs[0].get('minConceptItem', {}).get('name'),
                            interacting_drugs[1].get('minConceptItem', {}).get('name')
                        ]
                        # Add the pair to the list if both names are found
                        if all(drug_names):
                            interacting_pairs.append(tuple(drug_names))
    return interacting_pairs

def get_medications(medications, interaction_dictionary, time_period):
  medication_dictionary = []

  for medication in medications.keys():
    curr_dictionary = {}
    curr_dictionary['name'] = medication
    curr_dictionary['dosage'] = medications[medication]
    curr_dictionary['time_period'] = time_period[medication]

    interactions = {}
    print('medication: /n',medication)
    for pair, description in interaction_dictionary.items():
      if pair[0].upper() == medication:
        interactions[pair[1].upper()] = description

    curr_dictionary['interactions'] = interactions

    medication_dictionary.append(curr_dictionary)

  return medication_dictionary

#Extract time period information for drugs
def extract_time_period(text):
  ending_words = ['BEDTIME','bedtime', 'DAILY', 'HOUR', 'LUNCH', 'BREAKFAST', 'DINNER', 'DAY']
  split_file_contents = text.split()

  for i in range(len(split_file_contents)):
    if split_file_contents[i] in ['Take','TAKE']:
      starting_index = i

    elif split_file_contents[i] in ending_words:
      ending_index = i

  return " ".join(split_file_contents[starting_index:ending_index + 1])

def get_interactions(interacting_pairs, interactions):
    # Extract the 'description' from each dictionary in the interactions list
    descriptions = [interaction['description'] for interaction in interactions]
    # Zip the interacting pairs with the corresponding descriptions
    return {k: v for k, v in zip(interacting_pairs, descriptions)}

# def get_interactions(interacting_pairs, interactions):
#   return {k: v for k, v in zip(interacting_pairs, interactions['description'])}

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Assuming detect_text, extract_info, get_drug_interacting_pairs, check_drug_interactions, get_interactions, extract_time_period are defined elsewhere

def picture_to_image(image_list):

    # Load the environment variables
    load_dotenv('../.env')
    api_key = os.getenv('GCP_API_KEY')
    service = build('vision', 'v1', developerKey=api_key)

    # Process each image and collect the results in a list
    text_results = []
    
    for image in image_list:
        # file_path = os.path.join(input_folder_path, image_file)
        text = detect_text_from_image(image,service)
        text_results.append(text)

    # Now text_results contains all the detected texts from the images
    medications = {}
    interactions = {}
    instructions = {}

    for text in text_results:
        extract_info(text, medications)
        medicine_names = list(medications.keys())
        instructions[medicine_names[len(medicine_names) - 1]] = extract_time_period(text)
    interacting_pairs = get_drug_interacting_pairs(medications.keys())
    interaction_descriptions = check_drug_interactions(medications.keys())
    interactions = get_interactions(interacting_pairs, interaction_descriptions)
    all_medicines = get_medications(medications,interactions,instructions)
    return all_medicines

def main():
    # Specify the path to your folder that contains the images
    input_folder_path = 'data/pill_images/'
    
# List files in the input directory
    image_files = os.listdir(input_folder_path)

    # Specify the path to your folder where you want to save the results
    output_folder_path = 'data/medicine_text_files'

    # Load the environment variables
    load_dotenv('../.env')
    api_key = os.getenv('GCP_API_KEY')
    service = build('vision', 'v1', developerKey=api_key)

    # Process each image and collect the results in a list
    text_results = []
    
    for image_file in image_files:
        file_path = os.path.join(input_folder_path, image_file)

        # Skip directories, process files
        if os.path.isfile(file_path):
            text = detect_text(file_path, service)
            if text:
                text_results.append(text)
        else:
            print(f"Skipping directory: {file_path}")
    # print('length of text results:',len(text_results))
    # # print(text_results)

    # interaction_descriptions_check = check_drug_interactions(['CLONIDINE','ATENOLOL'])
    # print(interaction_descriptions_check)

    # Now text_results contains all the detected texts from the images
    medications = {}
    interactions = {}
    instructions = {}

    for text in text_results:
        extract_info(text, medications)
        medicine_names = list(medications.keys())
        instructions[medicine_names[len(medicine_names) - 1]] = extract_time_period(text)
    # print(medications.keys())
    interacting_pairs = get_drug_interacting_pairs(medications.keys())
    #print('interacting pairs:\n',interacting_pairs)
    interaction_descriptions = check_drug_interactions(medications.keys())
    #print('interacting_descripion\n',interaction_descriptions)
    interactions = get_interactions(interacting_pairs, interaction_descriptions)
    #print('interactions:\n', interactions)
    all_medicines = get_medications(medications,interactions,instructions)
    print(all_medicines)

    # Here you would typically save the results to a file or database
    # For example, you could write the medications and instructions to a file
    # with open(os.path.join(output_folder_path, 'output.txt'), 'w') as f:
    #     f.write(str(medications))
    #     f.write(str(instructions))

if __name__ == "__main__":
    main()

# # Specify the path to your folder on Google Drive that contains the images
# input_folder_path = 'data/pill_images/'
# # List files in the input directory
# image_files = os.listdir(input_folder_path)

# # Specify the path to your folder on Google Drive where you want to save the results
# output_folder_path = 'data/medicine_text_files'

# load_dotenv('../.env')
# api_key = os.getenv('GCP_API_KEY')
# service = build('vision', 'v1', developerKey=api_key)

# # Process each image and collect the results in a list
# text_results = []

# for image_file in image_files:
#     file_path = os.path.join(input_folder_path, image_file)

#     # Skip directories, process files
#     if os.path.isfile(file_path):
#         text = detect_text(file_path)
#         if text:
#             text_results.append(text)
#     else:
#         print(f"Skipping directory: {file_path}")

# # Now text_results contains all the detected texts from the images
# medications = {}
# interactions = {}
# instructions = {}

# for text in text_results:
#     extract_info(text,medications)
#     print(medications)
#     interacting_pairs = get_drug_interacting_pairs(medications.keys())
#     interaction_descriptions = check_drug_interactions(medications.keys())
#     interactions = get_interactions(interacting_pairs, interaction_descriptions)
#     medicine_names = list(medications.keys())
#     print(medicine_names)
#     print('length of mednames-1:',len(medicine_names)-1)

#     instructions[medicine_names[len(medicine_names)-1]] = extract_time_period(text) 
#     #instructions[]

