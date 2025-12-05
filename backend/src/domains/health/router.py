from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


# TODO: Add health checks for database and other dependencies