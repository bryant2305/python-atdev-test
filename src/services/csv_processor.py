import csv
from typing import List
from io import StringIO
from src.models.payroll import Employee  # type: ignore

def parse_csv(file_data: bytes, country: str) -> List[Employee]:
    decoded = file_data.decode("utf-8-sig")  # Usa utf-8-sig para eliminar el BOM
    reader = csv.DictReader(StringIO(decoded))
    
    # Limpia los headers: remueve \ufeff y comillas
    reader.fieldnames = [field.strip().strip('"').strip('\ufeff') for field in reader.fieldnames]
    print("Headers limpios:", reader.fieldnames)  # Debug
    
    employees = []
    for row in reader:
        language = "en" if country.lower() == "usa" else "es"
        employees.append(Employee(
            full_name=row["full_name"].strip(),
            email=row["email"].strip(),
            position=row["position"].strip(),
            health_discount_amount=float(row["health_discount_amount"]),
            social_discount_amount=float(row["social_discount_amount"]),
            taxes_discount_amount=float(row["taxes_discount_amount"]),
            other_discount_amount=float(row["other_discount_amount"]),
            gross_salary=float(row["gross_salary"]),
            gross_payment=float(row["gross_payment"]),
            net_payment=float(row["net_payment"]),
            period=row["period"].strip(),
            language=language  # Asigna el idioma basado en el parámetro `country`
        ))
    return employees
