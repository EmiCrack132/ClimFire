import requests
import pandas as pd

# ------------------------------------
# CONFIGURACIÓN
# ------------------------------------
LAT = -37.8136
LON = 144.9631

# ------------------------------------
# FUNCIÓN: Descargar datos históricos
# ------------------------------------
def descargar_historico():
    # Open-Meteo tiene un endpoint diferente para datos históricos
    url = "https://archive-api.open-meteo.com/v1/archive"

    parametros = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": "2015-01-01",   # Desde enero 2015
        "end_date":   "2024-12-31",   # Hasta diciembre 2024
        "daily": [
            "temperature_2m_max",
            "precipitation_sum",
            "windspeed_10m_max",
            "relative_humidity_2m_max"
        ],
        "timezone": "Australia/Melbourne"
    }

    print("Descargando 10 años de datos históricos...")
    print("Esto puede tardar unos segundos...\n")

    respuesta = requests.get(url, params=parametros)
    respuesta.raise_for_status()

    datos = respuesta.json()
    df = pd.DataFrame(datos["daily"])

    # Convertir la columna de fechas a formato fecha real
    # Ahora pandas entiende que "time" es una fecha, no solo texto
    df["time"] = pd.to_datetime(df["time"])

    print(f"Descarga completa.")
    print(f"Total de días descargados: {len(df)}")
    print(f"Desde: {df['time'].min().date()}")
    print(f"Hasta: {df['time'].max().date()}")
    print(f"\nPrimeras 5 filas:")
    print(df.head())

    return df

# ------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------
df_historico = descargar_historico()

# Guardar para usarlo en el siguiente paso
df_historico.to_csv("historico_victoria.csv", index=False)
print("\nArchivo guardado: historico_victoria.csv")