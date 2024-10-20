# agents/entrypoint_agent.py

from .case_context_agent import CaseContextAgent
from .question_agent import QuestionAgent
from .feedback_agent import FeedbackAgent

class EntrypointAgent:
    def __init__(self):
        self.case_context_agent = CaseContextAgent()
        self.question_agent = QuestionAgent()
        self.feedback_agent = FeedbackAgent()
        self.questions = []
        self.answers = []

    def start_interview(self):
        # Initialize the case study and questions
        context, self.questions = self.case_context_agent.generate_case_study()
        return context, self.questions  # Return for Streamlit

    def handle_response(self, user_response):
        # Append the user response and handle follow-ups
        self.answers.append(user_response)
        follow_up = self.question_agent.determine_follow_up(self.questions[len(self.answers) - 1], user_response)
        return follow_up  # Return follow-up question if any

    def give_feedback(self):
        # Generate feedback using the Feedback Agent
        feedback = self.feedback_agent.generate_feedback(self.questions, self.answers)
        return feedback  # Return feedback for Streamlit
