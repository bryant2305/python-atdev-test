from fastapi import APIRouter, UploadFile, File, Depends
from src.utils.auth import authenticate
from src.services.csv_processor import parse_csv
from src.services.pdf_generator import generate_pdf
from src.services.email_sender import send_email
from src.services.translator import get_translation
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), username: str = Depends(authenticate)):
    data = await file.read()
    employees = parse_csv(data)
    response = []

    for emp in employees:
        pdf_path = generate_pdf(emp, emp.language)
        i18n = get_translation(emp.language)
        send_email(emp.email, i18n["subject"], i18n["body"], pdf_path)
        response.append({
            "email": emp.email,
            "timestamp": datetime.utcnow().isoformat()
        })

    return {"status": "success", "sent": response}
