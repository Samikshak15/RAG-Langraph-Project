import os

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

# IntelliConvo MongoDB
INTELLICONVO_URI = os.getenv(
    "INTELLICONVO_URI",
    "mongodb://unknown2:HJfgd63sGdf31YgsYhs@216.48.179.107:37017/test_intelliconvo_new_dev?authSource=admin",
)
INTELLICONVO_DB_NAME = os.getenv("INTELLICONVO_DB_NAME", "intelliconvo_new_dev")

# Together AI
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = os.getenv(
    "TOGETHER_MODEL",
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
)

# Embeddings & vector store
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-base-en-v1.5")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "interview_chunks")

# API layer
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
CURRICULUM_PATH = os.getenv("CURRICULUM_PATH", "data/curriculum.json")
SAMPLE_TRANSCRIPT_PATH = os.getenv("SAMPLE_TRANSCRIPT_PATH", "data/sample_transcript.txt")
CANDIDATES_PATH = os.getenv("CANDIDATES_PATH", "data/candidates.json")

# Reranking
RERANK_MODEL_NAME = os.getenv("RERANK_MODEL_NAME", "cross-encoder/ms-marco-MiniLM-L-6-v2")
RERANK_CANDIDATE_MULTIPLIER = int(os.getenv("RERANK_CANDIDATE_MULTIPLIER", "4"))
RERANK_CANDIDATE_CEILING = int(os.getenv("RERANK_CANDIDATE_CEILING", "25"))