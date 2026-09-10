from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import CORS_ORIGINS
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.reranker_service import RerankerService
from app.rag.retriever import Retriever
from app.vectorstore.chroma_service import ChromaService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.embedding_service = EmbeddingService()
    app.state.chroma_service = ChromaService()
    app.state.reranker_service = RerankerService()
    app.state.retriever = Retriever(
        app.state.embedding_service, app.state.chroma_service, app.state.reranker_service
    )
    yield


app = FastAPI(title="Interview Intelligence RAG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
