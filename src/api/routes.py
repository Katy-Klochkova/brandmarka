"""FastAPI backend для Brandmarka."""

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from core.brand import load as load_brand, save as save_brand
from core.config import UPLOADS_DIR
from generators import business_card, email_signature, presentation, proposal

app = FastAPI(title="Brandmarka")

# Раздаём статические файлы из папки web
web_dir = Path(__file__).resolve().parent.parent / "web"
app.mount("/static", StaticFiles(directory=web_dir), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/svg+xml"}


@app.get("/", response_class=HTMLResponse)
def root():
    """Главная страница."""
    index_path = web_dir / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<h1>Brandmarka API</h1><p>Перейдите в папку src/web и создайте index.html</p>"


@app.post("/api/brandbook")
def upload_brandbook(
    brandbook: UploadFile = File(...),
    logo: Optional[UploadFile] = File(None),
):
    """Загрузить бренд-бук компании и опционально логотип."""
    content = brandbook.file.read().decode("utf-8")
    data = json.loads(content)

    if logo:
        if logo.content_type not in ALLOWED_IMAGE_TYPES:
            return {"status": "error", "message": "Логотип должен быть PNG, JPG или SVG"}
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        ext = Path(logo.filename).suffix.lower()
        if ext not in {".png", ".jpg", ".jpeg", ".svg"}:
            ext = ".png"
        logo_path = UPLOADS_DIR / f"logo{ext}"
        logo_path.write_bytes(logo.file.read())
        data["logo_url"] = f"/uploads/logo{ext}"

    save_brand(data)
    return {"status": "ok", "company": data.get("company"), "logo_url": data.get("logo_url")}


@app.get("/api/brandbook")
def get_brandbook():
    """Получить текущий бренд-бук."""
    return load_brand()


@app.post("/api/business-card")
def create_business_card(payload: str = Form(...)):
    """Сгенерировать визитку."""
    input_data = json.loads(payload)
    fmt = input_data.pop("_format", "png")
    path = business_card.generate(input_data, output_format=fmt)
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
    fmt = input_data.pop("_format", "pptx")
    path = presentation.generate(input_data, output_format=fmt)
    return FileResponse(path, filename=path.name)


@app.post("/api/proposal")
def create_proposal(payload: str = Form(...)):
    """Сгенерировать коммерческое предложение."""
    input_data = json.loads(payload)
    fmt = input_data.pop("_format", "docx")
    path = proposal.generate(input_data, output_format=fmt)
    return FileResponse(path, filename=path.name)
