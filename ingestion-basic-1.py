from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader

#core data structure -- docs and settings
from llama_index.core import Document
from llama_index.core import Settings

# Text Splitters
from llama_index.core.text_splitter import SentenceSplitter

# embedding model
from llama_index.embeddings.openai import OpenAIEmbedding

#Index creation - vector store Index
from llama_index.core import VectorStoreIndex

# LLm configuration -- OpenAI
# from llama_index.llms.openai import OpenAI

# Ollama
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# load_dotenv()

Settings.llm = Ollama(model="llama3.1:8b", request_timeout=120)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest", request_timeout=120)
Settings.chunk_size = 512

def main():
    print("Hello from documentation-helper!")
    documents = SimpleDirectoryReader(
        input_dir="./llamaindex-docs",
        recursive=False,
        required_exts=[".md"],
        num_files_limit=20
        ).load_data()
    
    #create index
    index = VectorStoreIndex.from_documents(documents=documents)

    # query the index
    query_engine = index.as_query_engine()
    response = query_engine.query("How to integrate pinecone as a vector store?")
    print(response)

if __name__ == "__main__":
    main()