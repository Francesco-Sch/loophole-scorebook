import os

from app.utils.embeddings_function import embeddings_function
from fastapi import APIRouter, HTTPException, UploadFile
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_qdrant import Qdrant
from langchain_text_splitters import RecursiveCharacterTextSplitter

router = APIRouter(
    prefix="/database",
    tags=["database"],
    responses={404: {"description": "Not found"}},
)


@router.post("/post", status_code=201, summary="Upload files to Vector Database")
async def post(file: UploadFile):
    """
    Upload file to Vector Database
    """
    try:
        print(f"Uploading file: {file.filename}")
        # Save the file to the server
        folder_path = "/media/uploads"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(f"{folder_path}/{file.filename}", "wb") as buffer:
            buffer.write(file.file.read())

        ###########################
        # LOADING
        ###########################
        pdf_file = PyMuPDFLoader(f"{folder_path}/{file.filename}")

        file_as_document = pdf_file.load()

        # Loop through each document and set the title
        for doc in file_as_document:
            doc.metadata["title"] = file.filename

        ###########################
        # CHUNKING
        ###########################
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(file_as_document)

        print(f"Number of chunks: {len(chunks)}")

        ###########################
        # EMBEDDING
        ###########################
        qdrant_collection = os.environ.get("QDRANT_COLLECTION")

        print(f"Uploading to Qdrant collection: {qdrant_collection}")

        Qdrant.from_documents(
            url=os.environ.get("QDRANT_URL"),
            prefer_grpc=False,
            collection_name=qdrant_collection,
            documents=chunks,
            embedding=embeddings_function,
            force_recreate=True,
        )

        return {
            "success": True,
            "message": "File embedded successfully",
            "documents": chunks,
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
