from fastapi import APIRouter, UploadFile, File, Depends, Path
from src.utils.auth import authenticate
from src.services.csv_processor import parse_csv
from src.services.pdf_generator import generate_pdf
from src.services.email_sender import send_email
from src.services.translator import get_translation
from datetime import datetime

router = APIRouter()

@router.post("/upload/{country_code}")
async def upload_csv(
    file: UploadFile = File(...),
    country_code: str = Path(..., regex="^(do|en|usa)$"),  #Solo permite "do" o "usa"
    company_name: str = "Empresa",
    username: str = Depends(authenticate)
):
    country_config = {
        "do": {"language": "es", "country_name": "República Dominicana"},
        "usa": {"language": "en", "country_name": "USA"},
        "en": {"language": "en", "country_name": "USA"}
    }
    
    data = await file.read()
    employees = parse_csv(data, country_code)
    
    response = []
    for emp in employees:
        pdf_path = generate_pdf(emp, country_code, company_name)
        i18n = get_translation(country_config[country_code]["language"])
        send_email(emp.email, i18n["subject"], i18n["body"], pdf_path)
        response.append({
            "email": emp.email,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    return {"status": "success", "sent": response}