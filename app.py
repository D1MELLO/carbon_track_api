from flask import Flask, request, jsonify
from flask_cors import CORS  # Importe o CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Fatores de emissão padrão (sem dependência da API Carbon Interface)
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
    return '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API de Pegada de Carbono</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }
                .container {
                    background: white;
                    padding: 2rem;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                    text-align: center;
                }
                h1 {
                    color: #4CAF50;
                }
                a {
                    color: #4CAF50;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .footer {
                    margin-top: 2rem;
                    font-size: 0.9rem;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Bem-vindo à API de Pegada de Carbono!</h1>
                <p>
                    Esta API permite calcular a pegada de carbono com base em dados de transporte, energia e alimentação.
                </p>
                <h2>Como usar:</h2>
                <p>
                    Envie uma requisição <strong>POST</strong> para o endpoint <code>/calculate</code> com os seguintes dados:
                </p>
                <pre>
{
    "transport": {
        "car_distance": 100.0,
        "bus_distance": 50.0,
        "plane_distance": 200.0
    },
    "energy": {
        "electricity_usage": 300.0
    },
    "food": {
        "meat_consumption": 5.0,
        "dairy_consumption": 10.0
    }
}
                </pre>
                <p>
                    A API retornará o cálculo da pegada de carbono em <strong>kg de CO2</strong>.
                </p>
            </div>
        </body>
        </html>
    '''

@app.route("/calculate", methods=["POST"])
def calculate():
    # Recebe os dados do app Android ou qualquer cliente
    data = request.json
    transport = data.get("transport", {})
    energy = data.get("energy", {})
    food = data.get("food", {})

    # Calcula a pegada de carbono usando os fatores de emissão padrão
    total_footprint = 0.0

    # Transporte
    car_distance = transport.get("car_distance", 0.0)
    bus_distance = transport.get("bus_distance", 0.0)
    plane_distance = transport.get("plane_distance", 0.0)

    total_footprint += car_distance * DEFAULT_EMISSION_FACTORS["car"]
    total_footprint += bus_distance * DEFAULT_EMISSION_FACTORS["bus"]
    total_footprint += plane_distance * DEFAULT_EMISSION_FACTORS["plane"]

    # Energia
    electricity_usage = energy.get("electricity_usage", 0.0)
    total_footprint += electricity_usage * DEFAULT_EMISSION_FACTORS["electricity"]

    # Alimentação
    meat_consumption = food.get("meat_consumption", 0.0)
    dairy_consumption = food.get("dairy_consumption", 0.0)

    total_footprint += meat_consumption * DEFAULT_EMISSION_FACTORS["beef"]
    total_footprint += dairy_consumption * DEFAULT_EMISSION_FACTORS["dairy"]

    # Retorna o resultado
    return jsonify({
        "total_footprint": total_footprint,
        "unit": "kg CO2"
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Usa a porta definida pelo ambiente ou 5000 como padrão
    app.run(host="0.0.0.0", port=port, debug=True)