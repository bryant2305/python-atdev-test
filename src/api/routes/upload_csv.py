from fastapi import APIRouter, UploadFile, File, Depends, Path, HTTPException
from fastapi.responses import JSONResponse
from src.auth.auth import authenticate
from src.services.csv_processor import parse_csv
from src.services.pdf_generator import generate_pdf
from src.services.email_sender import send_email
from src.services.translator import get_translation
from datetime import datetime
import logging

router = APIRouter()

@router.post("/upload/{country_code}/{company}")
async def upload_csv(
    file: UploadFile = File(..., description="Archivo CSV con datos de empleados"),
    country_code: str = Path(..., pattern="^(do|en|usa)$"),
    company: str = Path(..., description="Nombre de la compañía"),
    username: str = Depends(authenticate)
):
    # Validar tipo de archivo
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos CSV")

    try:
        data = await file.read()
        
        # Validar que el archivo no esté vacío
        if not data:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
            
        employees = parse_csv(data, country_code)
        
        country_config = {
            "do": {"language": "es", "currency": "RD$"},
            "usa": {"language": "en", "currency": "$"},
            "en": {"language": "en", "currency": "$"}
        }

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

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Formato de archivo inválido")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")