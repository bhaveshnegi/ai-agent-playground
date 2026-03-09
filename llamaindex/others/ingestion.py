from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.ingestion import IngestionPipeline

def get_pipeline(vector_store=None):
    return IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=20),
            HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),
        ],
        vector_store=vector_store,
    )
