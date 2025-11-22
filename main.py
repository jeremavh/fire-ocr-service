from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import os

app = FastAPI(title="Fire OCR Service", version="1.0.0")

# Langue OCR par défaut (français + anglais)
OCR_LANG = os.getenv("OCR_LANG", "fra+eng")


@app.get("/health")
def health():
    return {"status": "ok", "ocr_lang": OCR_LANG}


@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    """
    Reçoit une image (PNG/JPG) et renvoie le texte OCR.

    Appel typique depuis ton app principale :
      - POST multipart/form-data
      - champ 'file' contenant la page à OCRiser
    """
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Fichier vide")

        # Charger l'image avec PIL
        try:
            image = Image.open(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Image invalide: {e}")

        # OCR
        try:
            text = pytesseract.image_to_string(image, lang=OCR_LANG) or ""
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OCR error: {e}")

        return JSONResponse({"text": text})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
