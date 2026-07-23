import json
from pathlib import Path
from langchain.tools import tool

DATA_DIR = Path(__file__).resolve().parent.parent / "shared" / "data"


@tool(
    "get_nearby_airports",
    return_direct=False,
    description="Get nearby airports based on the provided city."
)
def GetNearbyAirports(city: str) -> list:
    """
    Get nearby airports based on the provided city.
    Args:
        city (str): The name of the city to search for nearby airports.
    Returns:
        list: A list of nearby airports.
    """
    with open(DATA_DIR / "airports.json", "r", encoding="utf-8") as file:
        airports = json.load(file)

    return [
        airport
        for airport in airports
        if airport["city"].lower() == city.lower()
    ]


@tool(
    "get_flight_options",
    return_direct=False,
    description="Get flight options based on the provided parameters."
)
def GetFlightOptions(
    originSkyId: str,
    destinationSkyId: str,
    departureDate: str,
) -> list:

    """
    Get flight options based on the provided parameters.
    Args:
        originSkyId (str): The Sky ID of the origin airport.
        destinationSkyId (str): The Sky ID of the destination airport.
        departureDate (str): The departure date in YYYY-MM-DD format.
    Returns:
        list: A list of flight options.
    """

    with open(DATA_DIR / "flights.json", "r", encoding="utf-8") as file:
        flights = json.load(file)

    return [
        flight
        for flight in flights
        if (
            flight["originSkyId"] == originSkyId
            and flight["destinationSkyId"] == destinationSkyId
            and flight["departureDate"] == departureDate
        )
    ]