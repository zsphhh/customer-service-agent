from ..utils.state import AgentState
from ..knowledge.vector_store import KnowledgeBase
from ..agents.faq_agent import frequency_counter, HIGH_FREQ_THRESHOLD
from ..main import llm
from langchain_core.messages import HumanMessage


def satisfaction_followup(state: AgentState) -> AgentState:
    # 反馈结果
    if state.get("ticket"):
        msg = f"工单{state['ticket']['ticket_id']}已处理：{state['resolution']}\n评分（1-5）："
    else:
        msg = state.get("faq_answer", "已解决")

    # 模拟满意度（生产环境应从用户输入提取）
    sat = 5
    try:
        sat = int(state["user_input"])
        if not 1 <= sat <= 5:
            sat = 5
    except:
        pass
    state["satisfaction"] = sat

    # 高频问题自动入库
    kb = KnowledgeBase()
    for query, count in list(frequency_counter.items()):
        if count >= HIGH_FREQ_THRESHOLD:
            faq_entry = llm.invoke([HumanMessage(content=f"将下句转化为标准FAQ：{query}")]).content
            kb.add(faq_entry)
            print(f"[知识库更新] 新增：{faq_entry}")
            frequency_counter[query] = 0

    final = f"{msg}\n感谢反馈！"
    return {**state, "final_response": final, "stage": "end"}