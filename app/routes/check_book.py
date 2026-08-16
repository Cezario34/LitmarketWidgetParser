from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from app.core.template_config import templates

router = APIRouter(
    prefix="/check_books",
    tags=["check_books"],
)

@router.get("/", response_class=HTMLResponse)
async def count_symbols(request: Request):
    return templates.TemplateResponse(request, 'check_books.html')

