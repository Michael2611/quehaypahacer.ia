# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from recomendacion import obtener_lugares_desde_bd, MotorRecomendacion

app = Flask(__name__)
CORS(app)

# Cargar lugares y motor al iniciar la API
lugares = obtener_lugares_desde_bd()
motor = MotorRecomendacion(lugares)

@app.route('/')
def home():
    return jsonify({"mensaje": "API de recomendación turística funcionando"})

@app.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.get_json()
    texto_usuario = data.get("texto", "")
    top_k = data.get("top_k", 3)

    if not texto_usuario:
        return jsonify({"error": "Debe enviar un texto"}), 400

    resultados = motor.recomendar(texto_usuario, top_k)
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=True)