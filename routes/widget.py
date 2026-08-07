from fastapi import APIRouter

router = APIRouter(
    prefix="/parser_widget",
    tags=["parser_widget"],
)


@router.get("/")
async def get_all_categories():
    return {"message": "Список всех категорий (заглушка)"}

@router.get("/")
async def get_widget():
    return {"message": "Список всех категорий (заглушка)"}