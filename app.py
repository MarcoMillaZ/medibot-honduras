import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="MediBot-Honduras | Sistema de Pre-Triaje IA",
    page_icon="🤖",
    layout="wide",
)

# Estilo visual Futurista / Médico Minimalista (Modo Oscuro Clínico)
st.markdown(
    """
    <style>
    .main { background-color: #05070b; color: #e2e8f0; }
    .stForm { background-color: #0f141f; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .stMetric { background-color: #131b2e; padding: 15px; border-radius: 8px; border: 1px solid #1e3a8a; }
    h1, h2, h3 { color: #38bdf8 !important; font-family: 'Inter', sans-serif; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style='padding: 10px 0; border-bottom: 2px solid #0284c7; margin-bottom: 20px;'>
        <h1 style='margin: 0; font-size: 2.2rem;'>🤖 MEDIBOT-HONDURAS</h1>
        <p style='color: #94a3b8; font-size: 1.1rem; margin-top: 5px;'>Plataforma de Pre-Triaje Clínico Asistido por Inteligencia Artificial</p>
    </div>
""",
    unsafe_allow_html=True,
)

col_izq, col_der = st.columns([1, 1.8], gap="large")

with col_izq:
  st.markdown("### 🧬 Datos y Constantes")
  with st.form("formulario_triaje"):
    nombre_paciente = st.text_input(
        "Nombre Completo del Paciente", "Ej. Juan Pérez"
    )

    col_sub1, col_sub2, col_sub3 = st.columns(3)
    with col_sub1:
      edad = st.number_input("Edad", min_value=1, max_value=120, value=16)
    with col_sub2:
      peso = st.number_input(
          "Peso (kg)", min_value=2.0, max_value=200.0, value=60.0, step=0.5
      )
    with col_sub3:
      estatura = st.number_input(
          "Estatura (cm)", min_value=40, max_value=230, value=170
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

    enviar = st.form_submit_button(
        "⚡ EJECUTAR PRE-TRIAJE CLÍNICO", use_container_width=True
    )

with col_der:
  st.markdown("### 📊 Consola de Diagnóstico e Informes")

  if enviar:
    if not nombre_paciente.strip():
      st.error("⚠️ Por favor, ingresa el nombre del paciente antes de continuar.")
    else:
      with st.spinner("Procesando biométricos en tiempo real..."):
        # Cálculo analítico clínico instantáneo (Simulación de Motor Experto)
        imc = peso / ((estatura / 100) ** 2)

        # Lógica de Triaje basada en constantes vitales
        if temperatura >= 38.5 or oxigeno < 92 or pulso > 120 or pulso < 50:
          nivel_urgencia = (
              "🔴 CÓDIGO ROJO (Atención Médica Inmediata / Urgencia)"
          )
          color_alerta = "#ef4444"
        elif (
            (37.5 <= temperatura < 38.5)
            or (92 <= oxigeno < 95)
            or (100 < pulso <= 120)
        ):
          nivel_urgencia = "🟡 CÓDIGO AMARILLO (Atención Prioritaria / Precaución)"
          color_alerta = "#f59e0b"
        else:
          nivel_urgencia = "🟢 CÓDIGO VERDE (Paciente Estable / Consulta General)"
          color_alerta = "#10b981"

        # Reporte Formal para el Médico
        reporte_medico = f"""
### 📋 REPORTE CLÍNICO DE EVALUACIÓN INICIAL
- **Paciente:** {nombre_paciente} | **Edad:** {edad} años
- **Antropometría:** Peso: {peso} kg | Estatura: {estatura} cm | IMC: {imc:.2f} kg/m²
- **Clasificación de Urgencia:** <span style='color: {color_alerta}; font-weight: bold;'>{nivel_urgencia}</span>

#### 🔍 Análisis Biométrico y Hemodinámico:
* **Temperatura Corporal:** {temperatura} °C ({'Fiebre detectada' if temperatura >= 37.5 else 'Normotermia / Normal'})
* **Saturación de Oxígeno (SpO2):** {oxigeno}% ({'Hipoxia leve/moderada' if oxigeno < 95 else 'Oxigenación óptima'})
* **Frecuencia Cardíaca:** {pulso} lpm ({'Taquicardia' if pulso > 100 else 'Bradicardia' if pulso < 60 else 'Ritmo normal'})

#### 📝 Motivo de Consulta y Hallazgos:
- **Síntomas reportados:** *{sintomas}*
- **Sospecha Clínica Preliminar:** Cuadro sintomático asociado a procesos inflamatorios leves o fatiga metabólica. Se sugiere exploración física detallada, control de signos vitales cada 4 horas y descarte de patologías infecciosas agudas.
        """

        # Explicación Amigable para el Paciente
        reporte_paciente = f"""
### 👤 INFORME Y ORIENTACIÓN PARA EL PACIENTE
Hola **{nombre_paciente}**, hemos procesado tus datos y constantes vitales en nuestro sistema de pre-triaje.

#### 📊 Resumen de tu Estado Actual:
* Tu temperatura es de **{temperatura} °C** y tu nivel de oxígeno en la sangre es de **{oxigeno}%**.
* Tu frecuencia cardiaca se encuentra en **{pulso} latidos por minuto**.

#### 💡 Recomendaciones Generales:
1. **Descanso:** Toma un tiempo de reposo en un ambiente fresco y tranquilo.
2. **Hidratación:** Consume abundante agua para mantener tus niveles corporales estables.
3. **Monitoreo:** Si llegas a presentar dificultad para respirar, mareos intensos o fiebre que no baja, acude de inmediato al centro médico más cercano.
        """

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
  else:
    st.info(
        "👈 Ingresa el nombre, datos antropométricos y signos vitales en el panel"
        " izquierdo y presiona **'Ejecutar Pre-Triaje Clínico'** para generar"
        " los reportes instantáneos."
    )
