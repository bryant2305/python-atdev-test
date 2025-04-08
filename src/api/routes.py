from fastapi import APIRouter, UploadFile, File, Depends
from src.utils.auth import authenticate
from src.services.csv_processor import parse_csv
from src.services.pdf_generator import generate_pdf
from src.services.email_sender import send_email
from src.services.translator import get_translation
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), country: str = "do", company_name: str = "Empresa", username: str = Depends(authenticate)):
    data = await file.read()
    employees = parse_csv(data, country)  # Pasar `country` al procesar el CSV
    response = []

    for emp in employees:
        pdf_path = generate_pdf(emp, country, company_name)  # Usa `country` para decidir idioma
        i18n = get_translation(country)  # Traducción para el correo
        send_email(emp.email, i18n["subject"], i18n["body"], pdf_path)
        response.append({
            "email": emp.email,
            "timestamp": datetime.utcnow().isoformat()
        })

    return {"status": "success", "sent": response}