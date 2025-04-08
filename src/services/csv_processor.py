import csv
from typing import List
from io import StringIO
from src.models.payroll import Employee  # type: ignore

def parse_csv(file_data: bytes) -> List[Employee]:
    decoded = file_data.decode("utf-8-sig")  # Usa utf-8-sig para eliminar el BOM
    reader = csv.DictReader(StringIO(decoded))
    
    # Limpia los headers: remueve \ufeff y comillas
    reader.fieldnames = [field.strip().strip('"').strip('\ufeff') for field in reader.fieldnames]
    print("Headers limpios:", reader.fieldnames)  # Debug
    
    employees = []
    for row in reader:
        employees.append(Employee(
            name=row["Nombre"].strip(),
            email=row["Email"].strip(),
            position=row["Posición"].strip(),
            salary=float(row["Salario"]),
            language=row.get("Idioma", "es").strip(),
            company=row.get("Empresa", "Empresa Predeterminada").strip()
        ))
        
        
    return employees