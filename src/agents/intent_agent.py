import json
from langchain_core.messages import HumanMessage
from ..utils.state import AgentState
from ..main import llm  # 避免循环引用，实际可独立传入

def intent_classifier(state: AgentState) -> AgentState:
    history = "\n".join(
        [f"{'用户' if m['role']=='user' else '客服'}: {m['content']}" for m in state['messages'][-6:]]
    )
    prompt = f"""分析对话历史，判断意图：faq（常见问题）、complex（复杂需工单）、chitchat（闲聊）
返回JSON：{{"intent": "...", "reason": "..."}}

对话历史：
{history}
用户最新输入：{state['user_input']}"""
    response = llm.invoke([HumanMessage(content=prompt)]).content
    try:
        result = json.loads(response)
        intent = result.get("intent", "faq")
    except:
        intent = "faq"
    return {**state, "intent": intent, "stage": "intent"}