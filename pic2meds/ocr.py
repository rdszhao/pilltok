from googleapiclient.discovery import build
import os
from io import BytesIO
from google.colab import files
from base64 import b64encode

# Construct the Vision API service object
api_key = "AIzaSyB2TiyCwOmhJvCtfrGDVQhgK5pY4fr7zVc"
service = build('vision', 'v1', developerKey=api_key)

# Specify the path to your folder on Google Drive that contains the images
input_folder_path = '../data/pill_images/'

# Specify the path to your folder on Google Drive where you want to save the results
output_folder_path = '../data/medicine_text_files'

# List files in the input directory
image_files = os.listdir(input_folder_path)

# Function to call the Vision API with an image file
def detect_text(image_path):
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

    # Output filename is the same as the input name but with a .txt extension
    output_file_name = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
    output_file_path = os.path.join(output_folder_path, output_file_name)

    # Write the first text annotation (which is typically the whole text) to the file
    with open(output_file_path, 'w') as output_file:
        for result in response['responses']:
            text_annotations = result.get('textAnnotations', [])
            if text_annotations:
                output_file.write(text_annotations[0]['description'])


# Process each image and save the results in the output directory
for image_file in image_files:
    file_path = os.path.join(input_folder_path, image_file)

    # Skip directories, process files
    if os.path.isfile(file_path):
        detect_text(file_path)
    else:
        print(f"Skipping directory: {file_path}")

