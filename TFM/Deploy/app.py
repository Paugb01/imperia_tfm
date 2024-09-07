import pickle
import pandas as pd
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

# Crear la aplicación FastAPI
app = FastAPI()

# Definir el modelo de datos para la entrada de la API
class InputData(BaseModel):
    Id_Producto: str
    Cliente: str
    Punto_de_Venta: int
    Mes: int
    Año: int

@app.post("/predict")
def predict_sales(data: InputData):
    try:
        # Generar características aleatorias para Id_Producto
        producto_data = {
            "Id_Producto": data.Id_Producto,
            "Familia": random.choice(["Electrónica", "Alimentos", "Ropa", "Muebles"]),
            "Subfamilia": random.choice(["Televisores", "Bebidas", "Camisas", "Sillas"]),
            "Formato": random.choice(["Grande", "Mediano", "Pequeño"]),
            "Precio": round(random.uniform(10, 1000), 2),
            "Margen": round(random.uniform(0.1, 0.5), 2),
            "Cliente_Objetivo": random.choice(["Jóvenes", "Adultos", "Niños"]),
            "Color": random.choice(["Rojo", "Azul", "Verde", "Negro"]),
            "Material": random.choice(["Plástico", "Metal", "Algodón"]),
            "Peso": round(random.uniform(0.5, 10.0), 2),
            "Tamaño": random.choice(["Pequeño", "Mediano", "Grande"]),
            "Marca": random.choice(["Marca A", "Marca B", "Marca C"]),
            "País_Origen": random.choice(["España", "China", "EE.UU", "Alemania"]),
            "Ventas_Base": random.randint(100, 10000)
        }

        # Generar características aleatorias para Cliente
        cliente_data = {
            "Cliente": data.Cliente,
            "Facturación_Total": round(random.uniform(10000, 1000000), 2),
            "Canal_de_Ventas": random.choice(["Online", "Físico"]),
            "Numero_Puntos_de_Venta": random.randint(1, 50),
            "Región": random.choice(["Norte", "Sur", "Este", "Oeste"]),
            "Segmento": random.choice(["Premium", "Económico", "Estándar"]),
            "Antigüedad": random.randint(1, 50)
        }

        # Generar características aleatorias para Punto de venta
        punto_de_venta_data = {
            "Cliente": data.Cliente,
            "Punto_de_Venta": data.Punto_de_Venta,
            "Población_500m": random.randint(1000, 50000),
            "Población_2km": random.randint(5000, 200000),
            "Puntos_de_Venta_Cercanos": random.randint(1, 20),
            "Aparcamiento": random.choice(["Sí", "No"]),
            "Accesibilidad": random.choice(["Buena", "Regular", "Mala"]),
            "Horas_Operación": random.choice(["24h", "12h", "8h"]),
            "Tipo_Zona": random.choice(["Urbana", "Suburbana", "Rural"])
        }

        # Simular predicción de ventas
        predicted_sales = round(random.uniform(1000, 100000), 2)

        # Generar la evolución de ventas de los últimos 6 meses
        fecha_actual = datetime(data.Año, data.Mes, 1)
        meses_anteriores = [(fecha_actual - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(1, 7)][::-1]
        ventas_anteriores = [round(random.uniform(500, 10000), 2) for _ in range(6)]

        # Combinar todos los datos en un solo diccionario
        resultado = {
            "Producto": producto_data,
            "Cliente": cliente_data,
            "Punto_de_Venta": punto_de_venta_data,
            "Predicción_Ventas": predicted_sales,
            "Histórico_Ventas": {
                "Meses": meses_anteriores,
                "Ventas": ventas_anteriores
            }
        }

        return resultado

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in prediction: {e}")
