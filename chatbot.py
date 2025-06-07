import os
from xai_sdk.client import Client
from prompts import GREETING_PROMPT, INFO_GATHERING_PROMPT, QUESTION_GENERATION_PROMPT, FALLBACK_PROMPT, END_CONVERSATION_PROMPT
from data_handler import DataHandler

class TalentScoutChatbot:
    def __init__(self):
        self.client = Client(api_key=os.getenv("XAI_API_KEY"))
        self.conversation_history = []
        self.candidate_info = {
            "full_name": None, "email": None, "phone": None, "experience": None,
            "positions": None, "location": None, "tech_stack": None
        }
        self.current_step = "greeting"
        self.info_fields = ["full_name", "email", "phone", "experience", "positions", "location", "tech_stack"]
        self.current_field_index = 0
        self.technical_questions = []
        self.data_handler = DataHandler()

    def get_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})

        if user_input.lower() in ["exit", "done", "finish"]:
            response = self.client.chat(END_CONVERSATION_PROMPT.format(conversation_history=self.conversation_history))
            self.data_handler.save_candidate(self.candidate_info)
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        if self.current_step == "greeting":
            response = self.client.chat(GREETING_PROMPT)
            self.current_step = "info_gathering"
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        if self.current_step == "info_gathering":
            return self.handle_info_gathering(user_input)
        elif self.current_step == "technical_questions":
            return self.handle_technical_questions(user_input)
        else:
            response = self.client.chat(FALLBACK_PROMPT.format(user_input=user_input, conversation_history=self.conversation_history))
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

    def handle_info_gathering(self, user_input):
        current_field = self.info_fields[self.current_field_index]
        prompt = INFO_GATHERING_PROMPT.format(conversation_history=self.conversation_history)
        response = self.client.chat(prompt)
        self.candidate_info[current_field] = user_input
        self.conversation_history.append({"role": "assistant", "content": response})
        self.current_field_index += 1
        if self.current_field_index >= len(self.info_fields):
            self.current_step = "technical_questions"
            self.generate_technical_questions()
            return self.technical_questions[0]
        return response

    def generate_technical_questions(self):
        tech_stack = self.candidate_info["tech_stack"]
        prompt = QUESTION_GENERATION_PROMPT.format(tech_stack=tech_stack, conversation_history=self.conversation_history)
        questions = self.client.chat(prompt)
        self.technical_questions = questions.split("\n")
        self.conversation_history.append({"role": "assistant", "content": questions})

    def handle_technical_questions(self, user_input):
        if len(self.technical_questions) > 1:
            self.technical_questions.pop(0)
            return self.technical_questions[0]
        else:
            response = self.client.chat(END_CONVERSATION_PROMPT.format(conversation_history=self.conversation_history))
            self.data_handler.save_candidate(self.candidate_info)
            self.conversation_history.append({"role": "assistant", "content": response})
            return response