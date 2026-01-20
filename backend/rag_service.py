import os
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine.types import ChatMode
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from pinecone import Pinecone

load_dotenv()

INDEX_NAME = "documentation-helper-index-768"

# Global settings (loaded once)
Settings.llm = Ollama(model="llama3.1:8b", request_timeout=300)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text:latest",
    request_timeout=300
)
Settings.chunk_size = 512
Settings.chunk_overlap = 50


class RAGService:
    def __init__(self):
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        pinecone_index = pc.Index(INDEX_NAME)

        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        self.index = VectorStoreIndex.from_vector_store(vector_store)

        # In-memory session storage (replace with Redis later)
        self.sessions = {}

    def get_chat_engine(self, session_id: str):
        if session_id not in self.sessions:
            memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
            self.sessions[session_id] = self.index.as_chat_engine(
                chat_mode=ChatMode.BEST,
                memory=memory,
                streaming=True,
                system_prompt=(
                    "You are a helpful assistant that answers questions "
                    "using documents stored in Pinecone."
                ),
            )
        return self.sessions[session_id]
