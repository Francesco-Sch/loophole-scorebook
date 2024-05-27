import os

from langchain_community.embeddings import OllamaEmbeddings

embeddings_function = OllamaEmbeddings(
    base_url=os.getenv("OLLAMA_EMBEDDING_URL", "http://localhost:11434"),
    model=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"),
)
