import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# URL de la API (asegúrate de que la API esté ejecutándose en esta URL)
API_URL = "http://localhost:8000/predict"

# URL de la imagen del producto
PRODUCT_IMAGE_URL = "https://pacolorente.es/wp-content/uploads/2022/07/simpleIV.jpg"

# Título de la aplicación
st.title("Predictor de Ventas")

# Entrada de datos del usuario
st.header("Datos de Entrada")

id_producto = st.text_input("Id del Producto")
cliente = st.text_input("Cliente")
punto_de_venta = st.number_input("Punto de Venta", min_value=1)
mes = st.number_input("Mes", min_value=1, max_value=12)
año = st.number_input("Año", min_value=2000, max_value=2100)

# Botón para hacer la predicción
if st.button("Predecir Ventas"):
    # Verificar que los campos requeridos no estén vacíos
    if id_producto and cliente and punto_de_venta and mes and año:
        # Crear el diccionario con los datos de entrada
        input_data = {
            "Id_Producto": id_producto,
            "Cliente": cliente,
            "Punto_de_Venta": punto_de_venta,
            "Mes": mes,
            "Año": año
        }

        # Enviar solicitud POST a la API
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            # Obtener la respuesta y mostrar los resultados
            result = response.json()
            st.header("Resultados")
            
            # Mostrar datos del producto
            st.subheader("Descripción del producto")
            st.image(PRODUCT_IMAGE_URL, caption=f"Producto: {id_producto}")
            st.json(result["Producto"])
            
            # Mostrar datos del cliente
            st.subheader("Datos del cliente")
            st.json(result["Cliente"])
            
            # Mostrar datos del punto de venta
            st.subheader("Punto de Venta")
            st.json(result["Punto_de_Venta"])
            
            # Mostrar predicción de ventas
            st.subheader("Predicción de Ventas")
            st.write(f"Predicción de Ventas: {result['Predicción_Ventas']}")

            # Crear una gráfica con la evolución de las ventas
            st.subheader("Evolución de Ventas")
            historico_meses = result["Histórico_Ventas"]["Meses"]
            ventas_historicas = result["Histórico_Ventas"]["Ventas"]

            # Agregar la predicción al final del historial
            historico_meses.append(f"{año}-{str(mes).zfill(2)}")
            ventas_historicas.append(result['Predicción_Ventas'])

            # Crear un DataFrame para la serie temporal
            df = pd.DataFrame({
                "Mes": historico_meses,
                "Ventas": ventas_historicas
            })

            # Graficar la evolución de las ventas
            plt.figure(figsize=(10, 5))
            plt.plot(df["Mes"], df["Ventas"], marker='o')
            plt.title("Evolución de Ventas (Últimos 6 Meses y Predicción Actual)")
            plt.xlabel("Mes")
            plt.ylabel("Ventas")
            plt.xticks(rotation=45)
            plt.grid(True)

            # Resaltar la predicción actual
            plt.scatter(df["Mes"].iloc[-1], df["Ventas"].iloc[-1], color='red', label='Predicción Actual')
            plt.legend()

            st.pyplot(plt)

            MI_IMAGEN = "./dash1.jpg"
            st.image(MI_IMAGEN)

        else:
            st.error("Error en la API: " + response.text)
    else:
        st.error("Por favor, complete todos los campos.")
