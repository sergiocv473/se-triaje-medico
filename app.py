import streamlit as st

st.set_page_config(page_title="Sistema de Triaje Respiratorio", layout="centered")

# Encabezado institucional estilo ficha clínica
st.title("Módulo de Triaje Respiratorio")
st.caption("Protocolo Institucional de Evaluación Preliminar de Pacientes")
st.markdown("---")

# Formulario de Admisión
st.sidebar.header("Admisión del Paciente")
edad = st.sidebar.number_input("Edad (años)", min_value=1, max_value=120, value=35)
genero = st.sidebar.selectbox("Sexo", ["Femenino", "Masculino"])

st.sidebar.subheader("Sintomatología")
dolor_pecho = st.sidebar.checkbox("Dolor torácico / Opresión")
dificultad_respirar = st.sidebar.checkbox("Dificultad respiratoria (Disnea)")
fiebre = st.sidebar.checkbox("Fiebre (>= 38°C)")
tos = st.sidebar.checkbox("Tos persistente")
secrecion_nasal = st.sidebar.checkbox("Congestión / Rinorrea")
dias_sintomas = st.sidebar.slider("Tiempo de evolución (días)", 1, 30, 3)

if st.sidebar.button("Procesar Triaje", type="primary"):
    st.subheader("Resultado de la Clasificación")
    
    if dolor_pecho and dificultad_respirar:
        prioridad = "PRIORIDAD I — Emergencia (Riesgo Vital)"
        alerta_fn = st.error
        diagnostico = "Sospecha de evento cardiovascular agudo o insuficiencia respiratoria severa."
        conducta = "Ingreso inmediato a Shock Trauma / Urgencias. Requerida valoración médica prioritaria."
    elif fiebre and dificultad_respirar and tos:
        prioridad = "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.error
        diagnostico = "Infección de vías respiratorias bajas (probable neumonía)."
        conducta = "Derivar a consulta médica general el mismo día. Solicitar radiografía de tórax."
    elif (fiebre and tos) or (tos and dias_sintomas > 7):
        prioridad = "PRIORIDAD III — Urgencia Menor"
        alerta_fn = st.warning
        diagnostico = "Cuadro agudo de vías respiratorias (probable bronquitis o infección viral en evolución)."
        conducta = "Programar atención ambulatoria en consultorio externo (24-48 horas)."
    elif secrecion_nasal or tos:
        prioridad = "PRIORIDAD IV — Patología No Urgente"
        alerta_fn = st.success
        diagnostico = "Sintomatología compatible con resfriado común o rinitis aguda."
        conducta = "Manejo ambulatorio sintomático, hidratación y pautas de alarma."
    else:
        prioridad = "PRIORIDAD V — Consulta General"
        alerta_fn = st.info
        diagnostico = "Sin criterios de prioridad respiratoria al momento de la evaluación."
        conducta = "Continuar con controles habituales de salud."

    # Bloque de clasificación clínica
    alerta_fn(f"**Nivel de Atención:** {prioridad}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Impresión Clínica Presuntiva:**")
        st.write(diagnostico)
    with col2:
        st.markdown("**Evolución:**")
        st.write(f"{dias_sintomas} días")

    st.markdown("---")
    st.markdown("**Conducta y Manejo Sugerido:**")
    st.info(conducta)
