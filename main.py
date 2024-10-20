from typing import Dict, List
from autogen import ConversableAgent
import autogen
import numpy as np
import sys
import os
import re
import json
import random



def fetch_case_study_data(case_study_title: str) -> Dict[str, List[str]]:
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

    entrypoint_agent_system_message = "You are an entry point agent and will converse with other agents."

    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
    entrypoint_agent = ConversableAgent("entrypoint_agent", 
                                        system_message=entrypoint_agent_system_message, 
                                        llm_config=llm_config)
    
    case_context_agent_system_message = "You are a case context agent that will retrieve a case study from database, only return the description of the case study to user for now."
    case_context_agent = ConversableAgent("case_context_agent", 
                                        system_message=case_context_agent_system_message, 
                                        llm_config=llm_config)
    
    entrypoint_agent.register_for_llm(name="fetch_case_study_data", description="Fetch a random case study data from data base")(fetch_case_study_data)
    case_context_agent.register_for_execution(name="fetch_case_study_data")(fetch_case_study_data)

    chat_results = entrypoint_agent.initiate_chats(
    [
        {
            "recipient": case_context_agent,
            "message": user_query,
            "max_turns": 2,
            "summary_method": "last_msg",
        },
    ])
    
    return

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query when executing main."
    main(sys.argv[1])