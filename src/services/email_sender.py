import os
import smtplib
from email.message import EmailMessage
from fastapi import HTTPException
from src.config.settings import settings

def send_email(to_email: str, subject: str, body: str, attachment_path: str) -> None:
    """
    Envía un correo electrónico con un archivo adjunto.
    
    Args:
        to_email (str): Correo del destinatario.
        subject (str): Asunto del correo.
        body (str): Cuerpo del correo.
        attachment_path (str): Ruta del archivo PDF a adjuntar.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg.set_content(body)

    # Adjuntar PDF
    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(attachment_path)
        )
    
    try:
        # Conexión SMTP con SSL (puerto 465)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            print("Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error SMTP: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al enviar el correo electrónico. Verifica la configuración del servidor SMTP."
        )
    