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
Settings.chunk_overlap = 500

def main():
    documents = SimpleDirectoryReader(
        input_dir="./llamaindex-docs",
        required_exts=[".md"],
        num_files_limit=10,
    ).load_data()

    print(f"Loaded {len(documents)} documents.")

    node_parser = SentenceSplitter(
        chunk_size=Settings.chunk_size,
        chunk_overlap=Settings.chunk_overlap
    )

    # Parse documents into nodes with custome chunking
    print(f"Parsing documents into nodes with custom chunking...")
    nodes = node_parser.get_nodes_from_documents(documents)
    print(f"Parsed {len(nodes)} nodes from documents.")

    # Inspect a few sample nodes
    print("\nSample nodes after custom chunking:")
    for i, node in enumerate(nodes[:3]):
        print(f"\nNode {i+1} content: \n{node.get_content()}\n")

        #Display metadata if available
        if node.metadata:
            print(f"- source {node.metadata.get("file_name", "N/A")}")

    # Create Vector Store Index from nodes
    print("Creating Vector store Index from nodes...")
    index = VectorStoreIndex(nodes=nodes)
    print("Vectore Store Index created successfully")

    # Example query to test the index
    query = "What is LLamaIndex?"
    print(f"\nQuerying the index with: '{query}'")
    response = index.as_query_engine().query(query)
    print(f"Response: \n{response}")

if __name__ == "__main__":
    main()