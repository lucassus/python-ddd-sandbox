from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def helo_endpoint():
    return {"message": "I'm fine!"}
