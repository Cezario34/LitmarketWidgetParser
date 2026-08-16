from fastapi.templating import Jinja2Templates
from datetime import datetime

templates = Jinja2Templates(directory="templates")

# --- Глобальные переменные ---
templates.env.globals["app_name"] = "BookDayStats"
templates.env.globals["current_year"] = datetime.now().year

# --- Фильтры ---
def format_date(value, fmt="%d.%m.%Y %H:%M"):
    if not value:
        return "—"
    return value.strftime(fmt)

def format_number(value):
    try:
        return f"{int(value):,}".replace(",", " ")
    except (ValueError, TypeError):
        return value

templates.env.filters["format_date"] = format_date
templates.env.filters["format_number"] = format_number