import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from src.utils.state import AgentState
from src.agents.intent_agent import intent_classifier
from src.agents.faq_agent import faq_agent
from src.agents.ticket_agent import ticket_classifier, cross_department_handler
from src.agents.satisfaction_agent import satisfaction_followup

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def route_after_intent(state: AgentState):
    intent = state["intent"]
    if intent == "faq":
        return "faq"
    elif intent == "complex":
        return "ticket_classify"
    else:
        return "clarify"

def route_faq(state: AgentState):
    return "ticket_classify" if "转人工" in state.get("faq_answer", "") else "end"

def clarify(state: AgentState):
    return {**state, "final_response": "我没有完全理解，请再描述一下？", "stage": "end"}

# 构建图
builder = StateGraph(AgentState)
builder.add_node("intent_classifier", intent_classifier)
builder.add_node("faq_agent", faq_agent)
builder.add_node("ticket_classifier", ticket_classifier)
builder.add_node("cross_dept", cross_department_handler)
builder.add_node("satisfaction_followup", satisfaction_followup)
builder.add_node("clarify", clarify)

builder.set_entry_point("intent_classifier")
builder.add_conditional_edges("intent_classifier", route_after_intent, {
    "faq": "faq_agent",
    "ticket_classify": "ticket_classifier",
    "clarify": "clarify"
})
builder.add_conditional_edges("faq_agent", route_faq, {
    "end": END,
    "ticket_classify": "ticket_classifier"
})
builder.add_edge("ticket_classifier", "cross_dept")
builder.add_edge("cross_dept", "satisfaction_followup")
builder.add_edge("satisfaction_followup", END)
builder.add_edge("clarify", END)

app = builder.compile()

if __name__ == "__main__":
    # 测试对话
    state = AgentState(
        user_input="", messages=[], intent=None, faq_answer=None,
        ticket=None, resolution=None, satisfaction=None,
        need_clarify=False, final_response=None, stage="init"
    )
    tests = [
        "如何退货？",
        "我的包裹一直没更新物流",
        "商品严重破损，我要投诉",
        "5"  # 模拟打分
    ]
    for inp in tests:
        state["user_input"] = inp
        state["messages"].append({"role": "user", "content": inp})
        print(f"用户：{inp}")
        result = app.invoke(state)
        state.update(result)
        print(f"客服：{state.get('final_response', '')}\n")