<h1 align="center">PillTok 💊</h1>

<p align="center">
  A cutting-edge application designed to revolutionize medication management.
</p>

## Overview 🌐

PillTok is a state-of-the-art application that empowers patients to effortlessly manage multiple medications. Leveraging camera technology, users can import prescriptions with ease. PillTok then generates personalized medication schedules, adjusts to user feedback, and provides critical interaction warnings for a comprehensive health management experience.

## Contributors 👨‍🔬👩‍💻

- [Bill Zhang](mailto:billzhangsc@gmail.com) 📧
- [Ray Zhao](mailto:rdszhao@gmail.com) 📧
- [Ryan Lee](mailto:13leeryan@gmail.com) 📧
- [Sathya Raminani](mailto:sat2400nr@gmail.com) 📧

## Table of Contents 📖

- [Overview](#overview-)
- [Contributors](#contributors-👨‍🔬👩‍💻)
- [Inspiration](#inspiration-💡)
- [Goals](#goals-🎯)
- [Built With](#built-with-🛠️)
- [Challenges](#challenges-🚧)
- [Accomplishments](#accomplishments-✨)
- [What We Learned](#what-we-learned-🎓)
- [What's Next](#whats-next-🔮)
- [How to Run](#how-to-run-🚀)

---

## Inspiration 💡

Fueled by the imperative to tackle medication non-adherence and interaction risks, PillTok aspires to streamline medication management, safeguard patient health, and economize healthcare costs. We champion healthcare accessibility for all, including the disabled, non-native English speakers, and those in remote locales, to ensure everyone can manage their health confidently and effortlessly.

## Goals 🎯

- 📸 Enable effortless prescription data uploads via photo capture.
- ⚠️ Identify and alert users to problematic prescription interactions.
- 📅 Craft user-centric weekly medication schedules based on individual routines.
- 📲 Send timely reminders and nudges to ensure adherence.
- 🔄 Adapt schedules in real-time based on user feedback.

## Built With 🛠️

- **Google Vision OCR**: For meticulous text parsing from prescription labels.
- **React & NextJS**: To create a dynamic and engaging frontend user experience.
- **FastAPI**: For robust, high-performance backend API services.
- **RedisCloud**: For swift and reliable database operations.

## Challenges 🚧

- Acquiring real prescription bottles for data accuracy.
- Mastering text extraction from the unique curvature of pill bottles.
- Engineering a multi-faceted scheduling algorithm for diverse medication regimens.
- Innovating a responsive system to update schedules based on user interactions.

## Accomplishments ✨

1. 🎯 Precision OCR implementation with Google Vision API.
2. 🛡️ Development of a thorough medication interaction checker.
3. 📆 Creation of a smart, adaptive scheduling system.
4. 🖥️ Deployment of a responsive, user-friendly interface with Next.js.
5. 🚀 FastAPI and RedisCloud integration for optimal backend performance.

## What We Learned 🎓

The development journey of PillTok imparted us with:

- The synergy of integrating technologies like Next.js, FastAPI, and RedisCloud into a seamless application.
- The complexities of building secure, capable backend services for intricate health data management.
- The finesse required for OCR text extraction from challenging surfaces.

## What's Next 🔮

- 🧠 Enhancing our computer vision algorithm for unparalleled text data precision.
- 🌍 Expanding accessibility with multi-language translation capabilities.
- 🤖 Crafting an AI-driven chatbot for personalized health guidance and user engagement.

## How to Run 🚀

1. **Clone the repository**:
   ```
   git clone [repository-url]
   ```
2. **Run Frontend**:
   ```
   cd frontend
   npm install
   npm start
   ```
3. **Run Backend**:
   ```
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

<div align="center">
  <sub>Built with ❤️ by the PillTok Team.</sub>
</div>
