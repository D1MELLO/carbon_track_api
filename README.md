# 🌱 CarbonTrack API

A **CarbonTrack API** é uma API REST criada com Flask para calcular a pegada de carbono com base nos hábitos de transporte, consumo de energia e alimentação do usuário. Ela é utilizada pelo app Android [CarbonTrack](https://github.com/D1MELLO/CarbonTrack), voltado à conscientização ambiental.

> ✅ API hospedada no [Render](https://carbon-track-api.onrender.com)

---

## 📌 Endpoints

### `GET /`
Retorna uma página HTML com instruções de uso da API.

---

### `POST /calculate`

Calcula a pegada de carbono com base nos dados enviados.

#### 🔸 Exemplo de Requisição:

```json
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
```

#### 🔸 Exemplo de Resposta:

```json
{
  "total_footprint": 164.5,
  "unit": "kg CO2"
}
```

---

## 🔬 Fatores de Emissão

| Categoria    | Fator (kg CO₂)         |
|--------------|------------------------|
| Carro        | 0.12 por km            |
| Ônibus       | 0.05 por km            |
| Avião        | 0.25 por km            |
| Eletricidade | 0.5 por kWh            |
| Carne        | 27.0 por kg            |
| Laticínios   | 2.0 por kg             |

---

## ⚙️ Tecnologias

- **Python 3**
- **Flask** (`2.3.2`)
- **Flask-Cors** (`4.0.0`)
- **Gunicorn** (`20.1.0`)
- **Render** (para deploy)

---

## 🚀 Como rodar localmente

```bash
git clone https://github.com/D1MELLO/carbon_track_api.git
cd carbon_track_api

python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

pip install -r requirements.txt
python app.py
```

Acesse em: [http://localhost:5000](http://localhost:5000)

---

## ☁️ Deploy (Render)

Este projeto já está configurado para deploy no Render.

### `Procfile`:
```txt
web: gunicorn app:app
```

---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo [`LICENSE`](LICENSE) para mais informações.

---

### Criado por [Sérgio de Melo](https://github.com/D1MELLO)
