from typing import Dict, List
from autogen import UserProxyAgent, ConversableAgent, AssistantAgent
from autogen import GroupChat, GroupChatManager
import autogen
import numpy as np
import sys
import os
import re
import json
import random
from dotenv import load_dotenv



def fetch_case_study_data() -> Dict[str, List[str]]:
    output = {}
    with open('data/data.json', 'r') as file:
        case_study_data = json.load(file)
    random_case_study = random.choice(case_study_data)
    output = {
        "title": random_case_study["title"],
        "description": random_case_study["description"],
        "questions": random_case_study["questions"]
    }
    return output


def main(user_query: str):
    load_dotenv()
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
    
    # case_context_agent_system_message = "You are a case context agent that will retrieve a case study from database, only return the description of the case study to user for now."
    # case_context_agent = ConversableAgent("case_context_agent", 
    #                                     system_message=case_context_agent_system_message, 
    #                                     llm_config=llm_config)

    ### Define different agents
    user_proxy = UserProxyAgent(
        name="User_Proxy",
        code_execution_config={"use_docker": False},
        human_input_mode="NEVER",
        default_auto_reply="",
        is_termination_msg=lambda x: True,
    )
    
    # using AssistantAgent because it never requires human input
    case_context_agent = AssistantAgent(
        name="Case_Context_Agent",
        system_message="You are a case context agent that will fetch a case study from database randomly by using the registered tool, return the description of the case study to user for now.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    case_context_agent_generate = AssistantAgent(
        name="Case_Context_Agent",
        system_message="You are a case context agent that will generate a case study based on user's choice of industry. Add TERMINATE at the very end when complete.",
        llm_config=llm_config,
        human_input_mode="NEVER",
        code_execution_config = False,
        function_map = None,
        is_termination_msg=lambda msg: "terminate" in msg["content"].lower(),
    )
    
    # using ConversableAgent
    question_agent = ConversableAgent(
        name="Question_Agent",
        system_message="You are a question agent, you will ask one question at a time and await user responses. If the current case study has provided questions, ask question from these given questions first.",
        llm_config=llm_config,
        human_input_mode="ALWAYS",
    )
    question_agent_generated = ConversableAgent(
        name="Question_Agent",
        system_message="""You are a question agent, a question will be asked to the interviewee and a response will be provided. If the interviewee's response is unclear, you can ask for follow up questions.
                        If a follow up question is needed, ask it. If not reply with: TERMINATE.""",
        llm_config=llm_config,
        human_input_mode="ALWAYS",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    )


    # using AssistantAgent because it never requires human input
    feedback_agent = AssistantAgent(
        name="Feedback_Agent",
        system_message="As the feedback agent, provide feedback on the user's responses to the questions based on the context provided in the case study.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # register tool functions
    case_context_agent.register_for_llm(name="fetch_case_study_data", description="Fetch a random case study data from data base")(fetch_case_study_data)
    case_context_agent.register_for_execution(name="fetch_case_study_data")(fetch_case_study_data)

    case_context_agent.description = "Retrieve a case study from our data."
    case_context_agent_generate.description = "Generate a case study based on user's choice of industry."
    question_agent.description = "Ask questions based on the case study."
    feedback_agent.description = "Provide feedback based on user's responses."

    # Initiate the Interview
    # Step 1: Obtain the Case Study: two options (1) Fetch from database, (2) Generate on the fly
    # (2)
    ### TODO: in the case of generate on the fly, we need user choice on a list of predetermined fields
    user_choice_of_field = "Rocketry"
    cca_msg = f"Generate a case study interview context in the {user_choice_of_field} industry. After generating the context, put a separator #$% and then generate the questions with separator #*# between each question. Limit to less than 6 questions."
    cca_result = user_proxy.initiate_chat(
        case_context_agent_generate,
        message=cca_msg,
        code_execution_config=False,
        max_turns=1,
        # summary_method="last_msg",
    )
    
    # print("\nchat_result:", cca_result)
    # print("\nagent.chat_messages:", cca_result.chat_history)
    # print("\nresponse:", cca_result.chat_history[1]["content"])
    context_and_questions = cca_result.chat_history[1]["content"].split("#$%")
    context = context_and_questions[0]
    questions = context_and_questions[1].split("#*#")
    questions_num = len(questions)
    
    ### TODO: Display context to user (in the final iteration we use TTS to convey with audio)
    
    # Step 2: QNA by User and Question_Agent
    interview_log = []
    response = []
    cnt = 0
    max_followups = 2  # Limit number of clarification questions per main question
    while cnt < questions_num:
        question = questions[cnt]
        followup_attempts = 0
        termination_flag = False
        print(f"Question {cnt + 1}: {question}")  # Display the question
        
        while not termination_flag and followup_attempts <= max_followups:
            interview_log.append(question)
            ### TODO: Play the audio of question to user here
            
            ### Get the user's response (simulated here)
            user_response = "I'm not sure... I think I could do A then B then C and make the company succeed."
            response.append(user_response)
            
            followup_question = user_proxy.initiate_chat(question_agent_generated, user_response)
            followup_msg = followup_question.chat_history[1]["content"]
            if "TERMINATE" in followup_msg.upper():  # Check for termination
                termination_flag = True
            elif followup_attempts < max_followups:  # Allow limited follow-ups
                question = followup_msg
                followup_attempts += 1
                print(f"Follow-up Question: {question}")
            else:  # Exceeded follow-up attempts, move to the next question
                print("Moving to the next question...")
                termination_flag = True
        
        cnt += 1
    
    # Feedback agent can be implemented here
    return

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query when executing main."
    main(sys.argv[1])