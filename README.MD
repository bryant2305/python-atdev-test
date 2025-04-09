# Payroll Paystubs API

API para generación y envío de recibos de nómina automatizados con soporte multi-país y multi-compañía.

## 🚀 Características

- Generación de PDFs con diseño profesional
- Envío automático por email
- Soporte para múltiples países (USA, República Dominicana)
- Configuración por compañía (logos, datos de contacto)
- Sistema de traducciones integrado
- Procesamiento de archivos CSV

## 🛠 Tecnologías

- Python 3.11+
- FastAPI
- ReportLab (PDF generation)
- Docker
- pytest (Testing)
- SMTP (Email sending)

## 📦 Instalación

### Requisitos previos
- Docker 20.10+
- Python 3.11+ (opcional para desarrollo local)
- pipenv (recomendado)

```bash
git clone https://github.com/bryant2305/python-atdev-test.git
cd python-atdev-test
```
### Construir la imagen:

docker build --no-cache -t python-paystubs .

### Ejecutar el contenedor:

docker run -d -p 8000:8000 --env-file .env python-paystubs

### Crear archivo .env:

SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=your_password
DEBUG=false

### 🧪 Ejecución de Tests

# Instalar dependencias de testing
pip install -r test_requirements.txt

# Ejecutar todos los tests
pytest tests/ -v

### Ejemplo con curl:

curl --location 'http://localhost:8000/api/upload/usa/atdev' \
--header 'Authorization: Basic YWRtaW46c3VwZXJzZWN1cmU=' \
--form 'file=@"/Users/bryantperez/Downloads/Copy of encoded-nomina.csv"'