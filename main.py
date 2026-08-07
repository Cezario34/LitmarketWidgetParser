from fastapi import FastAPI

from routes import widget

app = FastAPI(
    title="Парсер Виджетов",
    version="0.1.0",
    )

app.include_router(widget.router)

@app.get("/")
async def root():
    return {"message": "Парсер виджетов"}