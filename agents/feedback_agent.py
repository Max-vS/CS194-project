# agents/feedback_agent.py

import os
from autogen import UserProxyAgent, AssistantAgent

class FeedbackAgent:
    def __init__(self):
        self.llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
        self.user_proxy = UserProxyAgent(
            name="User_Proxy",
            code_execution_config={"use_docker": False},
            human_input_mode="NEVER",
            default_auto_reply=None,
            is_termination_msg=lambda x: True,
        )
        
        # using AssistantAgent because it never requires human input
        self.feedback_agent = AssistantAgent(
            name="Feedback_Agent",
            system_message="As the feedback agent, provide feedback on the user's responses to the questions based on the context provided in the case study.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
        )
        self.feedback_agent.description = "Provide feedback based on user's responses."
    
    
    def provide_feedback(self, interview_log):
        log_string = "\n".join(interview_log)
        fa_msg = (
            "Provide feedback on the user's responses based on the questions asked. "
            f"Interview log:\n {log_string} "
        )

        fa_result = self.user_proxy.initiate_chat(
            self.feedback_agent,
            message=fa_msg,
            code_execution_config=False,
            max_turns=1,
        )

        feedback_message = fa_result.chat_history[1]["content"]
        print(f"\nFeedback Summary:\n{feedback_message}")
        return feedback_message