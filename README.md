# 🔥 ClimFire
### Forest Fire Risk Intelligence System — Victoria, Australia

> Built for **WeatherWise Hack 2026** — Smarter Weather. Safer World.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![ML](https://img.shields.io/badge/ML-Random%20Forest-orange)
![API](https://img.shields.io/badge/Data-Open--Meteo-lightblue)

---

## 🌐 Live Demo

**[climfire.onrender.com](https://climfire.onrender.com)**
*(replace with your actual Render URL)*

---

## 🔥 What is ClimFire?

ClimFire is a real-time forest fire risk intelligence system for Victoria,
Australia — one of the most fire-prone regions on Earth.

The 2019–2020 Black Summer fires burned over 5.8 million hectares in Victoria
alone, killed billions of animals, and displaced thousands of people. Yet many
communities still lack access to reliable, actionable fire risk information.

ClimFire addresses this by combining real-time climate data with a Machine
Learning model trained on 10 years of historical weather patterns to predict
daily fire risk levels — and estimate the environmental impact on endangered
wildlife before a fire event occurs.

---

## 🧠 How It Works
Open-Meteo API          NASA-grade climate data
↓
Data Processing         pandas · feature engineering
↓
ML Model                Random Forest Classifier (scikit-learn)
↓
Risk Prediction         LOW / MODERATE / HIGH
↓
Flask Backend           REST API serving predictions
↓
Web Dashboard           Real-time map · Wildlife alerts · Impact calculator

---

## ✨ Features

- **7-Day Fire Risk Forecast** — daily predictions powered by ML
- **Interactive Risk Map** — Victoria's protected areas color-coded by risk level
- **Wildlife Impact Dashboard** — 6 endangered species monitored with real-time alerts
- **Environmental Impact Calculator** — estimates hectares, trees, CO₂, and animal populations at risk
- **Live Data** — climate data refreshed on every page load via Open-Meteo API

---

## 🏆 Hackathon Tracks

| Track | How ClimFire qualifies |
|---|---|
| 🌧 Weather Intelligence | Real-time 7-day climate forecast with visualization |
| 🚨 Disaster Response & Preparedness | Fire risk prediction with visual alerts |
| 🤖 AI & Data Innovation | Random Forest ML model trained on 10 years of data |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Backend | Flask · Gunicorn |
| Machine Learning | scikit-learn · pandas · numpy |
| Climate Data | Open-Meteo Forecast & Archive API |
| Frontend | HTML · CSS · Vanilla JavaScript |
| Map | Leaflet.js · OpenStreetMap · CARTO |
| Fonts | Google Fonts (Bebas Neue · DM Sans) |
| Deploy | Render (free tier) |

---

## 🤖 ML Model Details

- **Algorithm:** Random Forest Classifier
- **Training data:** Open-Meteo historical archive 2015–2024 (3,653 days)
- **Features used:**
  - Maximum daily temperature (°C)
  - Total precipitation (mm)
  - Maximum wind speed (km/h)
  - Maximum relative humidity (%)
  - Consecutive dry days *(engineered feature)*
- **Output classes:** LOW · MODERATE · HIGH fire risk
- **Test accuracy:** 99% on 731 unseen days
- **Labeling:** Based on Bureau of Meteorology (BOM) Fire Weather Index thresholds

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/EmiCrack132/ClimFire.git
cd ClimFire
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate data and train the model
```bash
python fase2_datos_historicos.py
python fase2_etiquetar.py
python fase2_modelo.py
```

### 5. Start the server
```bash
python servidor.py
```

### 6. Open in browser
http://127.0.0.1:5000

---

## 📁 Project Structure
ClimFire/
├── static/
│   └── index.html              # Frontend dashboard
├── fase1_api.py                # Phase 1 — API exploration
├── fase2_datos_historicos.py   # Phase 2 — Historical data download
├── fase2_etiquetar.py          # Phase 2 — Data labeling
├── fase2_modelo.py             # Phase 2 — ML model training
├── servidor.py                 # Flask backend
├── modelo_incendio.pkl         # Trained ML model
├── forecast_victoria.csv       # Sample forecast output
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deploy config
├── LICENSE                     # MIT License
└── README.md                   # This file

---

## 🌿 Data Sources & Attribution

| Source | Used for | License |
|---|---|---|
| [Open-Meteo](https://open-meteo.com) | Real-time & historical climate data | CC BY 4.0 |
| [Victorian Biodiversity Atlas](https://www.environment.vic.gov.au) | Species population estimates | Public reference |
| [IUCN Red List](https://www.iucnredlist.org) | Conservation status | Public reference |
| [OpenStreetMap](https://www.openstreetmap.org) | Map data | ODbL |
| [CARTO](https://carto.com) | Dark map tiles | Free tier |
| [Leaflet.js](https://leafletjs.com) | Interactive map library | BSD 2-Clause |

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE)
file for details.

---

## 👤 Author

**EmiCrack132**
Built with 🔥 for WeatherWise Hack 2026