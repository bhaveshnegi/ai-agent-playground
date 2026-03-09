from llama_index.core import SimpleDirectoryReader

def load_documents(directory):
    reader = SimpleDirectoryReader(input_dir=directory)
    return reader.load_data()