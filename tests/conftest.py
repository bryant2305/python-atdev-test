# tests/conftest.py
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Agregar el directorio src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_csv_data():
    return b"""full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period
John Doe,john@example.com,Developer,100,200,150,50,5000,4500,4000,2023-04"""