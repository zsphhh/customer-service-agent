import sys
sys.path.insert(0, '.')
from src.main import app
from src.utils.state import AgentState

def test_basic_flow():
    state = AgentState(
        user_input="退货政策", messages=[],
        intent=None, faq_answer=None, ticket=None, resolution=None,
        satisfaction=None, need_clarify=False, final_response=None, stage="init"
    )
    state["user_input"] = "退货政策"
    state["messages"].append({"role": "user", "content": "退货政策"})
    result = app.invoke(state)
    assert result["intent"] == "faq"
    assert result["stage"] == "end" or "faq_answer" in result
    print("基础流程测试通过")