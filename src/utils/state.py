from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    user_input: str
    messages: List[dict]
    intent: Optional[str]
    faq_answer: Optional[str]
    ticket: Optional[dict]
    resolution: Optional[str]
    satisfaction: Optional[int]
    need_clarify: bool
    final_response: Optional[str]
    stage: str