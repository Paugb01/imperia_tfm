# imperia_tfm

### As for now TFM folder contains a very basic and provisional infrastructure that looks as follows:
- imperia_db.sql script that creates three tables for the main data provided by Imperia. Further exploration is needed. 
- Docker-compose.yml file setting up a PostgreSQL service relying on the adjacent Dockerfile.
- Dockerfile.postgres file providing the initialisation scripts and the csv files.
- A init_db.sh db intialisation file that loads the data onto the recently created tables.

#### (Moreover you will find the csv files containing the data and a python notebook)

## How to deploy the db:
Open up a new terminal inside TFM folder. (Creating a virtual environment is higly recommended atm and will become necessary soon.) Now start docker on your machine and run the following command: `docker compose up --build`
Now this should be the last message shown on your terminal screen: `postgres_container  | 2024-07-03 10:03:36.648 UTC [1] LOG:  database system is ready to accept connections`

Now you should be able to connect to the database through your SQL client, such as DBeaver or similar. Generic .env should be created, though hidden on the repo which is not as for now. Check you're using the correct environment variable values. 

### There are still few issues to address:
- The punto_venta table is not being loaded its data for problems related to the primary key.
- A way of including all the data and csv files should be found.

## Next steps:
- Connect the notebook to the database and start an EDA taking that connection as the input is the current idea.
- Find feasible or more convenient alternatives to deploying a db. Otherwise, decide and implement the DB either on cloud or on local servers according to what might be more convenient. 
  

## API Deployment (JAVI)

Link : <<http://130.211.94.98:8501>> 

## Modelo XGBoost (MIGUEL)

### 1. Carga de librerías y datos

En la primera parte del código, se realiza la carga de las librerías necesarias para el análisis y el modelado predictivo. Se utilizan las siguientes librerías:

- **pandas**: Para la manipulación y análisis de datos.
- **numpy**: Para cálculos numéricos.
- **scikit-learn**: Para el preprocesamiento de los datos, la división del dataset, y las métricas de evaluación.
- **xgboost**: Para el entrenamiento del modelo de regresión basado en XGBoost.
- **matplotlib**: Para la visualización de resultados.

Además, se carga el archivo `set_testeo_V2.csv`, que contiene las variables históricas de ventas y otras características categóricas y numéricas adicionales necesarias para el modelo.

### 2. Definir las columnas de interés

Se define un conjunto de columnas que representan las ventas históricas de enero 2023 a enero 2024, las cuales serán utilizadas como variables predictoras para el entrenamiento del modelo. 

Asimismo, se define la columna de febrero de 2024 como la variable objetivo (`target`) que el modelo intentará predecir. 

Además de las variables históricas, también se seleccionan variables categóricas como `Id_Producto`, `Cliente`, `Familia`, y `Punto_de_Venta`, y variables numéricas como `Precio`, `Margen`, y otras relacionadas con el entorno comercial.

### 3. Feature Engineering

Se implementan técnicas de ingeniería de características con el objetivo de mejorar la capacidad predictiva del modelo. Entre las técnicas exploradas se encuentran:

- **Cálculo del promedio móvil**: Se calcula el promedio móvil de los últimos 3 meses de ventas históricas, que proporciona una visión suavizada de la tendencia de ventas.
- **Interacción entre variables**: Se crea una nueva característica que es el producto entre el `Precio` y el `Margen`, lo cual permite capturar la interacción entre ambas variables y su posible influencia en las ventas futuras.

Aunque estas nuevas características fueron comentadas en el código final, el objetivo es demostrar cómo pueden crearse características adicionales relevantes para el modelo.

### 4. Preprocesamiento de datos

El preprocesamiento es una fase crucial donde se preparan los datos para el entrenamiento del modelo:

- Se reemplazan los valores faltantes (`NaN`) en las columnas históricas por 0. Esta operación asegura que no haya valores faltantes que puedan afectar negativamente el modelo.
- Se definen las variables predictoras (X) y la variable objetivo (y).
- Las variables categóricas se transforman en valores numéricos utilizando el `OrdinalEncoder`. De esta forma, el modelo puede interpretar correctamente la información categórica.
- Se verifica que las variables categóricas han sido correctamente convertidas a tipo numérico para su uso en el modelo de predicción.

### 5. Eliminación de outliers

Para mejorar la calidad de los datos, se eliminan los valores atípicos o outliers. La técnica empleada es el rango intercuartílico (IQR), que identifica y filtra los datos que se encuentran fuera de 1.5 veces el IQR. Esto se aplica tanto a las columnas históricas como a las variables numéricas, reduciendo la influencia negativa de valores atípicos en el modelo.

### 6. División de los datos en entrenamiento y validación

El conjunto de datos se divide en dos subconjuntos:

- **Conjunto de entrenamiento**: El 80% de los datos, que se utiliza para entrenar el modelo.
- **Conjunto de validación**: El 20% de los datos, que se utiliza para validar el rendimiento del modelo y evitar problemas de sobreajuste (overfitting).

Esta división es importante para evaluar cómo se generaliza el modelo a nuevos datos no vistos durante el entrenamiento.

### 7. Normalización de las variables numéricas

Las variables numéricas se normalizan utilizando el `RobustScaler`, que es particularmente útil cuando se trata de datos con outliers, ya que utiliza los cuartiles en lugar de la media y la desviación estándar. Esta normalización garantiza que todas las variables numéricas tengan la misma escala, mejorando así la eficiencia del entrenamiento del modelo.

### 8. Entrenamiento del modelo XGBoost

Se entrena un modelo de regresión utilizando XGBoost, que es un algoritmo de boosting basado en árboles de decisión. Para optimizar el modelo, se utiliza `GridSearchCV` para buscar los mejores hiperparámetros posibles, como la tasa de aprendizaje (`learning_rate`), el número de estimadores (`n_estimators`), la profundidad de los árboles (`max_depth`), entre otros.

Además, se implementa una métrica de evaluación personalizada que combina el error cuadrático medio (RMSE) y el error porcentual absoluto medio (MAPE). Esto permite un balance entre precisión y robustez en el modelo.

Los hiperparámetros optimizados se seleccionan tras ejecutar una búsqueda exhaustiva (GridSearch), y se utiliza el mejor modelo para hacer predicciones en el conjunto de validación. Finalmente, se calculan y reportan los valores de RMSE y MAPE para evaluar el rendimiento del modelo.

### 9. Evaluación del modelo

Se evalúa el rendimiento del modelo tanto en el conjunto de entrenamiento como en el conjunto de validación utilizando las métricas de RMSE y MAPE. Estas métricas permiten cuantificar el error entre las predicciones del modelo y los valores reales:

- **RMSE (Root Mean Squared Error)**: Es una métrica que penaliza los errores grandes de manera más severa, útil para medir la precisión de las predicciones.
- **MAPE (Mean Absolute Percentage Error)**: Mide el error en términos porcentuales, lo cual es útil cuando se quiere entender el error relativo.

El objetivo de esta evaluación es comprobar si el modelo está ajustado adecuadamente y si existe algún indicio de sobreajuste o subajuste (overfitting o underfitting).

### 10. Importancia de las variables

Se analiza la importancia de las variables que influyen en el modelo de XGBoost. Para ello, se extrae la importancia de cada característica basada en el número de veces que se utiliza para dividir los nodos en los árboles de decisión del modelo.

Posteriormente, se crea una visualización con un gráfico de barras donde se muestra el porcentaje de importancia de cada variable. Esto permite identificar cuáles son las características más relevantes que el modelo utiliza para predecir la variable objetivo.

Esta etapa es fundamental para entender las relaciones entre las variables y las predicciones realizadas por el modelo, proporcionando una mayor interpretabilidad y justificación para las decisiones tomadas en el modelo.
