import joblib
import streamlit as st
import numpy as np
import pandas as pd

# Cargar el modelo y el preprocesador
modelo_path = 'xgb_model.pkl'
scaler_path = 'scaler.pkl'

modelo = joblib.load(modelo_path)
scaler = joblib.load(scaler_path)

# Configuración de la aplicación
st.set_page_config(
    page_title="Predicción de Ventas",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Título de la aplicación
st.title("Predicción de Ventas de Productos")
st.markdown("""
Esta aplicación predice las ventas de un producto dado un mes y un año específicos.
""")

# Inputs para el usuario
st.sidebar.header("Parámetros de entrada")
mes = st.sidebar.selectbox("Mes", list(range(1, 13)), index=0)
ano = st.sidebar.selectbox("Año", list(range(2020, 2031)), index=4)

# Función para realizar predicciones
def predecir_ventas(mes, ano):
    datos = [[mes, ano]]
    datos_transformados = scaler.transform(datos)
    prediccion = modelo.predict(datos_transformados)
    return prediccion[0]

# Botón para hacer la predicción
if st.sidebar.button("Predecir"):
    # Calcular las predicciones para los 3 meses anteriores y 3 posteriores
    resultados = []
    fechas = []
    
    for i in range(-3, 4):
        mes_pred = mes + i
        ano_pred = ano
        
        # Ajuste del mes y año en caso de que el mes sea menor que 1 o mayor que 12
        if mes_pred < 1:
            mes_pred += 12
            ano_pred -= 1
        elif mes_pred > 12:
            mes_pred -= 12
            ano_pred += 1
        
        prediccion = predecir_ventas(mes_pred, ano_pred)
        resultados.append(prediccion)
        fechas.append(f"{ano_pred}-{mes_pred:02d}")
    
    # Crear un DataFrame para el gráfico
    df_predicciones = pd.DataFrame({
        "Fecha": fechas,
        "Predicción": resultados
    })

    # Mostrar los resultados
    st.subheader("Resultados de la predicción")
    st.write(f"**Predicción para Mes:** {mes} **Año:** {ano}")
    st.write(f"**Predicción de ventas:** {resultados[3]:.2f} unidades")

    # Mostrar el gráfico de la tendencia
    st.subheader("Tendencia de Predicción")
    st.line_chart(df_predicciones.set_index('Fecha')['Predicción'])

# Footer
st.markdown("---")
st.write("Desarrollado por Pakotinaikos. Powered by Streamlit.")
