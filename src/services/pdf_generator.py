from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import tempfile
from src.models.payroll import Employee


def generate_pdf(employee: Employee, country: str, company_name: str) -> str:
    language = "en" if country.lower() == "usa" else "es"

    translations = {
        "en": {
            "title": "Payroll Stub",
            "employee": "Employee",
            "position": "Position",
            "period": "Period",
            "gross_salary": "Gross Salary",
            "gross_payment": "Gross Payment",
            "net_payment": "Net Payment",
            "discounts": "Discounts",
            "health": "Health",
            "social": "Social",
            "taxes": "Taxes",
            "others": "Other"
        },
        "es": {
            "title": "Comprobante de Nómina",
            "employee": "Empleado",
            "position": "Puesto",
            "period": "Período",
            "gross_salary": "Salario Bruto",
            "gross_payment": "Pago Bruto",
            "net_payment": "Pago Neto",
            "discounts": "Descuentos",
            "health": "Salud",
            "social": "Seguridad Social",
            "taxes": "Impuestos",
            "others": "Otros"
        }
    }

    t = translations[language]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        c = canvas.Canvas(tmp.name, pagesize=LETTER)
        width, height = LETTER
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, f"{t['title']} - {company_name}")

        c.setFont("Helvetica", 12)
        y -= 40
        c.drawString(50, y, f"{t['employee']}: {employee.full_name}")
        y -= 20
        c.drawString(50, y, f"Email: {employee.email}")
        y -= 20
        c.drawString(50, y, f"{t['position']}: {employee.position}")
        y -= 20
        c.drawString(50, y, f"{t['period']}: {employee.period}")

        y -= 30
        c.drawString(50, y, f"{t['gross_salary']}: ${employee.gross_salary:,.2f}")
        y -= 20
        c.drawString(50, y, f"{t['gross_payment']}: ${employee.gross_payment:,.2f}")
        y -= 20
        c.drawString(50, y, f"{t['net_payment']}: ${employee.net_payment:,.2f}")

        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, t["discounts"])
        c.setFont("Helvetica", 12)
        y -= 20
        c.drawString(50, y, f"{t['health']}: ${employee.health_discount_amount:,.2f}")
        y -= 20
        c.drawString(50, y, f"{t['social']}: ${employee.social_discount_amount:,.2f}")
        y -= 20
        c.drawString(50, y, f"{t['taxes']}: ${employee.taxes_discount_amount:,.2f}")
        y -= 20
        c.drawString(50, y, f"{t['others']}: ${employee.other_discount_amount:,.2f}")

        c.save()
        return tmp.name
