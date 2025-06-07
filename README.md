# talentscout_hiring_assistant
## Project Overview
A basic chatbot for screening tech candidates, built with Streamlit and xAI's Grok API. It collects candidate details, generates technical questions based on their tech stack, and saves data securely.

## Installation Instructions

Clone the repository: git clone https://github.com/yourusername/talentscout-hiring-assistant.git
Create a virtual environment: python -m venv venv
Activate it: source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows)
Install dependencies: pip install -r requirements.txt
Copy .env.example to .env and add your xAI API key.
Run the app: streamlit run app.py

## Usage Guide

Open the app in your browser.
Provide details (name, email, etc.) when asked.
List your tech stack and answer technical questions.
Type "exit" to end the conversation.

## Technical Details

Language: Python
Libraries: Streamlit, xAI SDK, python-dotenv
LLM: Grok (xAI API)
Structure: Modular with separate files for UI, chatbot logic, prompts, and data handling.

## Prompt Design

Greeting: Introduces the chatbot and asks for the candidate’s name.
Info Gathering: Collects details one at a time.
Question Generation: Creates 3 tech-specific questions.
Fallback: Handles unclear inputs.
End: Summarizes and closes the conversation.

## Challenges & Solutions

Challenge: Keeping conversation context.
Solution: Store and pass conversation history to the LLM.


Challenge: Generating relevant questions.
Solution: Use tech stack in prompt for tailored questions.


Challenge: Data privacy.
Solution: Save anonymized data to a JSON file.

