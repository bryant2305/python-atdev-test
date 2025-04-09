import pytest
from src.services.csv_processor import parse_csv
from src.models.payroll import Employee

def test_parse_csv_valid_data(sample_csv_data):
    employees = parse_csv(sample_csv_data, "usa")
    assert len(employees) == 1
    assert isinstance(employees[0], Employee)
    assert employees[0].email == "john@example.com"

# tests/unit/test_csv_processor.py
def test_parse_csv_invalid_data():
    invalid_data = b"invalid_header1,invalid_header2\nvalue1,value2"
    with pytest.raises(ValueError) as exc_info:
        parse_csv(invalid_data, "usa")
    assert "Invalid CSV headers" in str(exc_info.value)
    
def test_country_specific_parsing():
    data = b"""full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period
Maria,maria@example.com,Designer,50,100,75,25,3000,2800,2500,2023-04"""
    
    employees_do = parse_csv(data, "do")
    employees_usa = parse_csv(data, "usa")
    
    # Verificar lógicas específicas por país
    assert employees_do[0].gross_salary == 3000
    assert employees_usa[0].gross_salary == 3000
    
    