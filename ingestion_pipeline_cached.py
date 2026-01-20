import os
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

from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.chroma import ChromaVectorStore

from chromadb import chromadb

# LLm configuration -- OpenAI
# from llama_index.llms.openai import OpenAI

# Ollama
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# load_dotenv()

Settings.llm = Ollama(model="llama3.1:8b", request_timeout=300)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest", request_timeout=300)
Settings.chunk_size = 512
Settings.chunk_overlap = 50

# Directories for persistence
CHROMA_DIR = "./chroma_db"
CACHE_DIR = "./pipeline_cache"

def get_transformations():
    """Return transformations - must be identical for cache to work."""
    return [
        SentenceSplitter(
            chunk_size=Settings.chunk_size,
            chunk_overlap=Settings.chunk_overlap
            ),
        OllamaEmbedding(
            model_name=Settings.embed_model.model_name, 
            request_timeout=300)
    ]

def main():
    print("=" * 60)
    print("Ingestion pipeline with LlamaIndex Caching")
    print("=" * 60)

    # Load documents
    print("\n[1/6] Loading documents...")
    documents = SimpleDirectoryReader(
        input_dir="./llamaindex-docs",
        required_exts=[".md"],
        num_files_limit=10
    ).load_data()
    print(f"Found {len(documents)} documents in source directory.")

    # Creating persistent Chroma vector store
    print("\n[2/6] Setting up ChromaDB vector store...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(name="llamaindex-docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    print(f"ChromaDB path: {CHROMA_DIR}")
    print(f"Existing embeddings in chromaDB: {chroma_collection.count()}")

    # Creating pipeline with docstore for deduplication
    print("\n[3/6] Creating ingestion pipeline with caching...")
    pipeline = IngestionPipeline(
        transformations=get_transformations(),
        vector_store=vector_store,
        docstore=SimpleDocumentStore()
    )

    # Load existing cache if available
    if os.path.exists(CACHE_DIR):
        print(f"Loading existing cache from {CACHE_DIR}...")
        pipeline.load(persist_dir=CACHE_DIR)
        print("Cache loaded! Unchanged document will be skipped.")
    else:
        print("No existing cache found. Will process all documents.")
    
    # Run the pipeline - LlamaIndex will use cached transformations
    print("\n[4/6] Running ingestion pipeline...")
    print("(Cached transformations will be reused - no redundant API calls!)")

    import time
    start_time = time.time()
    processed_nodes = pipeline.run(documents=documents, show_progress=True)
    elapsed = time.time() - start_time

    # Report results
    print(f"\nPipeline completed in {elapsed:.2f} seconds.")
    print(f"Nodes returned: {len(processed_nodes)}")
    print(f"Total embeddings in ChromaDB: {chroma_collection.count()}")

    # Show metadata from first processed node (if any)
    if processed_nodes:
        print("\nSample metadata from first New node:")
        if processed_nodes[0].embedding:
            print(f"- Embedding dimensions: {len(processed_nodes[0].embedding)}")
        first_node_metadata = processed_nodes[0].metadata
        for key, value in list(first_node_metadata.items())[:3]:
            print(f"  {key}: {value}")

    # Persist cache for next run
    print(f"\n[5/6] Persisting cache to {CACHE_DIR}...")
    pipeline.persist(persist_dir=CACHE_DIR)
    print("Cache saved! Next run will skip unchanged documents.")

    # Create index and query
    print("\n[6/6] Creating vectore store index and testing query...")
    vector_index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = vector_index.as_query_engine()

    print("\n" + "=" * 60)
    print("Query Test")
    print("=" * 60)
    query = "What is LlamaIndex used for?"
    print(f"Query: {query}")
    response = query_engine.query(query)
    print(f"Response:\n {response}")

if __name__ == "__main__":
    main()