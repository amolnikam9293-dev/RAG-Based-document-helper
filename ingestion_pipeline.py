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

PERSISTENCE_DIR = "./pipeline_storage"
CHROMA_DIR = "./chroma_db"

def get_transformations():
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
    documents = SimpleDirectoryReader(
        input_dir="./llamaindex-docs",
        required_exts=[".md"],
        num_files_limit=5
    ).load_data()
    print(f"Loaded {len(documents)} documents.")

    # Create persistent chroma vector store
    print("Setting up ChromaDB vector store...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(name="llamaindex_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Check how many docs already in vector store
    existing_count = chroma_collection.count()
    print(f"ChromaDB already contains {existing_count} embeddings.")

    # If we already have embeddings, skip ingestion and go straight to querying
    if existing_count > 0:
        print("Using existing embeddings from ChromaDB (skipping ingestion).")
    else:
        # Create and run the ingestion pipeline
        print("Creating ingestion pipeline...")
        pipeline = IngestionPipeline(
            transformations=get_transformations(),
            vector_store=vector_store
        )

        print("Running ingestion pipeline...")
        processed_nodes = pipeline.run(documents=documents, show_progress=True)
        print(f"Processed {len(processed_nodes)} nodes into ChromaDB.")

    # # Create pipeline
    # print("Creating ingestion pipeline...")
    # pipeline = IngestionPipeline(
    #     transformations=get_transformations(),
    #     docstore=SimpleDocumentStore(persist_dir=PERSISTENCE_DIR)
    #     )
    
    # # Check if we have a persisted cache to load
    # if os.path.exists(PERSISTENCE_DIR):
    #     print("Loading persisted document store...")
    #     pipeline.docstore.load(persist_dir=PERSISTENCE_DIR)
    #     print("Loaded persisted document store.")
    
    # #Run pipeline (Will skip cached/unchanged documnets)
    # print("Running ingestion pipeline...")
    # processed_nodes = pipeline.run(documents=documents, show_progress=True)
    # print(f"Processed into {len(processed_nodes)} nodes with embeddings.")

    # # Persist the cache for the next run
    # print(f"Persisting documnet store...{PERSISTENCE_DIR}")
    # pipeline.docstore.persist(persist_dir=PERSISTENCE_DIR)
    # print("Document store persisted.")

        # Show metadata from first node
        if processed_nodes:
            if processed_nodes[0].embedding:
                print(f"Embedding dimensions: {len(processed_nodes[0].embedding)}")
            
            first_node_metadata = processed_nodes[0].metadata
            print("First node metadata:")
            for key, value in first_node_metadata.items():
                print(f"  {key}: {value}")

    #create index from the vector store
    print("Creating vectore store index from ChromaDB...")
    vector_index = VectorStoreIndex.from_vector_store(vector_store)
    print("Vectore store index created successfully.")

    # create query engine
    query_engine = vector_index.as_query_engine()

    # Sample query
    print("\n---Query Test---")
    response = query_engine.query("What is SimpleDirectoryReader?")
    print("Query: Whaht is the SimpleDirectoryReader?")
    print(f"Response:\n {response}")

if __name__ == "__main__":
    main()