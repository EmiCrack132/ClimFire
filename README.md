# 🔥 ClimFire
**Sistema de predicción de riesgo de incendio forestal — Victoria, Australia**

Proyecto desarrollado para WeatherWise Hack 2026.

---

## ¿Qué hace?
ClimFire consume datos climáticos en tiempo real de Victoria, Australia,
y predice el nivel de riesgo de incendio forestal para los próximos 7 días
usando un modelo de Machine Learning entrenado con 10 años de datos históricos.

## Stack técnico
- **Backend:** Python · Flask · scikit-learn · pandas
- **Modelo ML:** Random Forest (3 clases: BAJO / MODERADO / ALTO)
- **API de datos:** Open-Meteo (tiempo real + histórico)
- **Frontend:** HTML · CSS · JavaScript vanilla

## Cómo ejecutar el proyecto localmente

### 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/climfire.git
cd climfire

### 2. Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

### 3. Generar los datos y entrenar el modelo
python fase2_datos_historicos.py
python fase2_etiquetar.py
python fase2_modelo.py

### 4. Iniciar el servidor
python servidor.py

### 5. Abrir en el navegador
http://127.0.0.1:5000

## Estructura del proyecto
climfire/
├── static/
│   └── index.html          # Frontend
├── fase1_api.py            # Prueba inicial de API
├── fase2_datos_historicos.py
├── fase2_etiquetar.py
├── fase2_modelo.py
├── servidor.py             # Backend Flask
├── modelo_incendio.pkl     # Modelo entrenado
├── requirements.txt        # Dependencias
└── README.md

## Datos
- Fuente histórica: Open-Meteo Archive API (2015–2024)
- Fuente tiempo real: Open-Meteo Forecast API
- Etiquetado basado en umbrales del Bureau of Meteorology (BOM) de Australia