import requests
import pandas as pd

# ------------------------------------
# CONFIGURACIÓN
# ------------------------------------
LAT = -37.8136   # Victoria, Australia
LON = 144.9631

# ------------------------------------
# FUNCIÓN 1: Pedir datos a la API
# ------------------------------------
def obtener_forecast():
    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": LAT,
        "longitude": LON,
        "daily": [
            "temperature_2m_max",       # Temperatura máxima del día
            "precipitation_sum",         # Lluvia total del día
            "windspeed_10m_max",         # Viento máximo
            "relative_humidity_2m_max"    # Humedad máxima
        ],
        "timezone": "Australia/Melbourne",
        "forecast_days": 7
    }

    print("Conectando con la API...")
    respuesta = requests.get(url, params=parametros)
    respuesta.raise_for_status()  # Si hay error, lo muestra claro
    print("Datos recibidos correctamente.\n")

    datos = respuesta.json()
    df = pd.DataFrame(datos["daily"])
    return df

# ------------------------------------
# FUNCIÓN 2: Calcular riesgo por día
# ------------------------------------
def calcular_riesgo(fila):
    puntos = 0

    if fila["temperature_2m_max"] > 35:        puntos += 2
    if fila["relative_humidity_2m_max"] < 20:   puntos += 2
    if fila["windspeed_10m_max"] > 50:         puntos += 1
    if fila["precipitation_sum"] == 0:         puntos += 1

    if puntos >= 4:
        return "ALTO"
    elif puntos >= 2:
        return "MODERADO"
    else:
        return "BAJO"

# ------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------
df = obtener_forecast()

# Calcular el riesgo para cada día
df["riesgo"] = df.apply(calcular_riesgo, axis=1)

# Renombrar columnas para que sean legibles
df = df.rename(columns={
    "time":                      "Fecha",
    "temperature_2m_max":        "Temp_max (°C)",
    "precipitation_sum":         "Lluvia (mm)",
    "windspeed_10m_max":         "Viento (km/h)",
    "relative_humidity_2m_max":   "Humedad (%)"
})

# Mostrar resultados
print("=" * 60)
print("PRONÓSTICO DE RIESGO DE INCENDIO — Victoria, Australia")
print("=" * 60)
print(df[["Fecha", "Temp_max (°C)", "Lluvia (mm)", "Viento (km/h)", "Humedad (%)", "riesgo"]].to_string(index=False))
print("=" * 60)

# Guardar en CSV
df.to_csv("forecast_victoria.csv", index=False)
print("\nArchivo guardado: forecast_victoria.csv")