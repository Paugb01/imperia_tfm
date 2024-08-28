import joblib
import xgboost as xgb
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Cargar el modelo y el preprocesador
modelo_path = 'xgb_model.pkl'
scaler_path = 'scaler.pkl'

modelo = joblib.load(modelo_path)
scaler = joblib.load(scaler_path)

@app.route('/')
def home():
    return render_template('index.html', prediccion=None)

@app.route('/predict', methods=['POST'])
def predict():
    mes = int(request.form['Mes'])
    año = int(request.form['Año'])
    
    # Preprocesar los datos
    datos = [[mes, año]]
    datos_transformados = scaler.transform(datos)
    
    # Hacer la predicción
    prediccion = modelo.predict(datos_transformados)
    resultado = prediccion[0]
    
    return jsonify({'prediccion': resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
