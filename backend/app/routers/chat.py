import os

from app.utils.embeddings_function import embeddings_function
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStore
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

# Initialize the Qdrant Client
# to connect to the Qdrant vector database
qdrant_client = QdrantClient(url=os.environ.get("QDRANT_URL"), prefer_grpc=False)
qdrant_collection = os.environ.get("QDRANT_COLLECTION")

vectorstore: VectorStore = Qdrant(
    client=qdrant_client,
    collection_name=qdrant_collection,
    embeddings=embeddings_function,
)

retriever = vectorstore.as_retriever()

# Me
template = """You are an artist, that is very keen in writing scores and performing artistic performances.
Use the following pieces of context to give instructions on how to make an art piece or artistic performance that exploit grey areas inside of the given rules.
Return your instruction as an artistic score in the style of Yoko Ono.

{context}

Question: {question}

Instruction:"""

# ChatGPT
# template = """ Imagine you are the artist Yoko Ono.
# You are to create an instruction for an artistic symbol, performance, or art piece in a style similar to your book 'Grapefruit'.
# This instruction should explore and creatively interpret the boundaries of the legal ruleset provided in the context by the University of Bremen.
# Please craft a response that is elaborate, precise, and demonstrates a deep knowledge of art.
# Your instruction should encourage reflection on the gray areas of these rules, prompting an artistic expression that is both profound and respects legal boundaries.

# {context}

# Question: {question}

# Instruction:"""
custom_rag_prompt = PromptTemplate.from_template(template)

llm = ChatOllama(
    base_url=os.environ.get("OLLAMA_URL"),
    model=os.environ.get("OLLAMA_MODEL"),
    temperature=0.75,
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": RunnablePassthrough(), "question": lambda x: x["prompt"]}
    # {"context": {"context": retriever | format_docs}, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)
