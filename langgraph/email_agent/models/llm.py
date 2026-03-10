from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from dotenv import load_dotenv

load_dotenv()

# Set HF token correctly
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN")

# Base endpoint model
endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    temperature=0.7,
    max_new_tokens=200,
    task="conversational"
)

# Wrap in chat interface
llm = ChatHuggingFace(llm=endpoint)