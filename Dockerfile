FROM python:3.11-slim

# Instalar solo las dependencias necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo requirements.txt y el código al contenedor
COPY requirements.txt /app/
WORKDIR /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto, incluyendo el archivo .env
COPY . /app/

# Asegúrate de que el archivo .env esté en el directorio correcto
RUN ls -l /app  

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
