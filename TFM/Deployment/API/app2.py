from google.cloud import bigquery
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
import joblib
import pandas as pd

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

    # Consulta principal
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
    df_results = results.to_dataframe()
    # Si no hay resultados, ejecutamos las queries adicionales
    if df_results.empty:
        try:
            # Primera query para obtener características del producto
            #print("Ejecutando query1")
            query1 = """
                SELECT *
                FROM `pakotinaikos.tfm_dataset.caracteristicas_productos`
                WHERE Id_Producto = @id_producto
            """
            
            job_config1 = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("id_producto", "STRING", id_producto)
                ]
            )
            
            query_job1 = client.query(query1, job_config=job_config1)
            df1 = query_job1.result().to_dataframe()
            #print("Resultado query1:", df1.shape)

            # Segunda query para obtener los datos restantes
            #print("Ejecutando query2")
            query2 = """
                SELECT *
                FROM `pakotinaikos.tfm_dataset.set_testeo`
                WHERE Cliente = @cliente AND Punto_de_Venta = @punto_de_venta
                LIMIT 1
            """
            
            job_config2 = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("cliente", "STRING", cliente),
                    bigquery.ScalarQueryParameter("punto_de_venta", "INT64", punto_de_venta)
                ]
            )
            
            query_job2 = client.query(query2, job_config=job_config2)
            df2 = query_job2.result().to_dataframe()
            #print("Resultado query2:", df2.shape)

            # Desechar columnas no deseadas
            columns_to_keep = [
                'Cliente', 'Punto_de_Venta', 'Facturación_Total', 'Canal_de_Ventas', 'Numero_Puntos_de_Venta',
                'Región', 'Segmento', 'Antigüedad', 'Población_500m', 'Población_2km', 'Puntos_de_Venta_Cercanos',
                'Aparcamiento', 'Accesibilidad', 'Horas_Operación', 'Tipo_Zona', 'Historico 2023-01', 'Historico 2023-02', 'Historico 2023-03', 
                'Historico 2023-04', 'Historico 2023-05', 'Historico 2023-06', 
                'Historico 2023-07', 'Historico 2023-08', 'Historico 2023-09', 
                'Historico 2023-10', 'Historico 2023-11', 'Historico 2023-12', 
                'Historico 2024-1', 'Historico 2024-2', 'Historico 2024-3'
            ]
            df2 = df2[columns_to_keep]

            # Rellenar los históricos con 0
            historicos_cols = [col for col in df2.columns if 'Historico' in col]
            df2[historicos_cols] = 0

            # Combinar los resultados de las dos queries
            combined_df = pd.concat([df1, df2], axis=1)
            #print("DataFrame combinado:", combined_df.shape)
            #print(combined_df.head())

            # Reordenar las columnas para mantener el orden esperado
            expected_order = [
                'Id_Producto', 'Cliente', 'Punto_de_Venta', 'Familia', 'Subfamilia', 'Formato', 'Precio', 'Margen', 
                'Cliente_Objetivo', 'Color', 'Material', 'Peso', 'Tamaño', 'Marca', 'País_Origen', 'Ventas_Base', 
                'Facturación_Total', 'Canal_de_Ventas', 'Numero_Puntos_de_Venta', 'Región', 'Segmento', 'Antigüedad', 
                'Población_500m', 'Población_2km', 'Puntos_de_Venta_Cercanos', 'Aparcamiento', 'Accesibilidad', 
                'Horas_Operación', 'Tipo_Zona', 'Historico 2023-01', 'Historico 2023-02', 'Historico 2023-03', 
                'Historico 2023-04', 'Historico 2023-05', 'Historico 2023-06', 
                'Historico 2023-07', 'Historico 2023-08', 'Historico 2023-09', 
                'Historico 2023-10', 'Historico 2023-11', 'Historico 2023-12', 
                'Historico 2024-1', 'Historico 2024-2', 'Historico 2024-3'
            ]

            df_results = combined_df[expected_order]
        
        except Exception as e:
            print("Error en las consultas adicionales:", e)
            raise HTTPException(status_code=500, detail=f"Error en las consultas adicionales: {str(e)}")

    return df_results

def get_additional_data(id_producto: str):
    project_id = "pakotinaikos"
    client = bigquery.Client(project=project_id)

    # Consulta 1: Distribución de ventas por canal
    query_ventas = f"""
        SELECT Canal_de_Ventas, SUM(Ventas_Base) AS Ventas_Base_Total
        FROM `pakotinaikos.tfm_dataset.set_testeo`
        WHERE Id_Producto = '{id_producto}'
        GROUP BY Canal_de_Ventas
    """
    df_ventas = client.query(query_ventas).result().to_dataframe()

    # Consulta 2: Precio medio del producto
    query_precio = f"""
        SELECT Id_Producto, AVG(Precio) AS Precio_Medio
        FROM `pakotinaikos.tfm_dataset.set_testeo`
        WHERE Id_Producto = '{id_producto}'
        GROUP BY Id_Producto
    """
    df_precio = client.query(query_precio).result().to_dataframe()

    # Consulta 3: Tendencia del histórico de ventas
    query_tendencia = f"""
        SELECT Id_Producto, 
            SUM(`Historico 2023-01`) AS `Historico 2023-01`, 
            SUM(`Historico 2023-02`) AS `Historico 2023-02`, 
            SUM(`Historico 2023-03`) AS `Historico 2023-03`, 
            SUM(`Historico 2023-04`) AS `Historico 2023-04`, 
            SUM(`Historico 2023-05`) AS `Historico 2023-05`, 
            SUM(`Historico 2023-06`) AS `Historico 2023-06`, 
            SUM(`Historico 2023-07`) AS `Historico 2023-07`, 
            SUM(`Historico 2023-08`) AS `Historico 2023-08`, 
            SUM(`Historico 2023-09`) AS `Historico 2023-09`, 
            SUM(`Historico 2023-10`) AS `Historico 2023-10`, 
            SUM(`Historico 2023-11`) AS `Historico 2023-11`, 
            SUM(`Historico 2023-12`) AS `Historico 2023-12`, 
            SUM(`Historico 2024-1`) AS `Historico 2024-1`, 
            SUM(`Historico 2024-2`) AS `Historico 2024-2`
        FROM `pakotinaikos.tfm_dataset.set_testeo`
        WHERE Id_Producto = '{id_producto}'
        GROUP BY Id_Producto
    """
    df_tendencia = client.query(query_tendencia).result().to_dataframe()

    return df_ventas, df_precio, df_tendencia



@app.post("/predict")
def predict_sales(data: InputData):
    try:
        # Obtener los datos del producto desde BigQuery
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

        # Consultar los datos adicionales
        df_ventas, df_precio, df_tendencia = get_additional_data(data.Id_Producto)

        # Convertir los DataFrames adicionales a diccionarios para incluirlos en la respuesta
        ventas_data = df_ventas.to_dict(orient='records')
        precio_data = df_precio.to_dict(orient='records')
        tendencia_data = df_tendencia.to_dict(orient='records')

        # Convertir el DataFrame original a un diccionario y luego a JSON
        resultado_original = df_original.to_dict(orient='records')

        # Retornar la respuesta con los datos originales, predicción y datos adicionales
        return {
            "data": resultado_original,
            "Predicción_Ventas": prediccion_ventas,
            "Distribucion_Ventas": ventas_data,
            "Precio_Medio": precio_data,
            "Tendencia_Historico": tendencia_data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in prediction: {e}")

@app.get("/api")
def read_root():
    return {"message": "API is working."}