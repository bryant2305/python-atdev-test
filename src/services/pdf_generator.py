from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tempfile
from src.models.payroll import Employee

def generate_pdf(employee: Employee, country: str, company: str, currency: str) -> str:
    """Genera un PDF profesional con logo de la compañía"""
    
    styles = getSampleStyleSheet()
    width, height = LETTER
    margin = 50
    line_height = 20
    
    # Rutas de assets
    logo_path = Path(f"src/assets/logos/{company.lower()}_logo.png")
    if not logo_path.exists():
        logo_path = Path(f"src/assets/logos/{company.lower()}_logo.jpeg")

    # Crear PDF temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        c = canvas.Canvas(tmp.name, pagesize=LETTER)
        
        # ===== CABECERA =====
        y_position = height - margin

        # Logo
        if logo_path.exists():
            logo_width = 120
            logo_height = 40
            c.drawImage(str(logo_path), margin, y_position - logo_height, width=logo_width, height=logo_height, preserveAspectRatio=True)
            y_position -= (logo_height + 20)
        else:
            c.setFont("Helvetica-Bold", 18)
            c.drawString(margin, y_position - 40, company.upper())
            y_position -= 60
        
        # Información de la compañía
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.darkgray)
        c.drawString(margin, y_position - 20, "Tel: (123) 456-7890")
        c.drawString(margin, y_position - 40, "Email: info@compania.com")
        c.drawString(margin, y_position - 60, "Dirección: Calle Principal #123")
        
        # ===== INFORMACIÓN DEL EMPLEADO =====
        y_position -= 100
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(margin, y_position, "INFORMACIÓN DEL EMPLEADO")
        
        y_position -= 30
        c.setFont("Helvetica", 12)
        employee_info = [
            ("Nombre:", employee.full_name),
            ("Posición:", employee.position),
            ("Email:", employee.email),
            ("Período:", employee.period)
        ]
        
        for label, value in employee_info:
            c.drawString(margin + 20, y_position, f"{label:15} {value}")
            y_position -= line_height
        
        # ===== DETALLES DE PAGO =====
        y_position -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "DETALLES DE PAGO")
        
        y_position -= 30
        payment_details = [
            ("Salario Bruto", employee.gross_salary),
            ("Pago Bruto", employee.gross_payment),
            ("Pago Neto", employee.net_payment)
        ]
        
        c.setFont("Helvetica", 12)
        for label, amount in payment_details:
            formatted = f"{currency} {amount:,.2f}"
            c.drawString(margin + 20, y_position, f"{label:20} {formatted:>15}")
            y_position -= line_height
        
        # ===== DESCUENTOS =====
        y_position -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "DESCUENTOS")
        
        y_position -= 30
        discounts = [
            ("Salud", employee.health_discount_amount),
            ("Seguridad Social", employee.social_discount_amount),
            ("Impuestos", employee.taxes_discount_amount),
            ("Otros", employee.other_discount_amount)
        ]
        
        c.setFont("Helvetica", 12)
        for label, amount in discounts:
            formatted = f"{currency} {amount:,.2f}"
            c.drawString(margin + 20, y_position, f"{label:20} {formatted:>15}")
            y_position -= line_height
        
        # Footer
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, 40, "Documento generado automáticamente - Todos los derechos reservados")
        
        c.save()
        
        return tmp.name
