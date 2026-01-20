# Documentation Helper - RAG Application

A full-stack Retrieval-Augmented Generation (RAG) application that enables semantic search and interactive chat with documentation using LlamaIndex, Pinecone, and modern web technologies.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Features](#features)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)

## Project Overview

This application combines a powerful Python backend with a modern React frontend to provide an intelligent chat interface that retrieves contextual information from a vector database. Users can ask questions about documentation, and the system returns relevant answers by searching through indexed documents.

**Key Technologies:**

- Backend: FastAPI, LlamaIndex, Pinecone Vector Database, Ollama (Local LLM)
- Frontend: React, TypeScript, Vite
- Vector Storage: Pinecone
- Embeddings: Ollama (`nomic-embed-text:latest`)
- LLM: Ollama (`llama3.1:8b`)

## Architecture

```
User (React Frontend)
         ↓
   Chat Interface
         ↓
FastAPI Backend API
         ↓
    RAG Service
    ├── Chat Engine (LlamaIndex)
    ├── Vector Store (Pinecone)
    └── Session Manager
         ↓
    Pinecone Vector DB
    (Indexed Documentation)
         ↓
    Ollama LLM & Embeddings
    (Local Models)
```

## Backend Setup

### Directory Structure

```
backend/
├── chat_service.py          # FastAPI application with endpoints
├── rag_service.py           # RAG service with chat engine management
└── models/
    └── chat_models.py       # Pydantic models for request/response
```

### Core Components

#### 1. **chat_service.py** - FastAPI Application

Provides HTTP endpoints for chat operations with CORS support.

**Features:**

- FastAPI server running on port 8000
- CORS middleware configured for frontend (http://localhost:5173)
- Two chat endpoints: standard and streaming

**Endpoints:**

- `POST /chat` - Send a message and receive a complete response
- `POST /chat/stream` - Send a message and stream the response token-by-token

**Request Model:**

```python
ChatRequest:
  - session_id (str): Unique identifier for user session
  - message (str): User's message/question
```

**Response Model:**

```python
ChatResponse:
  - response (str): Assistant's response
```

#### 2. **rag_service.py** - RAG Service

Handles all Retrieval-Augmented Generation logic and session management.

**Key Configuration:**

- **Pinecone Index:** `documentation-helper-index-768` (768-dimensional embeddings)
- **LLM Model:** `llama3.1:8b` (via Ollama)
- **Embedding Model:** `nomic-embed-text:latest`
- **Chunk Size:** 512 tokens
- **Chunk Overlap:** 50 tokens
- **Token Limit:** 3900 tokens (for chat memory buffer)

**Core Features:**

- Session-based chat management (in-memory storage)
- Vector-augmented search using Pinecone
- Streaming response generation
- Chat memory buffer for conversation context
- System prompt configuration

**Main Class: RAGService**

```python
RAGService:
  - __init__(): Initialize Pinecone connection and vector index
  - get_chat_engine(session_id): Retrieve or create chat engine for session
  - sessions: Dictionary storing user chat sessions
```

#### 3. **models/chat_models.py** - Data Models

Pydantic models for type-safe request/response handling.

```python
ChatRequest:
  - session_id: str
  - message: str

ChatResponse:
  - response: str
```

### Dependencies

Core Python dependencies (from `pyproject.toml`):

- `fastapi>=0.128.0` - Web framework
- `llama-index>=0.14.12` - RAG framework
- `llama-index-embeddings-ollama>=0.8.6` - Local embedding model
- `llama-index-llms-ollama>=0.9.1` - Local LLM integration
- `llama-index-vector-stores-pinecone>=0.7.1` - Pinecone integration
- `pinecone>=7.3.0` - Vector database client
- `uvicorn>=0.40.0` - ASGI server
- `python-dotenv>=1.2.1` - Environment variable management

### Running the Backend

1. **Install dependencies:**

   ```bash
   uv install
   ```

2. **Set up environment variables** (create `.env` file):

   ```
   PINECONE_API_KEY=your_pinecone_api_key
   ```

3. **Start the backend server:**

   ```bash
   cd backend
   uvicorn chat_service:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

4. **API Documentation** (interactive Swagger UI):
   Visit `http://localhost:8000/docs` for interactive API exploration

## Frontend Setup

### Directory Structure

```
frontend/react-chat/
├── src/
│   ├── App.tsx              # Main React component with chat UI
│   ├── App.css              # Component styles
│   ├── types.ts             # TypeScript type definitions
│   ├── index.css            # Global styles
│   ├── main.tsx             # React entry point
│   └── assets/              # Static assets
├── public/                  # Public static files
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript configuration
└── eslint.config.js         # ESLint configuration
```

### Core Components

#### 1. **App.tsx** - Main Chat Component

Implements the chat interface with real-time message streaming.

**Features:**

- Session-based user identification
- Message history management
- Real-time streaming responses using Server-Sent Events (SSE)
- Auto-scrolling to latest messages
- Input validation

**Key State:**

- `messages`: Array of chat messages (user and assistant)
- `input`: Current user input
- `isStreaming`: Flag for active streaming operation
- `sessionId`: Unique user session identifier

**API Integration:**

- Uses `POST /chat/stream` endpoint
- Implements SSE for token-by-token streaming
- Handles event stream parsing and error handling

#### 2. **types.ts** - Type Definitions

TypeScript interfaces for type safety.

```typescript
ChatRequest:
  - session_id: string
  - message: string

ChatResponse:
  - response: string
```

### Dependencies

Node.js dependencies (from `package.json`):

- `react@^19.2.0` - UI framework
- `react-dom@^19.2.0` - DOM rendering
- `typescript~5.9.3` - Type checking
- `vite@^7.2.4` - Build tool and dev server
- ESLint and TypeScript ESLint for code quality

### Running the Frontend

1. **Install dependencies:**

   ```bash
   cd frontend/react-chat
   npm install
   ```

2. **Start development server:**

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

3. **Build for production:**

   ```bash
   npm run build
   ```

   Output will be in `dist/` directory

4. **Lint the code:**
   ```bash
   npm run lint
   ```

## Features

### User Features

- **Interactive Chat Interface** - Clean, intuitive chat UI
- **Real-time Streaming** - See responses as they're generated
- **Session Management** - Maintains chat history per user session
- **Message History** - View all messages in current session

### Technical Features

- **Vector Search** - Semantic search using Pinecone
- **Context Awareness** - Maintains conversation context with chat memory
- **Streaming Responses** - Real-time token-by-token response generation
- **CORS Support** - Secure cross-origin requests
- **Type Safety** - Full TypeScript type coverage
- **Local LLM** - Privacy-first with local Ollama models
- **Extensible Architecture** - Easy to add features or swap components

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Ollama with `llama3.1:8b` and `nomic-embed-text:latest` models
- Pinecone API key and initialized index

### Quick Start

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd documentation-helper
   ```

2. **Backend Setup:**

   ```bash
   uv install
   echo "PINECONE_API_KEY=your_key" > .env
   cd backend
   uvicorn chat_service:app --reload
   ```

3. **Frontend Setup** (in new terminal):

   ```bash
   cd frontend/react-chat
   npm install
   npm run dev
   ```

4. **Access the Application:**
   - Open browser to `http://localhost:5173`
   - Start chatting with your documentation!

## API Documentation

### Chat Endpoint

#### `POST /chat`

Send a message and receive a complete response.

**Request:**

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d {
    "session_id": "user-123",
    "message": "What is LlamaIndex?"
  }
```

**Response:**

```json
{
  "response": "LlamaIndex is a data framework for your LLM applications..."
}
```

#### `POST /chat/stream`

Send a message and receive a streaming response using Server-Sent Events.

**Request:**

```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d {
    "session_id": "user-123",
    "message": "Tell me about RAG systems"
  }
```

**Response (SSE stream):**

```
data: {"token": "RAG"}

data: {"token": " (Retrieval"}

data: {"token": "-Augmented"}

data: [DONE]
```

## Project Structure

```
documentation-helper/
├── backend/
│   ├── chat_service.py          # FastAPI endpoints
│   ├── rag_service.py           # RAG logic
│   ├── models/
│   │   └── chat_models.py       # Pydantic models
│   └── __pycache__/
├── frontend/
│   └── react-chat/              # React TypeScript application
│       ├── src/
│       ├── public/
│       ├── package.json
│       └── vite.config.ts
├── llamaindex-docs/             # Indexed documentation files
├── chroma_db/                   # Local Chroma vector store (if used)
├── pipeline_cache/              # Cache for ingestion pipelines
├── pyproject.toml               # Python project configuration
├── main.py                      # Main entry point (if applicable)
├── README.md                    # This file
└── [other ingestion scripts]    # Data ingestion scripts
```

## Development Notes

### Session Management

Currently uses in-memory storage for sessions. For production:

- Consider migrating to Redis
- Implement persistent session storage
- Add session cleanup/expiration

### Performance Optimization

- Pinecone index size: 768 dimensions
- Adjustable chunk size and overlap for better context
- Token limit (3900) prevents excessive context memory

### Extending the Application

- Add new endpoints to `chat_service.py`
- Extend `RAGService` for additional retrieval logic
- Add UI components to React frontend
- Implement authentication/authorization

## Future Enhancements

- User authentication and authorization
- Multiple vector indices support
- Document upload functionality
- Conversation export/sharing
- Analytics and usage tracking
- Response feedback mechanism
- Multi-language support
