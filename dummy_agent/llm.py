from dotenv import load_dotenv
load_dotenv()
import os
from huggingface_hub import InferenceClient
from system_prompt import SYSTEM_PROMPT
from getweather_tool import get_weather
from calculator import calculator

HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(
    model="moonshotai/Kimi-K2.5",
    token=HF_TOKEN
)

# ******************1***********************
# output = client.chat.completions.create(
#     messages=[
#         {"role": "user", "content": "The capital of France is"},
#     ],
#     stream=False,
#     max_tokens=1024,
#     extra_body={'thinking': {'type': 'disabled'}},
# )
# print(output.choices[0].message.content)

# ******************2***********************
# output = client.chat.completions.create(
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "What is the weather like in San Francisco?"},
#     ],
#     stream=False,
#     max_tokens=1024,
#     extra_body={'thinking': {'type': 'disabled'}},
# )

# print(output.choices[0].message.content)

# ******************3***********************
# messages = [
#     {"role": "system", "content": SYSTEM_PROMPT},
#     {"role": "user", "content": "What's the weather in London?"},
# ]

# output = client.chat.completions.create(
#     messages=messages,
#     stream=False,
#     max_tokens=200,
#     extra_body={'thinking': {'type': 'disabled'}},
# )

# print(output.choices[0].message.content)

# ******************4***********************
# The answer was hallucinated by the model. We need to stop to actually execute the function!
# output = client.chat.completions.create(
#     messages=messages,
#     max_tokens=150,
#     stop=["Observation:"], # Let's stop before any actual function is called
#     extra_body={'thinking': {'type': 'disabled'}},
# )

# print(output.choices[0].message.content)

# ******************5***********************
# messages = [
#     {"role": "system", "content": SYSTEM_PROMPT},
#     {"role": "user", "content": "What's the weather in London?"}
# ]

# # Step 1: Ask the model what action to take
# output = client.chat.completions.create(
#     messages=messages,
#     max_tokens=150,
#     stop=["Observation:"],
#     extra_body={'thinking': {'type': 'disabled'}},
# )

# assistant_message = output.choices[0].message.content
# print(assistant_message)

# # Step 2: Execute the tool
# weather = get_weather("London")

# # Step 3: Send observation back to the model
# messages.append({
#     "role": "assistant",
#     "content": assistant_message + "Observation:\n" + weather
# })

# # Step 4: Final answer
# final_output = client.chat.completions.create(
#     messages=messages,
#     max_tokens=200,
#     extra_body={'thinking': {'type': 'disabled'}},
# )

# print(final_output.choices[0].message.content)

# ******************6***********************
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "What is the sum of 5 and 5?"}
]

# Step 1: Ask the model what action to take
output = client.chat.completions.create(
    messages=messages,
    max_tokens=150,
    stop=["Observation:"],
    extra_body={'thinking': {'type': 'disabled'}},
)

assistant_message = output.choices[0].message.content
print(assistant_message)

# Step 2: Execute the tool
calculator_result = calculator(1, 2)

# Step 3: Send observation back to the model
messages.append({
    "role": "assistant",
    "content": f"{assistant_message}Observation:\n{calculator_result}"
})

# Step 4: Final answer
final_output = client.chat.completions.create(
    messages=messages,
    max_tokens=200,
    extra_body={'thinking': {'type': 'disabled'}},
)

print(final_output.choices[0].message.content)
