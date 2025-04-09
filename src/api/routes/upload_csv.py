from fastapi import APIRouter, UploadFile, File, Depends, Path
from src.auth.auth import authenticate
from src.services.csv_processor import parse_csv
from src.services.pdf_generator import generate_pdf
from src.services.email_sender import send_email
from src.services.translator import get_translation
from datetime import datetime

router = APIRouter()
@router.post("/upload/{country_code}/{company}")
async def upload_csv(
    file: UploadFile = File(...),
    country_code: str = Path(..., regex="^(do|en|usa)$"),
    company: str = Path(...),
    username: str = Depends(authenticate)
):
    country_config = {
        "do": {"language": "es", "country_name": "República Dominicana", "currency": "RD$"},
        "usa": {"language": "en", "country_name": "USA", "currency": "$"},
        "en": {"language": "en", "country_name": "USA", "currency": "$"}
    }

    data = await file.read()
    employees = parse_csv(data, country_code)
    
    i18n = get_translation(country_config[country_code]["language"])

    response = []
    for emp in employees:
        pdf_path = generate_pdf(
            emp,
            country=country_code,
            company=company,
            currency=country_config[country_code]["currency"],
            labels=i18n["pdf"]
        )
        send_email(emp.email, i18n["email"]["subject"], i18n["email"]["body"], pdf_path)
        response.append({
            "email": emp.email,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    return {"status": "success", "sent": response}
