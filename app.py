import streamlit as st

st.set_page_config(page_title="Sistema Experto - Triaje Médico", page_icon="🩺", layout="centered")

st.title("🩺 Sistema Experto de Diagnóstico Médico Rápido")
st.caption("Especialidad: Neumología y Salud Respiratoria")
st.markdown("---")

st.sidebar.header("📋 Evaluación del Paciente")
edad = st.sidebar.number_input("Edad del paciente", min_value=1, max_value=120, value=35)
genero = st.sidebar.selectbox("Género", ["Femenino", "Masculino"])

st.sidebar.subheader("Síntomas Presentes")
dolor_pecho = st.sidebar.checkbox("Dolor precordial / Pecho opresivo")
dificultad_respirar = st.sidebar.checkbox("Dificultad para respirar (Disnea)")
fiebre = st.sidebar.checkbox("Fiebre (>= 38°C)")
tos = st.sidebar.checkbox("Tos persistente")
secrecion_nasal = st.sidebar.checkbox("Congestión / Secreción nasal")
dias_sintomas = st.sidebar.slider("Días de evolución con los síntomas", 1, 30, 3)

if st.sidebar.button("🔍 Evaluar Diagnóstico", type="primary"):
    st.subheader("📊 Reporte de Evaluación de Triaje")
    
    if dolor_pecho and dificultad_respirar:
        nivel_urgencia, diagnostico, tipo_alerta = "Urgencia Alta (Riesgo Vital)", "Posible Síndrome Coronario Agudo o Edema Pulmonar", "error"
        recomendacion = "Derivación inmediata a urgencias hospitalarias. No conduzca por sus propios medios."
    elif fiebre and dificultad_respirar and tos:
        nivel_urgencia, diagnostico, tipo_alerta = "Urgencia Alta", "Cuadro compatible con Neumonía / Infección Respiratoria Baja", "error"
        recomendacion = "Requiere evaluación médica presencial urgente y radiografía de tórax."
    elif (fiebre and tos) or (tos and dias_sintomas > 7):
        nivel_urgencia, diagnostico, tipo_alerta = "Urgencia Media", "Sospecha de Bronquitis Aguda o Infección en Evolución", "warning"
        recomendacion = "Programe una cita médica en atención primaria dentro de 24 a 48 horas."
    elif secrecion_nasal or tos:
        nivel_urgencia, diagnostico, tipo_alerta = "Urgencia Baja", "Sintomatología compatible con Resfriado Común / Rinitis", "success"
        recomendacion = "Reposo, hidratación constante y vigilancia de signos de alarma."
    else:
        nivel_urgencia, diagnostico, tipo_alerta = "Sin Urgencia", "No se detectan patrones de riesgo respiratorio", "info"
        recomendacion = "Mantenga hábitos de vida saludables."

    # Nivel de Urgencia
    if tipo_alerta == "error": 
        st.error(f"🚨 **Nivel de Prioridad:** {nivel_urgencia}")
    elif tipo_alerta == "warning": 
        st.warning(f"⚠️ **Nivel de Prioridad:** {nivel_urgencia}")
    elif tipo_alerta == "success": 
        st.success(f"✅ **Nivel de Prioridad:** {nivel_urgencia}")
    else: 
        st.info(f"ℹ️ **Nivel de Prioridad:** {nivel_urgencia}")

    # Diagnóstico y Tiempo de Evolución
    st.markdown("### 🩺 **Diagnóstico Presuntivo**")
    st.info(f"**{diagnostico}**")
    
    st.markdown(f"⏱️ **Tiempo de Evolución:** {dias_sintomas} días")

    # Recomendación Médica
    st.markdown("### 💡 **Recomendación Médica**")
    st.write(recomendacion)
