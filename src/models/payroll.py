from pydantic import BaseModel, EmailStr
from typing import Optional

class Employee(BaseModel):
    full_name: str
    email: str
    position: str
    health_discount_amount: float
    social_discount_amount: float
    taxes_discount_amount: float
    other_discount_amount: float
    gross_salary: float
    gross_payment: float
    net_payment: float
    period: str
