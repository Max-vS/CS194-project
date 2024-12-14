from dataclasses import dataclass
from typing import Optional, Literal
from enum import Enum


class AgentType(Enum):
    INIT = "init"
    CCA = "case_context_agent"
    QA = "question_agent"
    FA = "feedback_agent"
    USER = "user_proxy"


@dataclass
class AgentConfig:
    name: AgentType
    description: str
    system_message: Optional[str] = None
    human_input_mode: Literal["NEVER", "ALWAYS"] = "NEVER"
    code_execution_config: bool = False


# System messages for each agent type
SYSTEM_MESSAGES = {
    AgentType.CCA: """
    Generate a case study interview context in the Technology industry. 
    Make sure to provide statistics about the company necessary to solve the question (i.e. income statement, balance sheet, or cash flow if needed). 
    Focus on one of the four case types: 
    - Profitability: how to restore client's profitability
    - Market Entry: how to enter a new market / region
    - Growth: creating a growth strategy for a client
    - Cost cutting: how to reduce costs strategically 
    After generating the context generate 3 case study questions concerning the context and the company. Number the questions with 1,2,3.""",

    AgentType.QA: """You are a Question Agent responsible for managing the flow of questions during a case interview.

    Your tasks:
    1. Ask questions in sequential order from the case context
    2. Evaluate user responses and determine if follow-up questions are needed
    3. Track the progress through all questions

    Response Format:
    - For main questions: Reply with 'QUESTION <number>: <question text from context>'
    - For follow-up questions: Reply with 'FOLLOW-UP <number>: <follow-up question>'
    The follow-up number restarts at 1 for each main question
    - When all questions are completed: Reply with 'FEEDBACK'

    Guidelines:
    - Always present questions in the exact order they appear in the context
    - Follow-up questions should only be asked if the user's response needs clarification
    - Each main question can have multiple follow-ups, numbered sequentially
    - Follow-up questions must be relevant to the current main question's context
    - After all main questions and necessary follow-ups are complete, respond with 'FEEDBACK'""",

    AgentType.FA: """As the feedback agent, provide feedback on the user's responses to the questions based on the context provided in the case study."""
}

AGENT_CONFIGS = {
    AgentType.INIT: AgentConfig(
        name=AgentType.INIT,
        description="You are the initializer agent that will start the chat by generating a case study context.",
    ),
    AgentType.USER: AgentConfig(
        name=AgentType.USER,
        description="User proxy agent for handling human interactions",
        human_input_mode="ALWAYS"
    ),
    AgentType.CCA: AgentConfig(
        name=AgentType.CCA,
        description="You are a case context agent that will generate a case study based on user's choice of industry.",
        system_message=SYSTEM_MESSAGES[AgentType.CCA],
    ),
    AgentType.QA: AgentConfig(
        name=AgentType.QA,
        description="You are a question agent that will generate questions.",
        system_message=SYSTEM_MESSAGES[AgentType.QA],
    ),
    AgentType.FA: AgentConfig(
        name=AgentType.FA,
        description="You are a feedback agent that will provide feedback.",
        system_message=SYSTEM_MESSAGES[AgentType.FA],
    )
}
