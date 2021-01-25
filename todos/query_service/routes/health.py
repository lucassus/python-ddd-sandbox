from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_endpoint():
    return {"message": "I'm fine!"}
