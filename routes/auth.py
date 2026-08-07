from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER

from config import get_settings

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["auth"])

settings = get_settings()

ADMIN_USERNAME = settings.ADMIN_USERNAME
ADMIN_PASSWORD = settings.ADMIN_PASSWORD

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return None
    return user


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    # Если уже вошёл — отправляем на главную
    if request.session.get("user"):
        return RedirectResponse("/parser_widget/", status_code=HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(request,"login.html", {"request": request, "error": None})


@router.post("/login")
def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["user"] = username
        return RedirectResponse("/parser_widget/", status_code=HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request, "error": "Неверный логин или пароль"},
        status_code=400
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)