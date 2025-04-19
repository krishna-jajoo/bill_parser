import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from tempfile import NamedTemporaryFile
from src.parser_processing.parser import extract_fields_from_bill
from src.utils import encode_image

app = FastAPI()

# Set base directory relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct path for templates and static
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount(
    "/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static"
)


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "result": None}
    )


@app.post("/upload/", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    # Define upload path
    upload_dir = os.path.join(BASE_DIR, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    # Save file to static/uploads so it can be served
    filename = file.filename
    save_path = os.path.join(upload_dir, filename)

    with open(save_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)

    try:
        # Encode and extract fields
        encoded_image = encode_image(save_path)
        result = extract_fields_from_bill(encoded_image, model_name="gpt-4o")
    except Exception as e:
        result = {"error": str(e)}

    image_url = f"/static/uploads/{filename}"

    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "result": result, "image_url": image_url}
    )


if __name__ == "__main__":
    uvicorn.run("src.ui.main:app", reload=True)
