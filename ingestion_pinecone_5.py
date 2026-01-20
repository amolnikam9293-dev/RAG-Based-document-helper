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
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from chromadb import chromadb

# LLm configuration -- OpenAI
# from llama_index.llms.openai import OpenAI

# Ollama
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

load_dotenv()

# Configuration
INDEX_NAME = "documentation-helper-index-768"
EMBEDDING_DIMENTION = 768 # text-embedding-3-small dimention

# LlamaIndex settings
Settings.llm = Ollama(model="llama3.1:8b", request_timeout=300)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest", request_timeout=300)
Settings.chunk_size = 512
Settings.chunk_overlap = 50

def main():
    print("=" * 60)
    print("Pinecone Ingestion Pipeline")
    print("=" * 60)

    # connect to Pinecone vector store index
    print("Connecting to Pinecone vector store...")
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY"),
    )
    pinecone_index = pc.Index(INDEX_NAME)
    vector_store = PineconeVectorStore(
        pinecone_index=pinecone_index
    )

    # check current stats
    stats = pinecone_index.describe_index_stats()
    print(f"Connected to index: {INDEX_NAME}")
    print(f"Current vector in index: {stats.total_vector_count}")

    # Load ALL documents from the 'data' directory
    print("Loading documents from 'data' directory...")
    documents = SimpleDirectoryReader(
        input_dir="./llamaindex-docs",
        required_exts=[".md"],
        num_files_limit=1000
    ).load_data()
    print(f"Loaded {len(documents)} documents.")

    # Create ingestion pipeline
    print("Creating ingestion pipeline...")
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(
                chunk_size=Settings.chunk_size,
                chunk_overlap=Settings.chunk_overlap
            ),
            OllamaEmbedding(
            model_name=Settings.embed_model.model_name, 
            request_timeout=300)
            ],
            vector_store=vector_store
    )

    # Step 4: Run the pipeline
    print("\n[4/5] Running ingestion pipeline...")
    print("(This may take a few minutes)")

    import time
    start_time = time.time()
    nodes = pipeline.run(documents=documents, show_progress=True, num_workers=4)
    end_time = time.time()
    print(f"Ingestion complete!")
    print(f"Ingestion pipeline completed in {end_time - start_time:.2f} seconds.")
    print(f"Nodes created: {len(nodes)}")

    # Step 5: Verify and test query
    print("\n[5/5] Testing query...")

    stats = pinecone_index.describe_index_stats()
    print(f"Total vectors in Pinecone: {stats.total_vector_count}")
    index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = index.as_query_engine()
    response = query_engine.query("What is LlamaIndex?")
    print(f"\n Query Response: {response}")

    print("\n" + "=" * 60)
    print(f"Done! {len(nodes)} nodes stored in Pinecone index '{INDEX_NAME}'")
    print("=" * 60)

if __name__ == "__main__":
    main()