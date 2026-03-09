import os
import asyncio
from dotenv import load_dotenv
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

from dataload import load_documents
from ingestion import get_pipeline
from storing import get_chroma_vector_store, get_index

from llama_index.core.evaluation import FaithfulnessEvaluator

# Load the .env file
load_dotenv()

# Retrieve HF_TOKEN from the environment variables
hf_token = os.getenv("HF_TOKEN")

async def main():
    # 1. Load Data
    print("Loading documents...")
    documents = load_documents("../Data")
    print("Loaded documents:", len(documents))
    print(documents[0].text[:500])

    # 2. Setup Storing
    print("Initializing vector store...")
    vector_store = get_chroma_vector_store()

    # 3. Ingestion Pipeline
    print("Running ingestion pipeline...")
    pipeline = get_pipeline(vector_store=vector_store)
    await pipeline.arun(documents=documents)

    # 4. Initialize Index
    print("Initializing index...")
    index = get_index(vector_store)

    # 5. Query
    print("Initializing LLM...")
    llm = HuggingFaceInferenceAPI(
        model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
        temperature=0.7,
        max_tokens=200,
        token=hf_token,
    )

    query_engine = index.as_query_engine(llm=llm)
    
    question = "Analyze the resume and tell me the key skills of Bhavesh Negi."
    print(f"Querying: {question}")
    response = query_engine.query(question)
    
    print("\nResponse:")
    print(response)

    evaluator = FaithfulnessEvaluator(llm=llm)
    eval_result = evaluator.evaluate_response(response=response)
    eval_result.passing

if __name__ == "__main__":
    asyncio.run(main())