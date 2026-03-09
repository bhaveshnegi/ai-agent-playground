import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def get_chroma_vector_store(path="./alfred_chroma_db", collection_name="alfred"):
    db = chromadb.PersistentClient(path=path)
    chroma_collection = db.get_or_create_collection(collection_name)
    return ChromaVectorStore(chroma_collection=chroma_collection)

def get_index(vector_store, embed_model_name="BAAI/bge-small-en-v1.5"):
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
    return VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

# The following lines are assumed to be part of a larger script
# and will now use the functions defined above.
# For example:
# vector_store = get_chroma_vector_store()
# index = get_index(vector_store)

# The IngestionPipeline part remains as it was not part of the requested change.
# Note: IngestionPipeline and SentenceSplitter are not defined in the provided snippet,
# but are kept as they were in the original document.
# You might need to add their imports if they are used in the actual full script.
# from llama_index.core.ingestion import IngestionPipeline
# from llama_index.core.node_parser import SentenceSplitter

# pipeline = IngestionPipeline(
#     transformations=[
#         SentenceSplitter(chunk_size=25, chunk_overlap=0),
#         HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),
#     ],
#     vector_store=vector_store,
# )