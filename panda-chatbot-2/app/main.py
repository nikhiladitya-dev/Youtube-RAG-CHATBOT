from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes import router
from app.core.service_container import container




@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Initializing services...")

    container.initialize()

    print("Application Ready!")

    yield

    print("Shutting down...")


app = FastAPI(
    title="YouTube RAG Chatbot",
    description="""
Production grade Retrieval-Augmented Generation API
for chatting with YouTube videos.

Features:
- Transcript Extraction
- Semantic Retrieval
- Conversational Memory
- Timestamp Citations
- Video-specific Retrieval
""",

    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)

