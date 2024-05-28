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

print("retriever", retriever)

# Me
template = """You are an artist, that is very keen in writing scores and performing artistic performances.
Use the following pieces of context to give create a score on how to make an art piece or artistic performance that exploit grey areas inside of the given rules.

Context: {context}

Write your score short and poetic similar to the following examples:

TAPE PIECE I
Stone Piece
Take the sound of the stone aging.

OVERTONE PIECE
Make music only with overtones.

CLOCK PIECE
Listen to the clock strokes.
Make exact repetitions in your head
after they stop.

Direction
Arrange to observe a sign indicating
direction of travel.
Travel in the indicated direction.
Travel in another direction.
1961

Entrance-Exit
A smooth linear transition from white
noise to sinus wave tone is broadcast.
Title is announced at beginning and at end,
but at end, title is announced by a 
tape played backward.
1962

Write no introductory sentence. Answer with the score only.

Question: {question}

Instruction:"""


custom_rag_prompt = PromptTemplate.from_template(template)

llm = ChatOllama(
    base_url=os.environ.get("OLLAMA_URL"),
    model=os.environ.get("OLLAMA_MODEL"),
    temperature=0.5,
)


def format_docs(docs):
    print(retriever)
    print(docs)
    return "\n\n".join(doc.page_content for doc in docs)


def get_relevant_docs(prompt):
    docs = retriever.invoke("rules", top_k=15)
    return docs


rag_chain = (
    {
        "context": lambda x: format_docs(get_relevant_docs(x.get("prompt", ""))),
        "question": lambda x: x.get("prompt", ""),
    }
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)
