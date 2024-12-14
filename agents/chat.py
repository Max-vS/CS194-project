from typing import Dict
from autogen import GroupChat, GroupChatManager
from config.settings import LLM_CONFIG
from .agent_configs import AgentType

def create_group_chat(agents: Dict[AgentType, any]):
    def state_transition(last_speaker, groupchat: GroupChat):
        messages = groupchat.messages

        if last_speaker is agents[AgentType.INIT]:
            return agents[AgentType.CCA]
        elif last_speaker is agents[AgentType.CCA]:
            return agents[AgentType.QA]
        elif last_speaker is agents[AgentType.QA]:
            if "FEEDBACK" in messages[-1]["content"].upper():
                return agents[AgentType.FA]
            else:
                return agents[AgentType.USER]
        elif last_speaker is agents[AgentType.USER]:
            return agents[AgentType.QA]
        elif last_speaker is agents[AgentType.FA]:
            return None

    groupchat = GroupChat(
        agents=list(agents.values()),
        messages=[],
        max_round=20,
        speaker_selection_method=state_transition,
    )

    return GroupChatManager(groupchat=groupchat, llm_config=LLM_CONFIG) 