# agents/case_context_agent.py

import os
from autogen import UserProxyAgent, ConversableAgent, AssistantAgent
from dotenv import load_dotenv

class CaseContextAgent:
    def __init__(self):
        self.llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
        self.user_proxy = UserProxyAgent(
            name="User_Proxy",
            code_execution_config={"use_docker": False},
            human_input_mode="NEVER",
            default_auto_reply="",
            is_termination_msg=lambda x: True,
        )
        self.case_context_agent_generate = AssistantAgent(
            name="Case_Context_Agent",
            system_message="You are a case context agent that will generate a case study based on user's choice of industry.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config = False,
            function_map = None,
            is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
        )
        
        self.case_context_agent_generate.description = "Generate a case study based on user's choice of industry."
    
    def generate_case(self, user_choice_of_industry):
        # WHEN: right as the interview is initiated
        # WHAT: generate case context based on user industry of interest
        cca_msg = f"""Generate a case study interview context in the {user_choice_of_industry} industry. 
                    Make sure to provide statistics about the company necessary to solve the question (i.e. income statement, balance sheet, or cash flow if needed). 
                    Focus on one of the four case types: 
                    - Profitability: how to restore client’s profitability
                    - Market Entry: how to enter a new market / region
                    - Growth: creating a growth strategy for a client
                    - Cost cutting: how to reduce costs strategically 
                    After generating the context, put a separator #$% and then generate the questions with separator "#*#" between each question. 
                    Limit to less than 3 questions. Remember, Use #*# between each question, but no numbering (i.e. 1,2,3)."""
        cca_result = self.user_proxy.initiate_chat(
            self.case_context_agent_generate,
            message=cca_msg,
            code_execution_config=False,
            max_turns=1,
            # summary_method="last_msg",
        )
        
        # parse the results
        context_and_questions = cca_result.chat_history[1]["content"].split("#$%")
        context = context_and_questions[0]
        questions = context_and_questions[1].split("#*#")
        questions_num = len(questions)
        
        return context, questions, questions_num
     