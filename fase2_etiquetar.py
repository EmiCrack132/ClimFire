import pandas as pd
import numpy as np

# ------------------------------------
# CARGAR LOS DATOS QUE DESCARGAMOS
# ------------------------------------
# Aquí leemos el CSV que generamos en el paso anterior
df = pd.read_csv("historico_victoria.csv")

# Volvemos a convertir la columna time a formato fecha
df["time"] = pd.to_datetime(df["time"])

print(f"Datos cargados: {len(df)} días")
print(f"Columnas: {list(df.columns)}\n")

# ------------------------------------
# MANEJAR VALORES VACÍOS
# ------------------------------------
# A veces la API devuelve días sin datos (sensores fallidos, etc.)
# Si no los manejamos, el modelo se rompe
print(f"Valores vacíos antes de limpiar:")
print(df.isnull().sum())

# Rellenamos los vacíos con el promedio de la columna
# Es la técnica más simple y funciona bien para pocos vacíos
df = df.fillna(df.mean(numeric_only=True))

print(f"\nValores vacíos después de limpiar:")
print(df.isnull().sum())

# ------------------------------------
# CREAR FEATURE: DÍAS SIN LLUVIA
# ------------------------------------
# Esta es la variable más importante para incendios
# Un día sin lluvia no es peligroso, pero 20 días seguidos sí
# Esto se llama "feature engineering" — crear variables nuevas
# a partir de las que ya tienes

dias_sin_lluvia = []
contador = 0

for lluvia in df["precipitation_sum"]:
    if lluvia == 0:
        contador += 1
    else:
        contador = 0  # Resetea cuando llueve
    dias_sin_lluvia.append(contador)

df["dias_sin_lluvia"] = dias_sin_lluvia

print(f"\nMáximo de días consecutivos sin lluvia: {df['dias_sin_lluvia'].max()}")

# ------------------------------------
# CREAR ETIQUETAS DE RIESGO
# ------------------------------------
# Basado en los umbrales oficiales del Bureau of Meteorology
# de Australia (BOM) adaptados al FWI simplificado

def etiquetar_riesgo(fila):
    puntos = 0

    # Temperatura
    if fila["temperature_2m_max"] > 25:
        puntos += 2
    elif fila["temperature_2m_max"] > 18:
        puntos += 1

    # Humedad
    if fila["relative_humidity_2m_max"] < 55:
        puntos += 2
    elif fila["relative_humidity_2m_max"] < 70:
        puntos += 1

    # Viento
    if fila["windspeed_10m_max"] > 25:
        puntos += 2
    elif fila["windspeed_10m_max"] > 15:
        puntos += 1

    # Sequía acumulada
    if fila["dias_sin_lluvia"] > 7:
        puntos += 3
    elif fila["dias_sin_lluvia"] > 3:
        puntos += 2
    elif fila["dias_sin_lluvia"] > 1:
        puntos += 1

    if puntos >= 6:
        return 2   # ALTO
    elif puntos >= 4:
        return 1   # MODERADO
    else:
        return 0   # BAJO

df["riesgo"] = df.apply(etiquetar_riesgo, axis=1)

# ------------------------------------
# REVISAR DISTRIBUCIÓN DE ETIQUETAS
# ------------------------------------
# Importante: si el 99% de días son "BAJO" y solo 1% son "ALTO"
# el modelo va a aprender a decir siempre "BAJO" y parecer preciso
# Queremos una distribución razonable

conteo = df["riesgo"].value_counts().sort_index()
nombres = {0: "BAJO", 1: "MODERADO", 2: "ALTO"}

print("\nDistribución de etiquetas:")
for nivel, cantidad in conteo.items():
    porcentaje = (cantidad / len(df)) * 100
    print(f"  {nombres[nivel]}: {cantidad} días ({porcentaje:.1f}%)")

# ------------------------------------
# GUARDAR
# ------------------------------------
df.to_csv("datos_entrenamiento.csv", index=False)
print("\nArchivo guardado: datos_entrenamiento.csv")
print(f"Columnas finales: {list(df.columns)}")