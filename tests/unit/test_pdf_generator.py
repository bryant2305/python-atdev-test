import os
from pathlib import Path
from src.services.pdf_generator import generate_pdf
from src.models.payroll import Employee

# tests/unit/test_pdf_generator.py
def test_pdf_generation(tmp_path):
    employee = Employee(
        full_name="John Doe",
        email="john@example.com",
        position="Developer",
        health_discount_amount=100.0,
        social_discount_amount=200.0,
        taxes_discount_amount=150.0,
        other_discount_amount=50.0,
        gross_salary=5000.0,
        gross_payment=4700.0,
        net_payment=4300.0,
        period="2023-04",
        language="en"
    )

    labels = {
        "employee_info": "Employee Info",
        "name": "Name:",
        "position": "Position:",
        "period": "Period:",
        "payment_details": "Payment Details",
        "gross_salary": "Gross Salary",
        "gross_payment": "Gross Payment",
        "net_payment": "Net Payment",
        "deductions": "Deductions",
        "health": "Health",
        "social": "Social",
        "taxes": "Taxes",
        "others": "Others",
        "footer": "Footer Text"
    }

    pdf_path = generate_pdf(employee, "usa", "testco", "$", labels)

    # Verificar
    assert Path(pdf_path).exists()
    assert os.path.getsize(pdf_path) > 0
    os.unlink(pdf_path)  # Limpiar
