import os
import asyncio
from dotenv import load_dotenv
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core.workflow import Context

load_dotenv()

# Retrieve HF_TOKEN from the environment variables
hf_token = os.getenv("HF_TOKEN")

llm = HuggingFaceInferenceAPI(
    model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
    temperature=0.7,
    max_tokens=200,
    token=hf_token,
)

# Define some tools
async def add(ctx: Context, a: int, b: int) -> int:
    """Add two numbers."""
    # update our count
    state = await ctx.store.get("state")
    state["num_fn_calls"] += 1
    await ctx.store.set("state", state)
    return a + b

async def multiply(ctx: Context, a: int, b: int) -> int:
    """Multiply two numbers."""
    # update our count
    state = await ctx.store.get("state")
    state["num_fn_calls"] += 1
    await ctx.store.set("state", state)
    return a * b

# Define the agents
multiply_agent = ReActAgent(
    name="multiply_agent",
    description="An agent that can multiply two numbers.",
    tools=[multiply],
    llm=llm,
)

addition_agent = ReActAgent(
    name="addition_agent",
    description="An agent that can add two numbers.",
    tools=[add],
    llm=llm,
)

# Create the workflow
workflow = AgentWorkflow(
    agents=[multiply_agent, addition_agent],
    root_agent="multiply_agent",
    initial_state={"num_fn_calls": 0},
    state_prompt="Current state: {state}. User message: {msg}",
)

async def main():
    # run the workflow with context
    ctx = Context(workflow)
    # Initialize the state in the store
    await ctx.store.set("state", {"num_fn_calls": 0})
    
    response = await workflow.run(user_msg="Can you add 5 and 3?", ctx=ctx)
    print(response)

    # pull out and inspect the state
    state = await ctx.store.get("state")
    print(f"Number of function calls: {state['num_fn_calls']}")

if __name__ == "__main__":
    asyncio.run(main())