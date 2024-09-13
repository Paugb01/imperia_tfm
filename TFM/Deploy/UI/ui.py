import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from google.cloud import bigquery


# URL de la API
API_URL = "http://34.79.144.132/predict"

PRODUCT_IMAGE_URL = "./simpleIV.jpg"

# Configuración de la página
st.set_page_config(
    page_title="Imperia : Predicción de Ventas",
    layout="centered"  # También puedes usar "centered"
)

# Ubica image.png arriba de la página y cambia el color a azul oscuro
st.image("./image.png", use_column_width=True, output_format="PNG", channels="BGR")
# Título de la aplicación
st.title("Sistema de Predicción de Ventas")

# Control de sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Función para verificar las credenciales en BigQuery
def verificar_credenciales(cliente_login, contraseña):
    # Inicializa el cliente de BigQuery
    client = bigquery.Client()

    # Consulta SQL para verificar las credenciales
    query = f"""
        SELECT COUNT(1) AS usuario_valido
        FROM `pakotinaikos.tfm_dataset.inicio_sesion`
        WHERE Cliente = '{cliente_login}' AND Contrasena = '{contraseña}'
    """

    # Ejecuta la consulta
    query_job = client.query(query)

    # Recupera los resultados
    result = query_job.result()

    # Si existe al menos un registro, las credenciales son correctas
    for row in result:
        return row.usuario_valido > 0

# Formulario de inicio de sesión
if not st.session_state.authenticated:
    cliente_login = st.text_input("Cliente")
    contraseña = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        # Verificar credenciales con BigQuery
        if cliente_login and contraseña:
            credenciales_validas = verificar_credenciales(cliente_login, contraseña)
            if credenciales_validas:
                st.session_state.authenticated = True
                st.session_state.cliente_login = cliente_login  # Guardar el cliente_login en session_state
                st.success("Inicio de sesión exitoso")
            else:
                st.error("Credenciales inválidas")
        else:
            st.error("Por favor, introduce tanto el Cliente como la Contraseña.")
else:
    # Aquí se muestra el contenido principal de la aplicación
    st.header("Datos de Entrada")
    
    id_producto = st.text_input("Id del Producto")
    cliente = st.text_input("Cliente", value=st.session_state.cliente_login)  # Usar el cliente_login guardado
    punto_de_venta = st.number_input("Punto de Venta", min_value=1)
    mes = st.number_input("Mes", min_value=1, max_value=12)
    año = st.number_input("Año", min_value=2024, max_value=2100)

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

            response = requests.post(API_URL, json=input_data)

            if response.status_code == 200:
                # Obtener la respuesta y mostrar los resultados
                result = response.json()

                st.header("Resultados")
                
                # Separar el resultado en secciones
                producto = {
                    "Id_Producto": result["data"][0]["Id_Producto"],
                    "Familia": result["data"][0]["Familia"],
                    "Subfamilia": result["data"][0]["Subfamilia"],
                    "Formato": result["data"][0]["Formato"],
                    "Precio": result["data"][0]["Precio"],
                    "Margen": result["data"][0]["Margen"],
                    "Cliente_Objetivo": result["data"][0]["Cliente_Objetivo"],
                    "Color": result["data"][0]["Color"],
                    "Material": result["data"][0]["Material"],
                    "Peso": result["data"][0]["Peso"],
                    "Tamaño": result["data"][0]["Tamaño"],
                    "Marca": result["data"][0]["Marca"],
                    "País_Origen": result["data"][0]["País_Origen"],
                    "Ventas_Base": result["data"][0]["Ventas_Base"]
                }

                cliente_info = {
                    "Cliente": result["data"][0]["Cliente"],
                    "Facturación_Total": result["data"][0]["Facturación_Total"],
                    "Canal_de_Ventas": result["data"][0]["Canal_de_Ventas"],
                    "Numero_Puntos_de_Venta": result["data"][0]["Numero_Puntos_de_Venta"],
                    "Región": result["data"][0]["Región"],
                    "Segmento": result["data"][0]["Segmento"],
                    "Antigüedad": result["data"][0]["Antigüedad"]
                }

                punto_de_venta_info = {
                    "Cliente": result["data"][0]["Cliente"],
                    "Punto_de_Venta": result["data"][0]["Punto_de_Venta"],
                    "Población_500m": result["data"][0]["Población_500m"],
                    "Población_2km": result["data"][0]["Población_2km"],
                    "Puntos_de_Venta_Cercanos": result["data"][0]["Puntos_de_Venta_Cercanos"],
                    "Aparcamiento": result["data"][0]["Aparcamiento"],
                    "Accesibilidad": result["data"][0]["Accesibilidad"],
                    "Horas_Operación": result["data"][0]["Horas_Operación"],
                    "Tipo_Zona": result["data"][0]["Tipo_Zona"]
                }

                historico_ventas = {
                    "Meses": list(result["data"][0].keys())[list(result["data"][0].keys()).index("Historico 2023-01"):],
                    "Ventas": list(result["data"][0].values())[list(result["data"][0].keys()).index("Historico 2023-01"):]
                }

                # Mostrar datos del producto
                st.image(PRODUCT_IMAGE_URL, caption=f"Producto: {id_producto}")

                st.subheader("Descripción del Producto")
                # Dividir la descripción del producto en dos tablas
                producto_1 = {k: producto[k] for i, k in enumerate(producto) if i < 7}
                producto_2 = {k: producto[k] for i, k in enumerate(producto) if i >= 7}

                col1, col2 = st.columns(2)

                with col1:
                    st.write(pd.DataFrame(list(producto_1.items()), columns=["Campo", "Valor"]).set_index("Campo"))

                with col2:
                    st.write(pd.DataFrame(list(producto_2.items()), columns=["Campo", "Valor"]).set_index("Campo"))

                # Mostrar datos del cliente y del punto de venta en paralelo
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Datos del Cliente")
                    st.write(pd.DataFrame(list(cliente_info.items()), columns=["Campo", "Valor"]).set_index("Campo"))

                with col2:
                    st.subheader("Datos del Punto de Venta")
                    st.write(pd.DataFrame(list(punto_de_venta_info.items()), columns=["Campo", "Valor"]).set_index("Campo"))
                
                st.markdown("<hr style='border: 1px solid black;'>", unsafe_allow_html=True)

                st.header("Predicción de Ventas")

                # Mostrar la predicción de ventas con fecha seleccionada
                st.success(f"🎯 Predicción ventas {str(mes).zfill(2)}/{año}: {result['Predicción_Ventas']:.2f} uds.")

                # Mostrar evolución de ventas
                historico_meses = historico_ventas["Meses"]
                ventas_historicas = historico_ventas["Ventas"]

                # Renombrar los meses para que tengan el formato deseado
                historico_meses = [mes.replace("Historico ", "").replace("-", "/") for mes in historico_meses]

                # Crear un DataFrame para la serie temporal
                df = pd.DataFrame({
                    "Mes": historico_meses,
                    "Ventas": ventas_historicas
                })

                # Agregar la predicción al final del historial
                df = pd.concat([df, pd.DataFrame({"Mes": [f"{año}/{str(mes).zfill(2)}"], "Ventas": [result["Predicción_Ventas"]]})], ignore_index=True)

                # Graficar la evolución de las ventas
                plt.figure(figsize=(10, 5))
                plt.plot(df["Mes"], df["Ventas"], marker='o', color='blue', label='Histórico de Ventas')
                plt.title("Evolución de Ventas (histórico)")
                plt.xlabel("Mes")
                plt.ylabel("Ventas")
                plt.xticks(rotation=45)
                plt.grid(True)

                # Resaltar la predicción actual en rojo
                plt.scatter(df["Mes"].iloc[-1], df["Ventas"].iloc[-1], color='red', s=100, label='Predicción Actual')
                plt.legend()

                st.pyplot(plt)

                st.markdown("<hr style='border: 1px solid #FF6347;'>", unsafe_allow_html=True)
                st.markdown("<h3>El producto en la industria</h3>", unsafe_allow_html=True)

                # Distribución de Ventas
                df_ventas = pd.DataFrame(result["Distribucion_Ventas"])

                fig, ax = plt.subplots(figsize=(6, 3))
                ax.pie(df_ventas["Ventas_Base_Total"], labels=df_ventas["Canal_de_Ventas"], autopct='%1.1f%%', startangle=90)
                ax.set_title("Nº Ventas por Canal de Ventas")
                ax.axis('equal')

                # Configurar las columnas
                col1, col2 = st.columns([1, 1])  # Puedes ajustar las proporciones

                # Mostrar el gráfico en la primera columna
                with col1:
                    st.pyplot(fig)

                # Precio Medio
                precio_medio = result["Precio_Medio"][0]["Precio_Medio"]

                # Mostrar el precio medio en grande y formateado
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <h1 style="color: #FF6347;">{precio_medio:.2f} €</h1>
                        <p style="font-size: 1em; color: #000;">Precio medio Producto {result["Precio_Medio"][0]["Id_Producto"]}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Tendencia Histórica
                historico = result["Tendencia_Historico"][0]
                meses = [f"{mes}" for mes in list(historico.keys())[1:]]
                ventas = [historico[mes] for mes in meses]

                # Convertir los nombres de los meses a un formato más legible
                meses_convertidos = [mes.replace("Historico ", "").replace("-", "/") for mes in meses]

                # Crear un DataFrame para la tendencia
                df_tendencia = pd.DataFrame({
                    "Mes": meses_convertidos,
                    "Ventas": ventas
                })

                # Graficar la tendencia de ventas
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(df_tendencia["Mes"], df_tendencia["Ventas"], marker='o', color='green', label='Tendencia de Ventas')
                ax.set_title("Tendencia de Ventas")
                ax.set_xlabel("Mes/Año")
                ax.set_ylabel("Ventas")
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True)
                ax.legend()

                st.pyplot(fig)



            else:
                st.error("Error en la API: " + response.text)
        else:
            st.error("Por favor, complete todos los campos.")