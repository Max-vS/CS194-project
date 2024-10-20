# agents/question_agent.py

class QuestionAgent:
    def determine_follow_up(self, question, response):
        # Simple logic: if the response contains 'improve', ask for elaboration
        if "improve" in response.lower():
            return "Can you elaborate on how the company should implement those improvements?"
        return None
