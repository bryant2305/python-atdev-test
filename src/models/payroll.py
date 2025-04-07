from pydantic import BaseModel, EmailStr
from typing import Optional

class Employee(BaseModel):
    name: str
    email: EmailStr
    position: str
    salary: float
    language: Optional[str] = "es"
    company: Optional[str] = "Default Company"
