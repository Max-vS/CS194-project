"""
Agent factory module that centralizes agent creation with consistent configurations.
Supports both assistant and user proxy agent types.
"""

from agents import CustomUserProxy
from agents.agent_configs import AGENT_CONFIGS, AgentType
from autogen import AssistantAgent, UserProxyAgent
from config.settings import LLM_CONFIG

def create_agent(agent_type: AgentType):
    """
    Factory function that creates and configures agents based on their type.
    Returns either a CustomUserProxy or an appropriate AssistantAgent.
    """
    config = AGENT_CONFIGS[agent_type]
    
    if agent_type == AgentType.USER:
        return CustomUserProxy()
    
    agent_class = UserProxyAgent if agent_type == AgentType.INIT else AssistantAgent
    
    return agent_class(
        name=config.name.value,
        description=config.description,
        system_message=config.system_message,
        llm_config=LLM_CONFIG,
        human_input_mode=config.human_input_mode,
        code_execution_config=config.code_execution_config,
    ) 