from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS  # Importe o CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Chave de API do Carbon Interface (usando variável de ambiente)
CARBON_INTERFACE_API_KEY = os.getenv("CARBON_INTERFACE_API_KEY")
CARBON_INTERFACE_URL = "https://www.carboninterface.com/api/v1/estimates"

# Fatores de emissão padrão (caso a API do Carbon Interface não esteja disponível)
DEFAULT_EMISSION_FACTORS = {
    "car": 0.12,  # kg CO2 por km (carro a gasolina)
    "bus": 0.05,  # kg CO2 por km (ônibus)
    "plane": 0.25,  # kg CO2 por km (avião)
    "electricity": 0.5,  # kg CO2 por kWh
    "beef": 27.0,  # kg CO2 por kg de carne
    "dairy": 2.0,  # kg CO2 por kg de laticínios
}

@app.route("/")
def home():
    return "Bem-vindo à API de Pegada de Carbono! Use o endpoint /calculate para calcular."

@app.route("/calculate", methods=["POST"])
def calculate():
    # Recebe os dados do app Android
    data = request.json
    transport = data.get("transport", {})
    energy