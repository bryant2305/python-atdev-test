import csv
from typing import List
from io import StringIO
from src.models.payroll import Employee # type: ignore

def parse_csv(file_data: bytes) -> List[Employee]:
    decoded = file_data.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))
    employees = []

    for row in reader:
        employees.append(Employee(
            name=row["name"],
            email=row["email"],
            position=row["position"],
            salary=float(row["salary"]),
            language=row.get("language", "es"),
            company=row.get("company", "Default Company")
        ))
    return employees
