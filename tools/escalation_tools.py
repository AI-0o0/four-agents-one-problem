from langchain.tools import tool


@tool(
    "escalate_to_human",
    return_direct=False,
    description="Escalate a customer case to a human support agent."
)
def escalate_to_human(case_id: str) -> dict:
    return {
        "status": "Escalated",
        "case_id": case_id,
        "message": "Case has been escalated to a human support agent.",
    }


@tool(
    "create_support_ticket",
    return_direct=False,
    description="Create a support ticket for a customer issue."
)
def create_support_ticket(
    customer_id: str,
    issue: str,
) -> dict:
    return {
        "ticket_id": f"TKT-{customer_id}",
        "customer_id": customer_id,
        "issue": issue,
        "status": "Open",
    }


@tool(
    "schedule_agent_callback",
    return_direct=False,
    description="Schedule a callback from a support agent."
)
def schedule_agent_callback(
    customer_id: str,
    phone: str,
    callback_time: str,
) -> dict:
    return {
        "customer_id": customer_id,
        "phone": phone,
        "callback_time": callback_time,
        "status": "Callback Scheduled",
    }


@tool(
    "notify_supervisor",
    return_direct=False,
    description="Notify a supervisor about an escalated case."
)
def notify_supervisor(case_id: str) -> dict:
    return {
        "case_id": case_id,
        "status": "Supervisor Notified",
    }


@tool(
    "log_escalation",
    return_direct=False,
    description="Log the reason for escalating a customer case."
)
def log_escalation(
    case_id: str,
    reason: str,
) -> dict:
    return {
        "case_id": case_id,
        "reason": reason,
        "status": "Logged",
    }
