import sys
from dotenv import load_dotenv
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from tools.booking_tools import GetFlightOptions, GetNearbyAirports
from tools.customer_tools import (GetBookingHistory,
                                  GetCustomerProfile, UpdateCustomerProfile)
from tools.utilties import SearchWeb, GetCurrentDate, EndConversation
from pydantic import BaseModel
load_dotenv()

@dataclass
class AgentContext:
    user_id: str


SYSTEM_PROMPT = (
    "You are a travel support agent. "
    "Use tools whenever they can answer the question directly — flights, airports, "
    "visa rules, and customer/booking data should come from tools, not memory. "
    "Only use the search tool when the answer requires current information the other "
    "tools can't provide; it is costly, so use it sparingly. "
    "If a tool call fails or returns no data, tell the user plainly — never fabricate "
    "flight numbers, prices, visa rules, or customer details. "
    "If the user asks you to end the conversation, call the end_conversation tool and exit gracefully. "
    "Write in plain text with no headers, bullets, or markdown formatting. "
    "Be concise: short, direct sentences, no filler or repeated information."
)

TOOLS = [
    GetCurrentDate,
    GetNearbyAirports,
    GetFlightOptions,
    SearchWeb,
    GetCustomerProfile,
    GetBookingHistory,
    UpdateCustomerProfile,
    EndConversation
]


agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)

def run_agent():

    print("Welcome to the Travel Support Agent!")

    user_id = 12345
    context = AgentContext(user_id=user_id)

    messages = []
    ended = False
    while True:
        
        if ended:
            print("thank you for using the Travel Support Agent. Goodbye!")
            sys.exit(0)
        user_input = input("User: ")

        # Add the new user message to the conversation history
        messages.append(HumanMessage(content=user_input))

        stream = agent.stream(
            {"messages": messages},
            context=context,
            stream_mode="values",
        )


        for snapshot in stream:
            latest_message = snapshot["messages"][-1]
            if isinstance(latest_message, AIMessage):
                if latest_message.tool_calls:
                    print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
                    if any(tc["name"] == "end_conversation" for tc in latest_message.tool_calls):
                        ended = True
                if latest_message.content:
                    print(f"Agent: {latest_message.content}")
            # if isinstance(latest_message, ToolMessage):
            #     print(f"Tool Result: {latest_message.content}")
            messages = snapshot["messages"] 

if __name__ == "__main__":
    run_agent()

