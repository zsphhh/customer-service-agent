import json, uuid
from datetime import datetime
from langchain_core.messages import HumanMessage
from ..utils.state import AgentState
from ..main import llm

def ticket_classifier(state: AgentState) -> AgentState:
    prompt = f"""生成工单JSON：{{"issue":"摘要","category":"类别","department":"部门","priority":"高/中/低","description":"描述"}}
用户输入：{state['user_input']}"""
    resp = llm.invoke([HumanMessage(content=prompt)]).content
    try:
        info = json.loads(resp)
    except:
        info = {"issue":"未知","category":"其他","department":"客服部","priority":"中","description":state["user_input"]}
    ticket_id = f"TK-{uuid.uuid4().hex[:8].upper()}"
    ticket = {**info, "ticket_id": ticket_id, "status": "open", "created_at": datetime.now().isoformat()}
    print(f"[工单] {ticket_id} → {info.get('department')}")
    return {**state, "ticket": ticket, "stage": "ticket_create"}

def cross_department_handler(state: AgentState) -> AgentState:
    ticket = state["ticket"]
    dept = ticket.get("department", "客服部")
    resolutions = {
        "售后部": "退货已通过，回寄单号：SF1234567890",
        "物流部": "包裹已重新派送，今日达",
        "质检部": "质量问题确认，换新处理",
        "技术部": "账户已修复，请重试登录",
        "财务部": "退款原路返回，1-3日到账",
        "客服部": "专员2小时内电话联系您"
    }
    resolution = resolutions.get(dept, "已处理完毕")
    ticket.update({"status": "resolved", "resolved_at": datetime.now().isoformat(), "resolution": resolution})
    return {**state, "ticket": ticket, "resolution": resolution, "stage": "ticket_resolve"}