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
    st.subheader("Resultado de la Clasificación Clínica")
    
    # 1. Determinación del Perfil Demográfico y Factor de Riesgo
    if edad < 12:
        perfil_etario = "Pediátrico"
        factor_riesgo_edad = True
    elif edad >= 65:
        perfil_etario = "Adulto Mayor (Geriátrico)"
        factor_riesgo_edad = True
    else:
        perfil_etario = "Adulto"
        factor_riesgo_edad = False

    # 2. Evaluación de la Fase Temporal
    if dias_sintomas <= 3:
        fase_evolucion = "Fase Aguda (1-3 días)"
    elif 4 <= dias_sintomas <= 14:
        fase_evolucion = "Fase Subaguda (4-14 días)"
    else:
        fase_evolucion = "Fase Prolongada / Crónica (>14 días)"

    # 3. Motor de Inferencia Lógica Sensible a Edad, Sexo y Tiempo
    diagnostico = ""
    conducta = ""
    prioridad = ""
    alerta_fn = st.info

    # REGLAS DE ALTA PRIORIDAD / RIESGO VITAL
    if dolor_pecho and dificultad_respirar:
        prioridad = "PRIORIDAD I — Emergencia (Riesgo Vital)"
        alerta_fn = st.error
        if genero == "Femenino":
            diagnostico = f"Paciente {perfil_etario} ({genero}, {edad} años): Dolor torácico y disnea. Descarte de síndrome coronario agudo (presentación atípica en mujeres) vs. embolia pulmonar."
        else:
            diagnostico = f"Paciente {perfil_etario} ({genero}, {edad} años): Dolor torácico y disnea. Descarte de síndrome coronario agudo vs. neumotórax o embolia."
        conducta = "Ingreso inmediato a área de Shock Trauma. Electrocardiograma de urgencia, oximetría y monitoreo hemodinámico continuo."

    elif dolor_pecho:
        prioridad = "PRIORIDAD II — Urgencia Mayor" if factor_riesgo_edad else "PRIORIDAD II — Urgencia"
        alerta_fn = st.error
        if perfil_etario == "Pediátrico":
            diagnostico = f"Paciente Pediátrico ({genero}, {edad} años): Dolor torácico en estudio. Descarte de miocarditis, broncoespasmo severo o patología osteomuscular."
            conducta = "Evaluación pediátrica inmediata con auscultación y monitoreo de signos vitales."
        else:
            diagnostico = f"Paciente {perfil_etario} ({genero}, {edad} años): Dolor torácico en investigación."
            conducta = "Realizar ECG dentro de los primeros 10 minutos y valoración por médico de guardia."

    elif dificultad_respirar and (fiebre or factor_riesgo_edad):
        prioridad = "PRIORIDAD I — Emergencia" if factor_riesgo_edad else "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.error
        diagnostico = f"Paciente {perfil_etario} ({genero}, {edad} años): Disnea y compromiso clínico en {fase_evolucion.lower()}. Probable insuficiencia respiratoria o neumonía en grupo de riesgo."
        conducta = "Evaluación médica urgente, oximetría de pulso, gasometría arterial y radiografía de tórax."

    elif fiebre and tos and dificultad_respirar:
        prioridad = "PRIORIDAD I — Emergencia" if perfil_etario == "Pediátrico" else "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.error
        diagnostico = f"Infección respiratoria baja grave / Neumonía ({dias_sintomas} días de evolución) en paciente {perfil_etario} ({genero})."
        conducta = "Evaluación prioritaria en urgencias, solicitar hemograma, PCR y radiografía de tórax."

    # REGLAS BASADAS EN TIEMPO DE EVOLUCIÓN Y SÍNTOMAS ESPECÍFICOS
    elif tos and dias_sintomas > 14:
        prioridad = "PRIORIDAD II — Urgencia" if factor_riesgo_edad else "PRIORIDAD III — Urgencia Menor"
        alerta_fn = st.warning
        diagnostico = f"Paciente {perfil_etario} ({genero}): Criterio de Sintomático Respiratorio ({dias_sintomas} días con tos). Descarte obligatorio de Tuberculosis (TBC), asma o enfermedad intersticial."
        conducta = "Iniciación de protocolo de Sintomático Respiratorio (Baciloscopía / BK en esputo x2) y derivación a Neumología."

    elif fiebre and dias_sintomas > 7:
        prioridad = "PRIORIDAD II — Urgencia Mayor" if factor_riesgo_edad else "PRIORIDAD III — Urgencia Menor"
        alerta_fn = st.warning
        diagnostico = f"Síndrome febril prolongado ({dias_sintomas} días de evolución) en paciente {perfil_etario} ({genero}). Alto riesgo de foco bacteriano no detectado o complicación sistémica."
        conducta = "Batería analítica completa (hemograma, reactantes de fase aguda, uroanálisis) y evaluación médica presencial."

    elif (fiebre and tos) or (fiebre and secrecion_nasal):
        if factor_riesgo_edad:
            prioridad = "PRIORIDAD II — Urgencia Mayor"
            alerta_fn = st.warning
            diagnostico = f"Infección respiratoria aguda febril en paciente vulnerado por edad ({perfil_etario}, {edad} años, {dias_sintomas} días de evolución)."
            conducta = "Evaluación médica presencial dentro de las primeras 12 horas para prevenir descompensación."
        else:
            prioridad = "PRIORIDAD III — Urgencia Menor"
            alerta_fn = st.warning
            diagnostico = f"Infección respiratoria aguda de vías altas/medias ({dias_sintomas} días de evolución) en paciente {perfil_etario} ({genero})."
            conducta = "Atención ambulatoria en consultorio externo dentro de 24-48 horas y tratamiento sintomático."

    elif fiebre:
        if dias_sintomas <= 3:
            prioridad = "PRIORIDAD IV — Patología No Urgente"
            alerta_fn = st.info
            diagnostico = f"Síndrome febril agudo de corta evolución ({dias_sintomas} días) en paciente {perfil_etario} ({genero}). Probable etiología viral inicial."
            conducta = "Control térmico ambulatorio con antipiréticos, hidratación oral y vigilancia de signos de alarma."
        else:
            prioridad = "PRIORIDAD III — Urgencia Menor"
            alerta_fn = st.warning
            diagnostico = f"Síndrome febril persistente ({dias_sintomas} días) en paciente {perfil_etario} ({genero}). Descarte de foco infeccioso bacteriano."
            conducta = "Consulta médica ambulatoria para examen físico segmentario y descarte de foco infeccioso."

    elif dificultad_respirar:
        prioridad = "PRIORIDAD II — Urgencia Mayor"
        alerta_fn = st.error
        diagnostico = f"Disnea en estudio ({dias_sintomas} días) en paciente {perfil_etario} ({genero}). Evaluando hiperreactividad bronquial vs. causa cardiovascular."
        conducta = "Evaluación médica prioritaria con oximetría de pulso y auscultación pulmonar."

    elif tos:
        if perfil_etario == "Pediátrico" and dias_sintomas <= 5:
            prioridad = "PRIORIDAD III — Urgencia Menor"
            alerta_fn = st.warning
            diagnostico = f"Tos aguda en paciente pediátrico ({edad} años, {dias_sintomas} días). Descarte de laringotraqueítis o bronquiolitis inicial."
            conducta = "Evaluación por Pediatría o medicina general."
        else:
            prioridad = "PRIORIDAD IV — Patología No Urgente"
            alerta_fn = st.info
            diagnostico = f"Tos irritativa en {fase_evolucion.lower()} ({dias_sintomas} días) en paciente {perfil_etario} ({genero})."
            conducta = "Manejo sintomático ambulatorio y educación sobre signos de alarma."

    elif secrecion_nasal:
        prioridad = "PRIORIDAD IV — Patología No Urgente"
        alerta_fn = st.success
        diagnostico = f"Rinofaringitis aguda / Rinitis sintomática en paciente {perfil_etario} ({genero}, {dias_sintomas} días de evolución)."
        conducta = "Medidas generales de soporte, lavado nasal, hidratación y reposo relativo."

    else:
        prioridad = "PRIORIDAD V — Consulta General / Preventiva"
        alerta_fn = st.info
        diagnostico = f"Paciente {perfil_etario} ({genero}, {edad} años) sin sintomatología respiratoria activa manifestada."
        conducta = "Mantenimiento de controles de salud preventivos y vacunación según esquema de edad."

    # DESPLIEGUE DE RESULTADOS EN LA INTERFAZ
    alerta_fn(f"**Nivel de Atención:** {prioridad}")
    
    # Resumen Ficha de Paciente
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**Edad:**")
        st.write(f"{edad} años")
    with col2:
        st.markdown("**Sexo:**")
        st.write(genero)
    with col3:
        st.markdown("**Grupo Etario:**")
        st.write(perfil_etario)
    with col4:
        st.markdown("**Evolución:**")
        st.write(f"{dias_sintomas} días")

    st.markdown("---")
    
    st.markdown("### 🩺 **Impresión Clínica Presuntiva**")
    st.write(diagnostico)

    st.markdown("### 📋 **Conducta y Manejo Sugerido**")
    st.info(conducta)
