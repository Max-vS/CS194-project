# agents/question_agent.py

import os
from autogen import UserProxyAgent, AssistantAgent

class QuestionAgent:
    def __init__(self):
        self.llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
        self.user_proxy = UserProxyAgent(
            name="User_Proxy",
            code_execution_config={"use_docker": False},
            human_input_mode="NEVER",
            default_auto_reply="",
            is_termination_msg=lambda x: True,
        )
        self.question_agent_generated = AssistantAgent(
            name="Question_Agent",
            system_message=(
                "You are a Question Agent responsible for determining if the process should proceed to the next question "
                "or ask a follow-up question based on the user's response. If the response is sufficient, reply with "
                "'TERMINATE'. If clarification is needed, generate a concise follow-up question. Ensure follow-ups are "
                "logical and relevant to the context of the original question and case."
            ),
            llm_config=self.llm_config,
            human_input_mode="ALWAYS",
            code_execution_config=False,
            function_map=None,
            is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
        )
        self.question_agent_generated.description = ("Evaluate the user response to given question and decide whether to proceed or ask follow-up questions.")


    def evaluate_response(self, context, question, user_response):
        qa_msg = (
            f"The Case interview context is as follows: {context}. "
            f"The user was asked: {question}. "
            f"Their response was: {user_response}. "
            "Should we proceed to the next main question, or do you need clarification?"
            "If clarification is needed, generate a concise follow-up question."
            "If their response is sufficient, reply with 'TERMINATE'."
            "If no response is made from the user, respond with 'No response was received, can you elaborate?'"
        )
        qa_result = self.user_proxy.initiate_chat(
            self.question_agent_generated,
            message=qa_msg,
            code_execution_config=False,
            max_turns=1,
        )

        # Check if chat_history has enough entries
        if not qa_result.chat_history or len(qa_result.chat_history) < 2:
            print("No response from QuestionAgent or insufficient chat history.")
            return {"followup_question": "No response received, please need to speak up!", "terminate": False}
        
        # Parse result from Question Agent
        ### Example response:
        ### ChatResult(
            # chat_id=None, 
            # chat_history=[{'content': "The Case interview context is as follows: **Case Study Context:**\n\nCompany: Artistry Collective\n\nOverview: Artistry Collective is a mid-sized arts and design firm specializing in custom artworks, design exhibitions, and public art installations. Founded in 2010, the company has established a reputation for innovative design solutions, catering primarily to both private clients and corporate entities.\n\nCurrent Situation: In recent years, Artistry Collective has struggled to maintain profitability despite a strong client base and a growing portfolio. Over the past two years, revenue has steadily increased, but so have costs associated with materials, labor, and project management. The firm currently employs 50 staff and has recently expanded its services to include digital design and virtual exhibitions in response to the growing digital market.\n\n**Financial Statistics:**\n- Annual Revenue: $3 million \n- Gross Margin: 45%\n- Operating Expenses: $1.4 million\n- Net Income Last Year: $150,000 \n- Current Assets: $1.2 million \n- Total Liabilities: $800,000 \n- Cash Flow from Operations: $200,000 \n\nGiven the financial landscape, the company is seeking to restore its profitability and explore options for cost management without sacrificing creativity or employee morale.\n\n. The user was asked: \n\n**Questions:**\n\nWhat factors do you think have contributed to the decline in Artistry Collective's profitability despite increasing revenues? . Their response was: {'text': '', 'segments': [], 'language': 'en'}. Should we proceed to the next main question, or do you need clarification?If clarification is needed, generate a concise follow-up question.If their response is sufficient, reply with 'TERMINATE'.", 
                # 'role': 'assistant', 
                # 'name': 'User_Proxy'}], 
            # summary="The Case interview context is as follows: **Case Study Context:**\n\nCompany: Artistry Collective\n\nOverview: Artistry Collective is a mid-sized arts and design firm specializing in custom artworks, design exhibitions, and public art installations. Founded in 2010, the company has established a reputation for innovative design solutions, catering primarily to both private clients and corporate entities.\n\nCurrent Situation: In recent years, Artistry Collective has struggled to maintain profitability despite a strong client base and a growing portfolio. Over the past two years, revenue has steadily increased, but so have costs associated with materials, labor, and project management. The firm currently employs 50 staff and has recently expanded its services to include digital design and virtual exhibitions in response to the growing digital market.\n\n**Financial Statistics:**\n- Annual Revenue: $3 million \n- Gross Margin: 45%\n- Operating Expenses: $1.4 million\n- Net Income Last Year: $150,000 \n- Current Assets: $1.2 million \n- Total Liabilities: $800,000 \n- Cash Flow from Operations: $200,000 \n\nGiven the financial landscape, the company is seeking to restore its profitability and explore options for cost management without sacrificing creativity or employee morale.\n\n. The user was asked: \n\n**Questions:**\n\nWhat factors do you think have contributed to the decline in Artistry Collective's profitability despite increasing revenues? . Their response was: {'text': '', 'segments': [], 'language': 'en'}. Should we proceed to the next main question, or do you need clarification?If clarification is needed, generate a concise follow-up question.If their response is sufficient, reply with ''.", 
            # cost={
                # 'usage_including_cached_inference': {'total_cost': 0}, 
                # 'usage_excluding_cached_inference': {'total_cost': 0}}, 
                # human_input=[])
        agent_response = qa_result.chat_history[1]["content"]        
        
        if "TERMINATE" in agent_response.upper():
            return {"followup_question": None, "terminate": True}
        return {"followup_question": agent_response, "terminate": False}
    
    