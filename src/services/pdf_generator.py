import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader("src/assets/templates"))

def generate_pdf(employee, lang="es") -> str:
    template = env.get_template(f"paystub_{lang}.html")
    html = template.render(employee=employee.dict())
    output_path = f"/tmp/{employee.name.replace(' ', '_')}.pdf"
    pdfkit.from_string(html, output_path)
    return output_path
