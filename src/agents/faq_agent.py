from langchain_core.messages import HumanMessage
from ..utils.state import AgentState
from ..knowledge.vector_store import KnowledgeBase
from ..main import llm
from collections import defaultdict

frequency_counter = defaultdict(int)
HIGH_FREQ_THRESHOLD = 3

def faq_agent(state: AgentState) -> AgentState:
    kb = KnowledgeBase()
    # 多轮上下文
    query = state["user_input"]
    if len(state["messages"]) >= 2:
        context_queries = [m["content"] for m in state["messages"][-4:] if m["role"] == "user"]
        query = " ".join(context_queries)

    docs = kb.search(query)
    if not docs:
        return {**state, "faq_answer": "转人工", "final_response": "转人工", "stage": "end"}

    context = "\n".join([d.page_content for d in docs])
    prompt = f"基于知识库回答用户问题（友好，≤150字）：\n知识库：{context}\n问题：{query}"
    answer = llm.invoke([HumanMessage(content=prompt)]).content

    frequency_counter[query] += 1
    return {**state, "faq_answer": answer, "final_response": answer, "stage": "end"}