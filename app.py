import time
from google import genai
from google.genai import types
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="MediBot-Honduras", page_icon="🤖", layout="wide"
)

# Estilo visual futurista tipo hospital
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #30333d; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 MediBot-Honduras - Unidad de Pre-Triaje Clínico")
st.markdown(
    "Sistema inteligente de asistencia médica preliminar con parámetros"
    " antropométricos."
)
st.markdown("---")

# Dividir la pantalla en dos columnas
col_izq, col_der = st.columns([1, 2])

with col_izq:
  st.header("📊 Datos del Paciente")
  with st.form("formulario_triaje"):
    # Nuevos campos solicitados por el usuario
    edad = st.number_input("Edad (Años)", min_value=1, max_value=120, value=16)
    peso = st.number_input(
        "Peso (kg)", min_value=5.0, max_value=200.0, value=65.0, step=0.5
    )
    estatura = st.number_input(
        "Estatura (cm)", min_value=50, max_value=230, value=170
    )

    st.markdown("---")
    st.subheader("Signos Vitales")
    temperatura = st.number_input(
        "Temperatura Corporal (°C)",
        min_value=34.0,
        max_value=43.0,
        value=38.5,
        step=0.1,
    )
    oxigeno = st.slider(
        "Saturación de Oxígeno (SpO2 %)", min_value=50, max_value=100, value=96
    )
    pulso = st.number_input(
        "Frecuencia Cardíaca (Pulso lpm)",
        min_value=30,
        max_value=220,
        value=110,
    )
    sintomas = st.text_area(
        "Síntomas y Molestias",
        "Fiebre alta, escalofríos y dolor de garganta persistente.",
    )

    enviar = st.form_submit_button(
        "🔍 Analizar con MediBot AI", use_container_width=True
    )

with col_der:
  st.header("📋 Panel de Diagnóstico Clínico")

  if enviar:
    with st.spinner("Baymax analizando perfil clínico del paciente..."):
      client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

      system_instruction = (
          "Eres 'MediBot-Honduras', un asistente robótico de triaje médico avanzado. "
          "Analiza rigurosamente los datos antropométricos (edad, peso, estatura) y signos vitales. "
          "Clasifica el nivel de urgencia de forma explícita (Bajo/Código Verde, Moderado/Código Amarillo, Alto/Código Rojo) "
          "y redacta un reporte clínico formal estructurado exclusivamente para el médico tratante. No recetes medicamentos."
      )

      # Incluimos los nuevos datos en el prompt para que la IA los procese
      prompt_usuario = f"""
            Perfil y datos clínicos del paciente:
            - Edad: {edad} años
            - Peso: {peso} kg
            - Estatura: {estatura} cm
            - Temperatura: {temperatura} °C
            - Saturación de Oxígeno: {oxigeno}%
            - Pulso Cardíaco: {pulso} lpm
            - Síntomas: {sintomas}
            
            Genera el reporte clínico de pre-triaje estructurado.
            """

      reporte_generado = None
      error_encontrado = None

      # Conexión optimizada y rápida con reintento único
      for intento in range(1, 3):
        try:
          response = client.models.generate_content(
              model="gemini-3.8-flash",
              contents=prompt_usuario,
              config=types.GenerateContentConfig(
                  system_instruction=system_instruction,
                  temperature=0.2,
              ),
          )
          reporte_generado = response.text
          break
        except Exception as e:
          error_encontrado = str(e)
          if "503" in str(e) or "UNAVAILABLE" in str(e):
            time.sleep(1)
          else:
            break

      if reporte_generado:
        st.success("¡Análisis completado con éxito por MediBot!")
        st.markdown("---")
        st.markdown(reporte_generado)
      else:
        st.error(
            "⚠️ El servidor de la IA tardó en responder. Error:"
            f" {error_encontrado}"
        )
        st.info("Vuelve a hacer clic en el botón de analizar.")
  else:
    st.info(
        "👈 Ingresa los datos del paciente en el panel izquierdo (Edad, Peso,"
        " Estatura y Signos Vitales) y presiona el botón para generar el informe"
        " médico."
    )