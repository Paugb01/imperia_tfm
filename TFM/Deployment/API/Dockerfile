# Utilizar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY app2.py /app/
COPY xgb_model_v3.pkl /app/
COPY scaler_v3.pkl /app/
COPY ordinal_encoder_v3.pkl /app/
COPY requirements.txt /app/
COPY pakotinaikos-5b1bb10e7834.json /app/credentials-file.json  

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Establecer la variable de entorno para las credenciales de Google Cloud
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials-file.json"

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app2:app", "--host", "0.0.0.0", "--port", "8000"]
