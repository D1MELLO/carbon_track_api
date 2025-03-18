from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS  # Importe o CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Chave de API do Carbon Interface (usando variável de ambiente)
CARBON_INTERFACE_API_KEY = os.getenv("cUr4PDUXEpSe4mzDjHkQ")
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
    energy = data.get("energy", {})
    food = data.get("food", {})

    # Calcula a pegada de carbono
    total_footprint = 0.0

    # Transporte
    car_distance = transport.get("car_distance", 0.0)
    bus_distance = transport.get("bus_distance", 0.0)
    plane_distance = transport.get("plane_distance", 0.0)

    total_footprint += car_distance * get_emission_factor("car")
    total_footprint += bus_distance * get_emission_factor("bus")
    total_footprint += plane_distance * get_emission_factor("plane")

    # Energia
    electricity_usage = energy.get("electricity_usage", 0.0)
    total_footprint += electricity_usage * get_emission_factor("electricity")

    # Alimentação
    meat_consumption = food.get("meat_consumption", 0.0)
    dairy_consumption = food.get("dairy_consumption", 0.0)

    total_footprint += meat_consumption * get_emission_factor("beef")
    total_footprint += dairy_consumption * get_emission_factor("dairy")

    # Retorna o resultado
    return jsonify({
        "total_footprint": total_footprint,
        "unit": "kg CO2"
    })

def get_emission_factor(source):
    try:
        if source in ["car", "bus", "plane"]:
            response = requests.post(
                CARBON_INTERFACE_URL,
                headers={
                    "Authorization": f"Bearer {CARBON_INTERFACE_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "type": "vehicle",
                    "distance_unit": "km",
                    "vehicle": source,
                    "fuel": "gasoline" if source == "car" else "diesel"
                }
            )
            print("Resposta da API do Carbon Interface:", response.text)  # Log da resposta
            return response.json().get("data", {}).get("attributes", {}).get("carbon_kg", DEFAULT_EMISSION_FACTORS[source])
        elif source == "electricity":
            response = requests.post(
                CARBON_INTERFACE_URL,
                headers={
                    "Authorization": f"Bearer {CARBON_INTERFACE_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "type": "electricity",
                    "value": 1,  # 1 kWh
                    "unit": "kWh"
                }
            )
            print("Resposta da API do Carbon Interface:", response.text)  # Log da resposta
            return response.json().get("data", {}).get("attributes", {}).get("carbon_kg", DEFAULT_EMISSION_FACTORS[source])
        elif source in ["beef", "dairy"]:
            return DEFAULT_EMISSION_FACTORS[source]
    except Exception as e:
        print(f"Erro ao obter fator de emissão: {e}")
        return DEFAULT_EMISSION_FACTORS[source]

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Usa a porta definida pelo Render ou 5000 como padrão
    app.run(host="0.0.0.0", port=port, debug=True)