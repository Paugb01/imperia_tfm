from google.cloud import bigquery
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler

app = FastAPI()

# Cargar el modelo y los objetos de preprocesamiento
model = joblib.load("xgb_model_v3.pkl")
scaler = joblib.load("scaler_v3.pkl")
ordinal_encoder = joblib.load("ordinal_encoder_v3.pkl")

class InputData(BaseModel):
    Id_Producto: str
    Cliente: str
    Punto_de_Venta: int
    Mes: int
    Año: int

def get_data_from_bigquery(id_producto: str, cliente: str, punto_de_venta: int):
    project_id = "pakotinaikos"
    client = bigquery.Client(project=project_id)

    query = """
        SELECT * FROM `pakotinaikos.tfm_dataset.set_testeo`
        WHERE Id_Producto = @id_producto AND Cliente = @cliente AND Punto_de_Venta = @punto_de_venta
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_producto", "STRING", id_producto),
            bigquery.ScalarQueryParameter("cliente", "STRING", cliente),
            bigquery.ScalarQueryParameter("punto_de_venta", "INT64", punto_de_venta)
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    return results.to_dataframe()

@app.post("/predict")
def predict_sales(data: InputData):
    try:
        df = get_data_from_bigquery(data.Id_Producto, data.Cliente, data.Punto_de_Venta)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No se encontraron datos para los parámetros proporcionados.")
        
        # Guardar una copia del DataFrame original para la respuesta
        df_original = df.copy()

        # Definir el orden esperado de las columnas
        expected_feature_order = ['Historico 2023-01', 'Historico 2023-02', 'Historico 2023-03', 
                                  'Historico 2023-04', 'Historico 2023-05', 'Historico 2023-06', 
                                  'Historico 2023-07', 'Historico 2023-08', 'Historico 2023-09', 
                                  'Historico 2023-10', 'Historico 2023-11', 'Historico 2023-12', 
                                  'Historico 2024-1', 'Id_Producto', 'Cliente', 'Familia', 
                                  'Punto_de_Venta', 'Precio', 'Margen', 'Facturación_Total', 
                                  'Antigüedad', 'Ventas_Base', 'Población_500m', 'Población_2km', 
                                  'Puntos_de_Venta_Cercanos']

        # Asegurarse de que el DataFrame contenga solo las columnas esperadas
        df = df[expected_feature_order]
        
        # Llenar valores faltantes (si es necesario)
        df = df.fillna(0)

        # Separar las columnas numéricas y categóricas
        numeric_cols = ['Precio', 'Margen', 'Facturación_Total', 'Antigüedad', 
                        'Ventas_Base', 'Población_500m', 'Población_2km', 'Puntos_de_Venta_Cercanos']
        categorical_cols = ['Id_Producto', 'Cliente', 'Familia', 'Punto_de_Venta']
        
        # Aplicar OrdinalEncoder y MinMaxScaler a los datos
        try:
            # Solo escalar las columnas numéricas que no son históricas
            df[numeric_cols] = scaler.transform(df[numeric_cols])
        except Exception as e:
            print("Error during numeric column scaling:", e)
            raise
        
        try:
            df[categorical_cols] = ordinal_encoder.transform(df[categorical_cols])
        except Exception as e:
            print("Error during categorical column encoding:", e)
            raise

        # Realizar la predicción de ventas
        prediction = model.predict(df)
        
        # Convertir la predicción a un tipo de dato compatible
        prediccion_ventas = round(float(prediction[0]))

        # Convertir el DataFrame original a un diccionario y luego a JSON
        resultado_original = df_original.to_dict(orient='records')

        return {"data": resultado_original,
                "Predicción_Ventas": prediccion_ventas}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in prediction: {e}")
