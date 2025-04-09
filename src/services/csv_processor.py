import csv
from typing import List
from io import StringIO
from src.models.payroll import Employee  # type: ignore
def parse_csv(file_data: bytes, country: str) -> List[Employee]:
    decoded = file_data.decode("utf-8-sig")
    reader = csv.DictReader(StringIO(decoded))

    if not reader.fieldnames:
        raise ValueError("CSV file is missing headers")

    # Limpia los headers
    reader.fieldnames = [field.strip().strip('"').strip('\ufeff') for field in reader.fieldnames]

    required_headers = [
        "full_name", "email", "position", "health_discount_amount",
        "social_discount_amount", "taxes_discount_amount",
        "other_discount_amount", "gross_salary", "gross_payment",
        "net_payment", "period"
    ]

    for field in required_headers:
        if field not in reader.fieldnames:
            raise ValueError("Invalid CSV headers")

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
            language=language
        ))
    return employees
