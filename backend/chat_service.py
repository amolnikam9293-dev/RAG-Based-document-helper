from fastapi import FastAPI
from rag_service import RAGService
from models.chat_models import ChatRequest, ChatResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag = RAGService()


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    chat_engine = rag.get_chat_engine(req.session_id)
    response = chat_engine.chat(req.message)
    return {"response": response.response}


from fastapi.responses import StreamingResponse
import json

@app.post("/chat/stream")
def chat_stream(req: ChatRequest):

    def event_generator():
        chat_engine = rag.get_chat_engine(req.session_id)
        response = chat_engine.stream_chat(req.message)

        for token in response.response_gen:
            yield f"data: {json.dumps({'token': token})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
