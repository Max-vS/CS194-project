from typing import Dict, List
from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager
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

    # define different agents
    case_context_agent = ConversableAgent(
        name="Case_Context_Agent",
        system_message="You are a case context agent that will fetch a case study from database randomly by using the registered tool, return the description of the case study to user for now.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    question_context_agent = ConversableAgent(
        name="Question_Context_Agent",
        system_message="You are a question agent, you will ask one question at a time and await user responses. If the current case study has provided questions, ask question from these given questions first.",
        llm_config=llm_config,
        human_input_mode="ALWAYS",
    )

    feedback_agent = ConversableAgent(
        name="Feedback_Agent",
        system_message="You provide feedback on the user's responses to the questions based on the case study.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # register tool functions
    case_context_agent.register_for_llm(name="fetch_case_study_data", description="Fetch a random case study data from data base")(fetch_case_study_data)
    case_context_agent.register_for_execution(name="fetch_case_study_data")(fetch_case_study_data)

    case_context_agent.description = "Retrieve a case study from our data."
    question_context_agent.description = "Ask questions based on the case study."
    feedback_agent.description = "Provide feedback based on user's responses."

    # Set up group chat and manager
    group_chat = GroupChat(
        agents=[case_context_agent, question_context_agent, feedback_agent],
        messages=[],
        speaker_selection_method="manual", # since currently manager needs to converse with question agent multiple times
        max_round=6,
    )

    group_chat_manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
    )

    # begin the conversation
    initial_message = "Please start the case study interview with a case study."
    chat_result = case_context_agent.initiate_chat(
        group_chat_manager,
        message=initial_message,
        summary_method="reflection_with_llm",
    )

    return

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query when executing main."
    main(sys.argv[1])