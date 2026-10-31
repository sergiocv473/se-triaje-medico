import streamlit as st

st.set_page_config(page_title="Sistema de Triaje Respiratorio", layout="centered")

# Encabezado institucional
st.title("Módulo de Triaje Respiratorio")
st.caption("Protocolo Institucional de Evaluación Preliminar de Pacientes")
st.markdown("---")

# Formulario de Admisión
st.sidebar.header("Admisión del Paciente")
edad = st.sidebar.number_input("Edad (años)", min_value=1, max_value=120, value=25)
genero = st.sidebar.selectbox("Sexo", ["Femenino", "Masculino"])

st.sidebar.subheader("Sintomatología")
dolor_pecho = st.sidebar.checkbox("Dolor torácico / Opresión")
dificultad_respirar = st.sidebar.checkbox("Dificultad respiratoria (Disnea)")
fiebre = st.sidebar.checkbox("Fiebre (>= 38°C)")
tos = st.sidebar.checkbox("Tos persistente")
secrecion_nasal = st.sidebar.checkbox("Congestión / Rinorrea")
dias_sintomas = st.sidebar.slider("Tiempo de evolución (días)", 1, 30, 5)

if st.sidebar.button("Procesar Triaje", type="primary"):
    st.subheader("Resultado de la Clasificación")
    
    # Banderas de evaluación lógica
    es_vulnerable = edad < 5 or edad >= 65
    sintomas_totales = sum([dolor_pecho, dificultad_respirar, fiebre, tos, secrecion_nasal])
    
    # 1. EMERGENCIAS Y RIESGO VITAL (Prioridad I)
    if dolor_pecho and dificultad_respirar:
        prioridad = "PRIORIDAD I — Emergencia (Riesgo Vital)"
        alerta_fn = st.error
        diagnostico = "Síndrome coronario agudo vs. Embolia pulmonar o Neumotórax."
        conducta = "Atención e ingreso inmediato a área de Shock Trauma."

    elif dificultad_respirar and (es_vulnerable or fiebre):
        prioridad = "PRIORIDAD I — Emergencia"
        alerta_fn = st.error
        diagnostico = f"Insuficiencia respiratoria aguda en paciente {'vulnerable' if es_vulnerable else 'con síndrome febril'}."
        conducta = "Evaluación prioritaria en urgencias con monitorización y oxigenoterapia."

    # 2. URGENCIAS MAYORES (Prioridad II)
    elif fiebre and dificultad_respirar and tos:
        prioridad = "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.error
        diagnostico = "Infección respiratoria baja / Neumonía clínica presuntiva."
        conducta = "Evaluación médica presencial urgente, radiografía de tórax y exámenes de laboratorio."

    elif dolor_pecho:
        prioridad = "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.error
        diagnostico = "Dolor torácico en estudio (Descarte cardiovascular o pleurítico)."
        conducta = "Electrocardiograma de urgencia y valoración por médico de guardia."

    elif dificultad_respirar:
        prioridad = "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.error
        diagnostico = "Disnea de origen a determinar (Descarte broncoespasmo / hiperreactividad)."
        conducta = "Evaluación médica rápida y oximetría de pulso."

    elif fiebre and dias_sintomas > 7:
        prioridad = "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.warning
        diagnostico = f"Síndrome febril prolongado ({dias_sintomas} días de evolución). Riesgo de complicación o bacteriemia."
        conducta = "Iniciar protocolo de estudio febril (analítica sanguínea y examen de orina urgente)."

    # 3. URGENCIAS MENORES (Prioridad III)
    elif tos and dias_sintomas > 14:
        prioridad = "PRIORIDAD III — Urgencia Menor"
        alerta_fn = st.warning
        diagnostico = f"Tos subaguda/crónica ({dias_sintomas} días). Descarte de Tuberculosis (TBC) o patología intersticial."
        conducta = "Solicitar baciloscopía (BK en esputo) y cita con Neumología."

    elif (fiebre and tos) or (fiebre and secrecion_nasal):
        if es_vulnerable:
            prioridad = "PRIORIDAD II — Urgencia Mayor"
            alerta_fn = st.warning
            diagnostico = "Infección respiratoria aguda en grupo de riesgo edario."
            conducta = "Evaluación clínica presencial dentro de las primeras 12 horas."
        else:
            prioridad = "PRIORIDAD III — Urgencia Menor"
            alerta_fn = st.warning
            diagnostico = "Infección de vías respiratorias (Probable bronquitis o síndrome gripal)."
            conducta = "Consulta ambulatoria médica en 24 a 48 horas."

    elif fiebre:
        if dias_sintomas > 3:
            prioridad = "PRIORIDAD III — Urgencia Menor"
            alerta_fn = st.warning
            diagnostico = f"Síndrome febril sostenido ({dias_sintomas} días de evolución sin foco evidente)."
            conducta = "Atención ambulatoria para descarte de foco infeccioso."
        else:
            prioridad = "PRIORIDAD IV — Patología No Urgente"
            alerta_fn = st.info
            diagnostico = f"Síndrome febril agudo en inicio de evolución ({dias_sintomas} días)."
            conducta = "Control térmico con antipiréticos, hidratación y reevaluar si supera los 3 días."

    # 4. PATOLOGÍAS NO URGENTES (Prioridad IV)
    elif tos:
        prioridad = "PRIORIDAD IV — Patología No Urgente"
        alerta_fn = st.info
        diagnostico = f"Tos irritativa / Infección respiratoria alta ({dias_sintomas} días de evolución)."
        conducta = "Manejo sintomático y vigilancia de apariciones de disnea o fiebre."

    elif secrecion_nasal:
        prioridad = "PRIORIDAD IV — Patología No Urgente"
        alerta_fn = st.success
        diagnostico = "Rinofaringitis aguda / Rinitis sintomática."
        conducta = "Tratamiento sintomático ambulatorio y reposo relativo."

    # 5. CONSULTA GENERAL (Prioridad V)
    else:
        prioridad = "PRIORIDAD V — Consulta General / Preventiva"
        alerta_fn = st.info
        diagnostico = "Sin hallazgos ni sintomatología respiratoria activa manifestada."
        conducta = "Continuar con controles médicos habituales de salud."

    # Despliegue de Resultados
    alerta_fn(f"**Nivel de Atención:** {prioridad}")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("**Impresión Clínica Presuntiva:**")
        st.write(diagnostico)
    with col2:
        st.markdown("**Evolución:**")
        st.write(f"{dias_sintomas} días")
    with col3:
        st.markdown("**Condición:**")
        st.write("Grupo Vulnerable" if es_vulnerable else "Adulto Estándar")

    st.markdown("---")
    st.markdown("**Conducta y Manejo Sugerido:**")
    st.info(conducta)
