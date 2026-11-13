from google import genai
from google.genai import types
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="MediBot-Honduras | Sistema de Pre-Triaje IA",
    page_icon="🤖",
    layout="wide",
)

# Estilo visual Futurista / Médico Minimalista (Modo Oscuro Clínico de Alta Gama)
st.markdown(
    """
    <style>
    .main { background-color: #05070b; color: #e2e8f0; }
    .stForm { background-color: #0f141f; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .stMetric { background-color: #131b2e; padding: 15px; border-radius: 8px; border: 1px solid #1e3a8a; }
    h1, h2, h3 { color: #38bdf8 !important; font-family: 'Inter', sans-serif; }
    .reportview-container { background: #05070b; }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado con estilo de interfaz médica avanzada
st.markdown(
    """
    <div style='padding: 10px 0; border-bottom: 2px solid #0284c7; margin-bottom: 20px;'>
        <h1 style='margin: 0; font-size: 2.2rem;'>🤖 MEDIBOT-HONDURAS</h1>
        <p style='color: #94a3b8; font-size: 1.1rem; margin-top: 5px;'>Plataforma de Pre-Triaje Clínico Asistido por Inteligencia Artificial</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Distribución en dos columnas principales
col_izq, col_der = st.columns([1, 1.8], gap="large")

with col_izq:
  st.markdown("### 🧬 Datos y Constantes")
  with st.form("formulario_triaje"):
    # Campo de Nombre del Paciente
    nombre_paciente = st.text_input(
        "Nombre Completo del Paciente", "Ej. Juan Pérez"
    )

    col_sub1, col_sub2, col_sub3 = st.columns(3)
    with col_sub1:
      edad = st.number_input("Edad", min_value=1, max_value=120, value=25)
    with col_sub2:
      peso = st.number_input(
          "Peso (kg)", min_value=2.0, max_value=200.0, value=70.0, step=0.5
      )
    with col_sub3:
      estatura = st.number_input(
          "Estatura (cm)", min_value=40, max_value=230, value=172
      )

    st.markdown("---")
    st.markdown("#### ⚡ Signos Vitales")
    temperatura = st.number_input(
        "Temperatura Corporal (°C)",
        min_value=34.0,
        max_value=43.0,
        value=37.0,
        step=0.1,
    )
    oxigeno = st.slider(
        "Saturación de Oxígeno (SpO2 %)", min_value=50, max_value=100, value=98
    )
    pulso = st.number_input(
        "Frecuencia Cardíaca (Pulso lpm)",
        min_value=30,
        max_value=220,
        value=75,
    )

    sintomas = st.text_area(
        "Descripción Clínica de Síntomas",
        "Dolor de cabeza leve, fatiga y malestar general.",
        height=100,
    )

    st.markdown("")
    enviar = st.form_submit_button(
        "⚡ EJECUTAR PRE-TRIAJE CLÍNICO", use_container_width=True
    )

with col_der:
  st.markdown("### 📊 Consola de Diagnóstico e Informes")

  if enviar:
    if not nombre_paciente.strip():
      st.error("⚠️ Por favor, ingresa el nombre del paciente antes de continuar.")
    else:
      with st.spinner("Procesando pre-triaje de ultra alta velocidad..."):
        try:
          if (
              "GEMINI_API_KEY" not in st.secrets
              or not st.secrets["GEMINI_API_KEY"]
          ):
            st.error(
                "❌ Error crítico: La API Key no está configurada en los"
                " Secrets de Streamlit Cloud."
            )
          else:
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

            system_instruction = (
                "Eres 'MediBot-Honduras', un sistema experto de pre-triaje médico. "
                "Responde de forma concisa y directa dividiendo estrictamente tu respuesta con esta etiqueta exacta: [SEPARADOR_REPORTES].\n"
                "Parte 1: Reporte clínico formal para el médico (Nivel de urgencia, constantes y sospecha clínica).\n"
                "Parte 2: Explicación amigable y clara para el paciente."
            )

            prompt_usuario = f"""
                        Paciente: {nombre_paciente}
                        - Edad: {edad} años | Peso: {peso} kg | Estatura: {estatura} cm
                        - Temperatura: {temperatura} °C | SpO2: {oxigeno}% | Pulso: {pulso} lpm
                        - Síntomas: {sintomas}
                        """

            # Usamos gemini-2.5-flash que es el modelo estándar optimizado y compatible con google-genai
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1,
                    max_output_tokens=800,
                ),
            )

            texto_total = response.text

            if "[SEPARADOR_REPORTES]" in texto_total:
              partes = texto_total.split("[SEPARADOR_REPORTES]")
              reporte_medico = partes[0].strip()
              reporte_paciente = partes[1].strip()
            else:
              reporte_medico = texto_total
              reporte_paciente = (
                  "Consulte el informe detallado en la pestaña del médico."
              )

            st.success(
                f"✅ Pre-triaje completado con éxito para: **{nombre_paciente}**"
            )

            tab_medico, tab_paciente = st.tabs(
                ["📋 Reporte para el Médico", "👤 Explicación para el Paciente"]
            )

            with tab_medico:
              st.markdown(
                  "<div style='background-color: #0f141f; padding: 20px;"
                  f" border-radius: 10px; border: 1px solid"
                  f" #1e293b;'>{reporte_medico}</div>",
                  unsafe_allow_html=True,
              )

            with tab_paciente:
              st.markdown(
                  "<div style='background-color: #0f141f; padding: 20px;"
                  f" border-radius: 10px; border: 1px solid"
                  f" #1e293b;'>{reporte_paciente}</div>",
                  unsafe_allow_html=True,
              )

        except Exception as e:
          st.error(
              "⚠️ Ocurrió un error al procesar la solicitud. Detalle técnico:"
              f" {e}"
          )
  else:
    st.info(
        "👈 Ingresa el nombre, datos antropométricos y signos vitales en el panel"
        " izquierdo y presiona **'Ejecutar Pre-Triaje Clínico'** para generar"
        " los reportes instantáneos."
    )
