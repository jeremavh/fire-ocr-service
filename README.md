# Fire OCR Service

Micro-service OCR pour le projet Fire.

- Framework : FastAPI
- OCR : Tesseract (fra+eng)
- Endpoint de santé : `GET /health`
- Endpoint OCR : `POST /ocr` (multipart/form-data, champ `file`)

## Variables d'environnement

- `OCR_LANG` (optionnel) : langues tesseract, ex `fra+eng` (défaut).
