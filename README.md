# PillTok

## Overview

PillTok is an application that allows patients to easily manage multiple medications. It provides them with tools to easily import prescriptions into the app using just their camera. Once they've uploaded their data, it can create personalized medication schedules based on their routines and adjust them based on their feedback while provioding warnings on any potentially harmful interactions between prescriptions.


## Contributors

1.  [Bill Zhang](mailto:billzhangsc@gmail.com)
2.  [Ray Zhao](mailto:rdszhao@gmail.com)
3.  [Ryan Lee](mailto:13leeryan@gmail.com)
4.  [Sathya Raminani](mailto:sat2400nr@gmail.com)

## Table of Contents

- [PillTok](#pilltok)
  - [Overview](#overview)
  - [Contributors:](#contributors)
  - [Table of Contents](#table-of-contents)
  - [Inspiration](#inspiration)
  - [Goals](#goals)
  - [Built With](#built-with)
  - [Challenges](#challenges)
  - [Accomplishments](#accomplishments)
  - [What We Learned](#what-we-learned)
  - [What's Next](#whats-next)
  - [How to run](#how-to-run)
 
## Inspiration

Driven by the critical need to address medication non-adherence and the risks of drug interactions, our app aims to simplify medication management, enhance patient safety, and cut healthcare costs. Recognizing the disparities in healthcare access for the disabled, non-native English speakers, and those in remote areas, we're committed to delivering a solution that makes healthcare more inclusive and accessible to all. This app is our response to the urgent call for a healthcare system that supports patients comprehensively, ensuring that every individual can manage their health with confidence and ease.

## Goals

- Enable users to upload their prescription data just by taking a photo
- Identify any problematic interactions between patients' prescriptions
- Use doctor's instructions on the label as well as patient's daily routine to create a weekly medication schedule
- Send patient reminds/nudges based on medication schedule
- Adjust schedule based on user-reported adherence to schedule

## Built With

- Text on prescription bottle labels parsed using Google Vision OCR
- Frontend UI built with React and NextJS, displaying patient login and interface for tracking medication schedule
- API built with FastAPI due to its high performance
- Database schema built with RedisCloud due to its efficient caching capabilities

## Challenges

- Lack of actual labeled prescription pill bottles available online
- Parsing text from the cylindrical-shaped bottle
- Developing a scheduling algorithm for multiple medications taken at different times of day while accomodating the user's daily routine
- Developing algorithm to update scheduled medication times based on user adherence to schedule


## Accomplishments

1. Successfully implemented OCR functionality using Google Vision API, enabling users to extract text from images of pill bottles accurately.
2. Developed a comprehensive medication interaction checker that cross-references user-inputted drugs to identify potential adverse interactions.
3. Created a sophisticated scheduling system that not only reminds users to take their medications but also intelligently spaces out doses to avoid conflicts and maximize therapeutic effectiveness.
4. Designed and deployed a responsive, intuitive user interface using Next.js.
5. Leveraged FastAPI to build high-performance backend services that handle requests efficiently, coupled with RedisCloud caching to ensure quick data retrieval and minimal latency.

## What We Learned

Throughout the development of PillTok, our team learned:

- To integrate various technologies such as Next.js, FastAPI, and RedisCloud to create a cohesive and functional application.
- About creating robust and secure back-end services that can handle complex queries, such as checking for drug interactions and scheduling medications.
- About the intricacies of extracting text from images, especially from cylindrical surfaces like pill bottles.

## What's Next

- Improve on our computer vision algorithm to ensure even more accurate parsing of text data from labels
- Incorporate translation to make prescriptions more accessible to people of all backgrounds
- Develop an AI-powered chatbot that can provide personalized advice and answer health-related questions


## How to run

1. Clone the repository
2. Run Frontend
   1. 'cd server'
   2. 'npm install'
   3. 'npm start'
3. Run Backend
   1. 'cd server'
   2. 'pip install -r requirements.txt'
   3. 'pip start'

