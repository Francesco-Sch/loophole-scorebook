from fastapi import APIRouter, HTTPException, UploadFile

router = APIRouter(
    prefix="/database",
    tags=["database"],
    responses={404: {"description": "Not found"}},
)


@router.post("/post", status_code=201, summary="Upload files to Vector Database")
async def post(file: UploadFile):
    """
    Upload files to Vector Database
    """
    try:
        return {"file": file}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
