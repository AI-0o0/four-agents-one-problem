import json
from langchain.tools import tool


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
    "get_flight_status",
    return_direct=False,
    description="Get the current status of a flight."
)
def get_flight_status(flight_id: str) -> str:
    flights = _load_json_file("shared/data/flights.json", {})
    return flights.get(flight_id, {}).get("status")


@tool(
    "get_delay_duration",
    return_direct=False,
    description="Get the delay duration of a flight in minutes."
)
def get_delay_duration(flight_id: str) -> int:
    flights = _load_json_file("shared/data/flights.json", {})
    return flights.get(flight_id, {}).get("delay_minutes")


@tool(
    "check_disruption_reason",
    return_direct=False,
    description="Get the reason for a flight disruption or delay."
)
def check_disruption_reason(flight_id: str) -> str:
    flights = _load_json_file("shared/data/flights.json", {})
    return flights.get(flight_id, {}).get("reason")


@tool(
    "get_weather",
    return_direct=False,
    description="Get the current weather conditions at an airport."
)
def get_weather(airport_code: str) -> str:
    airports = _load_json_file("shared/data/airports.json", {})
    return airports.get(airport_code, {}).get("weather")


@tool(
    "check_airport_status",
    return_direct=False,
    description="Get the operational status of an airport."
)
def check_airport_status(airport_code: str) -> str:
    airports = _load_json_file("shared/data/airports.json", {})
    return airports.get(airport_code, {}).get("status")


@tool(
    "check_connection_risk",
    return_direct=False,
    description="Check whether a delayed flight may cause a missed connection."
)
def check_connection_risk(flight_id: str) -> bool:
    flights = _load_json_file("shared/data/flights.json", {})
    return flights.get(flight_id, {}).get("connection_risk")


@tool(
    "get_estimated_departure",
    return_direct=False,
    description="Get the estimated departure time of a flight."
)
def get_estimated_departure(flight_id: str) -> str:
    flights = _load_json_file("shared/data/flights.json", {})
    return flights.get(flight_id, {}).get("estimated_departure")


@tool(
    "get_estimated_arrival",
    return_direct=False,
    description="Get the estimated arrival time of a flight."
)
def get_estimated_arrival(flight_id: str) -> str:
    flights = _load_json_file("shared/data/flights.json", {})
    return flights.get(flight_id, {}).get("estimated_arrival")


@tool(
    "check_alternative_transport",
    return_direct=False,
    description="Get available alternative transportation options for a destination."
)
def check_alternative_transport(destination: str) -> list:
    transport = _load_json_file(
        "shared/data/alternative_transport.json",
        {}
    )
    return transport.get(destination, [])


@tool(
    "get_disruption_severity",
    return_direct=False,
    description="Get the severity level of a flight disruption."
)
def get_disruption_severity(flight_id: str) -> str:
    flights = _load_json_file("shared/data/flights.json", {})
    return flights.get(flight_id, {}).get("severity")
