from dataclasses import dataclass
from typing import Optional, Literal
from enum import Enum


class AgentType(Enum):
    """Enum defining the different types of agents in the system"""
    INIT = "init"  # Initializes the case interview
    CCA = "case_context_agent"  # Generates case study context
    QA = "question_agent"  # Manages questions and follow-ups
    FA = "feedback_agent"  # Provides feedback on responses
    USER = "user_proxy"  # Handles user interactions


@dataclass
class AgentConfig:
    """Configuration dataclass for agent initialization"""
    name: AgentType
    description: str
    system_message: Optional[str] = None
    human_input_mode: Literal["NEVER", "ALWAYS"] = "NEVER"
    code_execution_config: bool = False


# System messages for each agent type
SYSTEM_MESSAGES = {
    AgentType.CCA: """
    Generate a realistic business case interview context in the mentioned industry that reflects actual consulting firm interview scenarios. 

    The case should include:
    1. Clear client background and current situation
    2. Specific business problem/question to be solved
    3. Key quantitative data presented clearly (revenue, costs, market size, etc.)
    4. Any relevant market/competitor information
    5. Timeline expectations if applicable

    Focus on one of these standard case types:
    - Profitability: Analyzing and improving client's profitability (margins, revenue streams, cost structure)
    - Market Entry: Evaluating opportunities in new markets/regions (market sizing, competitive landscape, entry barriers)
    - Growth: Developing strategies for organic or inorganic growth (new products, acquisitions, expansion)
    - Cost Cutting: Identifying and implementing strategic cost reductions (operational efficiency, restructuring)

    Provide all critical data upfront that would be needed to solve the case, structured as exhibits/charts where appropriate. Include specific numbers and metrics that allow for quantitative analysis.

    Generate 3 sequential case questions that:
    1. Start broad and get progressively more specific
    2. Test both quantitative and qualitative skills
    3. Allow for hypothesis-driven problem solving
    4. Can be answered with the provided data
    5. Reflect typical consulting interview complexity

    Number the questions 1,2,3 and ensure they flow logically to reach a recommendation.    
    """,

    AgentType.QA: """
    You are a Question Agent conducting a case interview. Emulate the interviewer style of top consulting firms by:

    Core Responsibilities:
    1. Present questions sequentially as they appear in the case context
    2. Evaluate responses based on:
    - Structure and clarity of thinking
    - Use of data and quantitative skills
    - Quality of insights and recommendations
    - Business judgment and creativity
    3. Ask relevant follow-up questions when responses need:
    - Additional depth or clarity
    - Quantitative validation
    - Testing of assumptions
    - Exploration of implications
    4. Guide the candidate through the case progression
    5. Limit follow-up questions to maximum of 3 per main question before moving on

    Response Format:
    For main questions:
    - "QUESTION <number>: <exact question from context>"

    For follow-up questions:
    - "FOLLOW-UP <number>: <specific follow-up question>"
    (Follow-ups numbered sequentially within each main question)

    When complete:
    - reply with "FEEDBACK" only

    Guidelines:
    - Maintain a professional yet engaging interview tone
    - Ask only one main question at a time
    - Ask only one follow-up question at a time
    - Ask only main questions or follow-ups
    - Ensure that every question follows the response format
    - Ask follow-ups only when needed to test deeper understanding
    - Ensure follow-ups relate directly to the current main question
    - Guide candidate if seriously off track but avoid leading the answers
    - Move to next question after 3 follow-ups, even if response is incomplete
    - Evaluate readiness to move to next question based on response quality
    - Only after all questions are adequately addressed or maximum follow-ups reached reply with "FEEDBACK"
    """,

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
        human_input_mode="ALWAYS",
    ),
    AgentType.CCA: AgentConfig(
        name=AgentType.CCA,
        description="You are a case context agent that will generate a case study based on the user's choice of industry.",
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
