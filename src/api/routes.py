"""FastAPI backend для Brandmarka."""

import json
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from core.brand import load as load_brand, save as save_brand
from generators import business_card, email_signature, presentation, proposal

app = FastAPI(title="Brandmarka")

# Раздаём статические файлы из папки web
web_dir = Path(__file__).resolve().parent.parent / "web"
app.mount("/static", StaticFiles(directory=web_dir), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    """Главная страница."""
    index_path = web_dir / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<h1>Brandmarka API</h1><p>Перейдите в папку src/web и создайте index.html</p>"


@app.post("/api/brandbook")
def upload_brandbook(brandbook: UploadFile = File(...)):
    """Загрузить бренд-бук компании."""
    content = brandbook.file.read().decode("utf-8")
    data = json.loads(content)
    save_brand(data)
    return {"status": "ok", "company": data.get("company")}


@app.get("/api/brandbook")
def get_brandbook():
    """Получить текущий бренд-бук."""
    return load_brand()


@app.post("/api/business-card")
def create_business_card(payload: str = Form(...)):
    """Сгенерировать визитку."""
    input_data = json.loads(payload)
    path = business_card.generate(input_data)
    return FileResponse(path, filename=path.name)


@app.post("/api/email-signature")
def create_email_signature(payload: str = Form(...)):
    """Сгенерировать email-подпись."""
    input_data = json.loads(payload)
    path = email_signature.generate(input_data)
    return FileResponse(path, filename=path.name)


@app.post("/api/presentation")
def create_presentation(payload: str = Form(...)):
    """Сгенерировать презентацию."""
    input_data = json.loads(payload)
    path = presentation.generate(input_data)
    return FileResponse(path, filename=path.name)


@app.post("/api/proposal")
def create_proposal(payload: str = Form(...)):
    """Сгенерировать коммерческое предложение."""
    input_data = json.loads(payload)
    path = proposal.generate(input_data)
    return FileResponse(path, filename=path.name)
