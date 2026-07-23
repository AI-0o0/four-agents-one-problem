import json
from dataclasses import dataclass

from langchain.tools import tool, ToolRuntime


@dataclass
class AgentContext:
    user_id: str


def _load_json_file(file_path: str, default):
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except FileNotFoundError:
        return default


@tool(
    "calculate_trip_cost",
    return_direct=False,
    description="Calculate the total trip cost for a booking."
)
def CalculateTripCost(booking_id: str) -> float:
    bookings = _load_json_file("shared/data/bookings.json", {})
    return bookings.get(booking_id, {}).get("trip_cost")


@tool(
    "check_refund_eligibility",
    return_direct=False,
    description="Check whether a booking is eligible for a refund."
)
def CheckRefundEligibility(booking_id: str) -> bool:
    bookings = _load_json_file("shared/data/bookings.json", {})
    return bookings.get(booking_id, {}).get("refund_eligible")


@tool(
    "calculate_refund_amount",
    return_direct=False,
    description="Calculate the refund amount for a booking."
)
def CalculateRefundAmount(booking_id: str) -> float:
    bookings = _load_json_file("shared/data/bookings.json", {})
    return bookings.get(booking_id, {}).get("refund_amount")


@tool(
    "process_refund",
    return_direct=False,
    description="Process the refund for a booking."
)
def ProcessRefund(booking_id: str) -> dict:
    return {
        "booking_id": booking_id,
        "status": "Refund Processed",
    }


@tool(
    "calculate_compensation",
    return_direct=False,
    description="Calculate the compensation amount for a booking."
)
def CalculateCompensation(booking_id: str) -> float:
    bookings = _load_json_file("shared/data/bookings.json", {})
    return bookings.get(booking_id, {}).get("compensation")


@tool(
    "issue_travel_voucher",
    return_direct=False,
    description="Issue a travel voucher for a booking."
)
def IssueTravelVoucher(booking_id: str) -> dict:
    return {
        "booking_id": booking_id,
        "voucher": "$100 Travel Voucher",
    }


@tool(
    "compare_rebooking_cost",
    return_direct=False,
    description="Compare the original trip cost with a new rebooking cost."
)
def CompareRebookingCost(
    old_booking_id: str,
    new_booking_cost: float,
) -> str:
    bookings = _load_json_file("shared/data/bookings.json", {})

    old_cost = bookings.get(old_booking_id, {}).get("trip_cost", 0)

    if new_booking_cost > old_cost:
        return "Additional Payment Required"
    elif new_booking_cost < old_cost:
        return "Refund Difference"
    else:
        return "No Price Difference"
