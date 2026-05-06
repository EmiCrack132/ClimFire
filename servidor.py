from flask import Flask, jsonify
import requests
import pandas as pd
import pickle
from flask import Flask, jsonify, send_from_directory

# ------------------------------------
# INICIAR FLASK
# ------------------------------------
# Flask(__name__) crea la aplicación web
# __name__ le dice a Flask en qué archivo está
app = Flask(__name__)

# ------------------------------------
# CARGAR EL MODELO ENTRENADO
# ------------------------------------
# pickle.load lee el archivo .pkl que guardamos en la Fase 2
# Esto lo hacemos una sola vez al iniciar el servidor
# para no recargarlo en cada petición
with open("modelo_incendio.pkl", "rb") as f:
    modelo = pickle.load(f)

print("Modelo cargado correctamente.")

# ------------------------------------
# FUNCIÓN: Obtener datos de la API
# ------------------------------------
def obtener_datos_clima():
    url = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": -37.8136,
        "longitude": 144.9631,
        "daily": [
            "temperature_2m_max",
            "precipitation_sum",
            "windspeed_10m_max",
            "relative_humidity_2m_max"
        ],
        "timezone": "Australia/Melbourne",
        "forecast_days": 7
    }
    respuesta = requests.get(url, params=parametros)
    respuesta.raise_for_status()
    return pd.DataFrame(respuesta.json()["daily"])

# ------------------------------------
# FUNCIÓN: Calcular días sin lluvia
# ------------------------------------
def agregar_dias_sin_lluvia(df):
    # Pedimos también datos de los últimos 10 días
    # para calcular la sequía acumulada correctamente
    url = "https://archive-api.open-meteo.com/v1/archive"

    from datetime import datetime, timedelta
    hoy = datetime.now()
    hace_10_dias = hoy - timedelta(days=10)

    parametros = {
        "latitude": -37.8136,
        "longitude": 144.9631,
        "start_date": hace_10_dias.strftime("%Y-%m-%d"),
        "end_date": hoy.strftime("%Y-%m-%d"),
        "daily": ["precipitation_sum"],
        "timezone": "Australia/Melbourne"
    }

    respuesta = requests.get(url, params=parametros)
    df_pasado = pd.DataFrame(respuesta.json()["daily"])

    # Contar días consecutivos sin lluvia hasta hoy
    contador = 0
    for lluvia in df_pasado["precipitation_sum"]:
        if lluvia == 0:
            contador += 1
        else:
            contador = 0

    # Aplicar ese contador a los días del forecast
    dias_sin_lluvia = []
    for lluvia in df["precipitation_sum"]:
        if lluvia == 0:
            contador += 1
        else:
            contador = 0
        dias_sin_lluvia.append(contador)

    df["dias_sin_lluvia"] = dias_sin_lluvia
    return df

# ------------------------------------
# RUTA: Página principal
# ------------------------------------
# @app.route define una URL
# Cuando el navegador entra a "/" responde con esto
@app.route("/")
def inicio():
    return send_from_directory("static", "index.html")

# ------------------------------------
# RUTA: API de predicciones
# ------------------------------------
# El navegador va a llamar a esta URL para pedir los datos
# jsonify convierte un diccionario Python a formato JSON
@app.route("/api/forecast")
def forecast():
    # 1. Obtener datos del clima
    df = obtener_datos_clima()

    # 2. Agregar días sin lluvia
    df = agregar_dias_sin_lluvia(df)

    # 3. Preparar los datos para el modelo
    features = [
        "temperature_2m_max",
        "precipitation_sum",
        "windspeed_10m_max",
        "relative_humidity_2m_max",
        "dias_sin_lluvia"
    ]
    X = df[features]

    # 4. Hacer predicciones con el modelo
    predicciones = modelo.predict(X)

    # 5. Convertir números a texto legible
    nombres = {0: "LOW", 1: "MODERATE", 2: "HIGH"}
    colores = {0: "#22c55e", 1: "#ff6a00", 2: "#ff2a00"}

    # 6. Armar la respuesta como lista de diccionarios
    dias = []
    for i, row in df.iterrows():
        nivel = int(predicciones[i])
        dias.append({
            "fecha":        row["time"],
            "temperatura":  round(row["temperature_2m_max"], 1),
            "lluvia":       round(row["precipitation_sum"], 1),
            "viento":       round(row["windspeed_10m_max"], 1),
            "humedad":      round(row["relative_humidity_2m_max"], 1),
            "dias_sequia":  int(row["dias_sin_lluvia"]),
            "riesgo":       nombres[nivel],
            "color":        colores[nivel]
        })

    return jsonify(dias)

# ------------------------------------
# RUTA: Datos de especies y zonas
# ------------------------------------
@app.route("/api/especies")
def especies():
    # Datos reales de especies amenazadas de Victoria
    # fuente: Victorian Biodiversity Atlas + IUCN Red List
    datos = {
        "especies": [
            {
                "nombre": "Koala",
                "nombre_cientifico": "Phascolarctos cinereus",
                "estado": "Vulnerable",
                "poblacion_estimada": 32000,
                "habitat": "Eucalyptus forests",
                "sensibilidad_incendio": "alta",
                "emoji": "🐨"
            },
            {
                "nombre": "Long-footed Potoroo",
                "nombre_cientifico": "Potorous longipes",
                "estado": "Endangered",
                "poblacion_estimada": 200,
                "habitat": "Eastern wet forests",
                "sensibilidad_incendio": "muy_alta",
                "emoji": "🦘"
            },
            {
                "nombre": "Leadbeater's Possum",
                "nombre_cientifico": "Gymnobelideus leadbeateri",
                "estado": "Critically Endangered",
                "poblacion_estimada": 1500,
                "habitat": "Mountain ash forests",
                "sensibilidad_incendio": "muy_alta",
                "emoji": "🦔"
            },
            {
                "nombre": "Gang-gang Cockatoo",
                "nombre_cientifico": "Callocephalon fimbriatum",
                "estado": "Vulnerable",
                "poblacion_estimada": 10000,
                "habitat": "Alpine and subalpine forests",
                "sensibilidad_incendio": "alta",
                "emoji": "🦜"
            },
            {
                "nombre": "Baw Baw Frog",
                "nombre_cientifico": "Philoria frosti",
                "estado": "Critically Endangered",
                "poblacion_estimada": 2500,
                "habitat": "Wet alpine grasslands",
                "sensibilidad_incendio": "alta",
                "emoji": "🐸"
            },
            {
                "nombre": "Spotted-tailed Quoll",
                "nombre_cientifico": "Dasyurus maculatus",
                "estado": "Vulnerable",
                "poblacion_estimada": 5000,
                "habitat": "Dense coastal forests",
                "sensibilidad_incendio": "media",
                "emoji": "🐾"
            }
        ],
        "zonas": [
            {
                "nombre": "Great Otway National Park",
                "lat": -38.7500, "lon": 143.7000,
                "area_ha": 103000,
                "cobertura": "Temperate rainforest",
                "riesgo_base": "moderate"
            },
            {
                "nombre": "Alpine National Park",
                "lat": -36.9000, "lon": 147.2000,
                "area_ha": 646000,
                "cobertura": "Alpine and subalpine forest",
                "riesgo_base": "high"
            },
            {
                "nombre": "Yarra Ranges National Park",
                "lat": -37.6500, "lon": 145.8000,
                "area_ha": 76000,
                "cobertura": "Mountain ash and eucalyptus forest",
                "riesgo_base": "moderate"
            },
            {
                "nombre": "Grampians National Park",
                "lat": -37.1500, "lon": 142.5200,
                "area_ha": 167000,
                "cobertura": "Eucalyptus and mallee woodland",
                "riesgo_base": "high"
            },
            {
                "nombre": "Wilsons Promontory",
                "lat": -39.0800, "lon": 146.3800,
                "area_ha": 50000,
                "cobertura": "Coastal forest and heath",
                "riesgo_base": "moderate"
            }
        ]
    }
    return jsonify(datos)

# ------------------------------------
# INICIAR EL SERVIDOR
# ------------------------------------
if __name__ == "__main__":
    # debug=True recarga el servidor automáticamente
    # cuando guardas cambios en el archivo
    app.run(debug=True)