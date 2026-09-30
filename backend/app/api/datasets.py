from fastapi import APIRouter

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


@router.get("")
def get_datasets():
    return {
        "status": "ok",
        "message": (
            "Dataset integration is not implemented yet."
        ),
        "datasets": [],
    }