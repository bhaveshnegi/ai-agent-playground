from langchain_core.messages import SystemMessage
from models.llm import llm
from tools.vision_tool import extract_text
from tools.math_tool import divide


tools = [extract_text, divide]

llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


def assistant(state):

    image = state["input_file"]

    system_prompt = f"""
You are Alfred, the butler of Bruce Wayne.

You analyze documents, extract text from images,
and perform calculations when needed.

Currently loaded image: {image}
"""

    sys_msg = SystemMessage(content=system_prompt)

    response = llm_with_tools.invoke(
        [sys_msg] + state["messages"]
    )

    return {
        "messages": [response],
        "input_file": image
    }