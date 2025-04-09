import csv
import io
from src.models.payroll import Employee
from typing import List

def parse_csv(csv_data: bytes, country_code: str) -> List[Employee]:
    required_columns = {
        'full_name', 'email', 'position', 'health_discount_amount',
        'social_discount_amount', 'taxes_discount_amount', 'other_discount_amount',
        'gross_salary', 'gross_payment', 'net_payment', 'period'
    }

    # Convertir bytes a stream de texto
    text_stream = io.StringIO(csv_data.decode('utf-8-sig'))
    
    reader = csv.DictReader(text_stream)
    
    # Validar headers
    if not reader.fieldnames:
        raise ValueError("El archivo CSV no contiene encabezados válidos")
    

    cleaned_headers = [header.strip().strip('"').strip('\ufeff') for header in reader.fieldnames]
    
    
    missing_columns = required_columns - set(cleaned_headers)
    if missing_columns:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(missing_columns)}")

    employees = []
    for row_num, row in enumerate(reader, start=2):
        try:
            employees.append(Employee(
                full_name=row['full_name'],
                email=row['email'],
                position=row['position'],
                health_discount_amount=float(row['health_discount_amount']),
                social_discount_amount=float(row['social_discount_amount']),
                taxes_discount_amount=float(row['taxes_discount_amount']),
                other_discount_amount=float(row['other_discount_amount']),
                gross_salary=float(row['gross_salary']),
                gross_payment=float(row['gross_payment']),
                net_payment=float(row['net_payment']),
                period=row['period']
            ))
        except (KeyError, ValueError) as e:
            raise ValueError(f"Error en fila {row_num}: {str(e)}")

    if not employees:
        raise ValueError("El CSV no contiene datos válidos de empleados")
        
    return employees