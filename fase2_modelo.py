import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# ------------------------------------
# CARGAR DATOS ETIQUETADOS
# ------------------------------------
df = pd.read_csv("datos_entrenamiento.csv")
print(f"Datos cargados: {len(df)} días\n")

# ------------------------------------
# SEPARAR FEATURES Y ETIQUETAS
# ------------------------------------
# Features = las variables que el modelo usa para predecir
# Son las "pistas" que le damos al modelo
features = [
    "temperature_2m_max",
    "precipitation_sum",
    "windspeed_10m_max",
    "relative_humidity_2m_max",
    "dias_sin_lluvia"
]

# X = las pistas (lo que el modelo recibe como entrada)
# y = la respuesta correcta (lo que el modelo debe aprender a predecir)
X = df[features]
y = df["riesgo"]

print(f"Features usadas: {features}")
print(f"Total de ejemplos: {len(X)}\n")

# ------------------------------------
# DIVIDIR EN ENTRENAMIENTO Y PRUEBA
# ------------------------------------
# test_size=0.2 significa 20% para prueba, 80% para entrenar
# random_state=42 es una semilla — garantiza que la división
# sea siempre la misma cada vez que ejecutes el script
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Días para entrenar: {len(X_train)}")
print(f"Días para evaluar:  {len(X_test)}\n")

# ------------------------------------
# CREAR Y ENTRENAR EL MODELO
# ------------------------------------
# n_estimators=100 significa 100 árboles en el bosque
# random_state=42 para reproducibilidad
modelo = RandomForestClassifier(n_estimators=100, random_state=42)

print("Entrenando el modelo...")
modelo.fit(X_train, y_train)   # Aquí ocurre el aprendizaje
print("Entrenamiento completo.\n")

# ------------------------------------
# EVALUAR EL MODELO
# ------------------------------------
# Hacemos predicciones sobre los días que el modelo nunca vio
predicciones = modelo.predict(X_test)

# classification_report muestra qué tan bien predice cada categoría
nombres_clases = ["BAJO", "MODERADO", "ALTO"]
print("=" * 50)
print("RESULTADOS DEL MODELO")
print("=" * 50)
print(classification_report(y_test, predicciones, target_names=nombres_clases))

# ------------------------------------
# IMPORTANCIA DE CADA FEATURE
# ------------------------------------
# El modelo nos dice cuál variable fue más útil para predecir
importancias = pd.Series(modelo.feature_importances_, index=features)
importancias = importancias.sort_values(ascending=False)

print("¿Qué variable importó más para predecir el riesgo?")
for feature, valor in importancias.items():
    barra = "█" * int(valor * 40)
    print(f"  {feature:<35} {barra} {valor:.3f}")

# ------------------------------------
# GUARDAR EL MODELO
# ------------------------------------
# pickle guarda el modelo entrenado en un archivo
# para poder usarlo después sin reentrenar
with open("modelo_incendio.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("\nModelo guardado: modelo_incendio.pkl")