import os
import asyncio
import subprocess
from dotenv import load_dotenv

from llama_index.core import Settings

# Ollama
from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import ReActAgent, AgentStream, ToolCallResult, FunctionAgent
from llama_index.core.workflow import Context


# LlamaIndex settings
Settings.llm = Ollama(model="llama3.1:8b", request_timeout=300)

load_dotenv()

# define the tools
def multiply(a: int, b: int) -> int:
    """Multiplies two integers."""
    return a * b

def add(a: int, b: int) -> int:
    """Adds two integers and returns the result."""
    return a + b

def open_screenshot() -> str:
    """Opens the screenshot application on my computer to capture a screen screenshot """
    try:
        subprocess.run(["open", "-a", "Screenshot"], check=True)
        return "Screenshot application opened successfully."
    except subprocess.CalledProcessError as e:
        return f"An error occurred while trying to open the screenshot application: {e}"

async def main():
    llm = Settings.llm

    # define the ReactAgent
    # agent = ReActAgent(
    #     llm=llm,
    #     tools=[multiply, add, open_screenshot]
    # )
    agent = FunctionAgent(
        llm=llm,
        tools=[multiply, add, open_screenshot],
        allow_parallel_tool_calles=True
    )

    # create a context for the agent
    context = Context(agent)

    # Run the agent with a sample query (asynchronous execution)
    handler = agent.run(
        "What is the sum of 5 and 10, and then multiply the result by 2? Also, open the screenshot on my Mac.",
        ctx=context
    )

    # Stream the response
    async for ev in handler.stream_events():
        if isinstance(ev, ToolCallResult):
            print(f"Tool call result: {ev.tool_name} returned {ev.tool_output}")
        if isinstance(ev, AgentStream):
            print(ev.delta, end="", flush=True)

    # Get final response
    final_response = await handler
    print(f"Agent Response: {final_response}")

if __name__=="__main__":
    asyncio.run(main())