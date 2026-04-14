# Usa una imagen ligera de Python
FROM python:3.9-slim

# Crea una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu computadora al contenedor
COPY requirements.txt .
COPY app.py .

# Instala las librerías
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usa tu app
EXPOSE 80

# Comando para iniciar la app
CMD ["python", "app.py"]
