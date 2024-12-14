import sys
from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent

from agents import CustomUserProxy
from config.settings import LLM_CONFIG
from data.system_messages import case_context_agent_sys_msg, question_agent_sys_msg, feedback_agent_sys_msg

initializer = UserProxyAgent(
    name="init",
    description="You are the initializer agent that will start the chat by generating a case study context.",
    llm_config=LLM_CONFIG,
    human_input_mode="NEVER",
    code_execution_config=False,
    function_map=None,
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)

case_context_agent = AssistantAgent(
    name="case_context_agent",
    description="You are a case context agent that will generate a case study based on user's choice of industry.",
    system_message=case_context_agent_sys_msg,
    llm_config=LLM_CONFIG,
    human_input_mode="NEVER",
    code_execution_config=False,
    function_map=None,
)

question_agent = AssistantAgent(
    name="question_agent",
    description="You are a question agent that will generate a case study based on user's choice of industry.",
    system_message=question_agent_sys_msg,
    llm_config=LLM_CONFIG,
    human_input_mode="NEVER",
    code_execution_config=False,
    function_map=None,
)

feedback_agent = AssistantAgent(
    name="feedback_agent",
    description="You are a feedback agent that will provide feedback on the user's performance in answering the questions of the specific case study.",
    system_message=feedback_agent_sys_msg,
    llm_config=LLM_CONFIG,
    human_input_mode="NEVER",
    code_execution_config=False,
    function_map=None,
)


def state_transition(last_speaker, groupchat: GroupChat):
    messages = groupchat.messages

    if last_speaker is initializer:
        return case_context_agent

    elif last_speaker is case_context_agent:
        return question_agent

    elif last_speaker is question_agent:
        if "FEEDBACK" in messages[-1]["content"].upper():
            return feedback_agent
        else:
            return user_proxy

    elif last_speaker is user_proxy:
        return question_agent

    elif last_speaker is feedback_agent:
        return None


groupchat = GroupChat(
    agents=[initializer, user_proxy, case_context_agent,
            question_agent, feedback_agent],
    messages=[],
    max_round=20,
    speaker_selection_method=state_transition,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=LLM_CONFIG)


def main(user_query: str):

    initializer.initiate_chat(
        manager,
        message="Start the chat by generating a case study context.",
    )


if __name__ == "__main__":
    assert len(
        sys.argv) > 1, "Please ensure you include a query when executing main."
    main(sys.argv[1])
