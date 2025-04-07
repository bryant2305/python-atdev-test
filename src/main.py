from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import router as api_router # type: ignore

load_dotenv()

app = FastAPI(
    title="Paystub Generator API",
    description="API para procesar nóminas y enviar comprobantes de pago por correo.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rutas
app.include_router(api_router, prefix="/api")
