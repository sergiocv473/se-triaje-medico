import streamlit as st

st.set_page_config(page_title="Sistema de Triaje Respiratorio", layout="centered")

# Encabezado Institucional
st.title("Módulo de Triaje y Clasificación de Riesgo Respiratorio")
st.caption("Protocolo Clínico de Admisión Hospitalaria y Evaluación de Urgencias")
st.markdown("---")

# Panel Lateral de Admisión
st.sidebar.header("📋 Ficha de Admisión")
edad = st.sidebar.number_input("Edad del paciente (años)", min_value=1, max_value=120, value=35)
genero = st.sidebar.selectbox("Sexo biológico", ["Femenino", "Masculino"])

st.sidebar.subheader("Sintomatología Presente")
dolor_pecho = st.sidebar.checkbox("Dolor torácico / Opresión precordial")
dificultad_respirar = st.sidebar.checkbox("Dificultad para respirar (Disnea)")
fiebre = st.sidebar.checkbox("Fiebre medida (>= 38.0 °C)")
tos = st.sidebar.checkbox("Tos persistente")
secrecion_nasal = st.sidebar.checkbox("Congestión nasal / Rinorrea")
dias_sintomas = st.sidebar.slider("Tiempo de evolución (días)", 1, 30, 4)

if st.sidebar.button("⚙️ Procesar Triaje Clínico", type="primary"):
    st.subheader("📄 Dictamen de Triaje y Plan de Manejo")
    
    # ---------------------------------------------------------
    # 1. ESTRATIFICACIÓN DE RIESGO DEMOGRÁFICO Y TEMPORAL
    # ---------------------------------------------------------
    if edad < 5:
        grupo_etario = "Pediátrico (<5 años)"
        vulnerable = True
    elif edad < 18:
        grupo_etario = "Pediátrico / Adolescente"
        vulnerable = False
    elif edad >= 65:
        grupo_etario = "Adulto Mayor / Geriátrico"
        vulnerable = True
    else:
        grupo_etario = "Adulto Estándar"
        vulnerable = False

    if dias_sintomas <= 3:
        fase = "Fase Aguda (1-3 días)"
    elif 4 <= dias_sintomas <= 14:
        fase = "Fase Subaguda (4-14 días)"
    else:
        fase = "Fase Crónica / Prolongada (>14 días)"

    # Variables de salida
    prioridad = ""
    alerta_fn = st.info
    dx_principal = ""
    dx_diferenciales = []
    conducta = ""
    ordenes_medicas = []

    # ---------------------------------------------------------
    # 2. MOTOR DE INFERENCIA LÓGICA CLÍNICA
    # ---------------------------------------------------------
    
    # CASO 1: RED FLAGS / RIESGO VITAL INMINENTE (PRIORIDAD I)
    if dolor_pecho and dificultad_respirar:
        prioridad = "PRIORIDAD I — EMERGENCIA (Riesgo Vital Inminente)"
        alerta_fn = st.error
        if genero == "Femenino":
            dx_principal = f"Síndrome Coronario Agudo (Presentación Atípica) vs. Tromboembolismo Pulmonar (TEP)."
            dx_diferenciales = ["Neumotórax espontáneo", "Edema agudo de pulmón", "Disecación aórtica"]
        else:
            dx_principal = f"Síndrome Coronario Agudo Clásico (Infarto / Angina Inestable) vs. Neumotórax."
            dx_diferenciales = ["Tromboembolismo pulmonar", "Pericarditis aguda", "Síndrome de Boerhaave"]
        conducta = "Ingreso inmediato a Sala de Reanimación / Shock Trauma. No diferir atención."
        ordenes_medicas = [
            "Electrocardiograma (ECG) de 12 derivadas en < 10 minutos.",
            "Oximetría continua y administración de Oxígeno suplementario si SpO2 < 92%.",
            "Canalización de vía venosa periférica y dosaje de Troponinas T/I y Dímero D.",
            "Evaluación inmediata por Médico Intensivista o Cardiólogo de guardia."
        ]

    elif dificultad_respirar and vulnerable:
        prioridad = "PRIORIDAD I — EMERGENCIA"
        alerta_fn = st.error
        dx_principal = f"Insuficiencia Respiratoria Aguda Severa en paciente de grupo de alto riesgo ({grupo_etario})."
        dx_diferenciales = ["Neumonía grave", "Broncoespasmo severo / Crisis asmática", "Sepsis de punto de partida respiratorio"]
        conducta = "Pase directo a Box de Urgencias Prioritarias."
        ordenes_medicas = [
            "Monitoreo continuo de signos vitales (SpO2, FC, FR, PA).",
            "Radiografía de tórax portátil anteroposterior.",
            "Gasometría arterial (AGA) y hemograma completo."
        ]

    # CASO 2: URGENCIAS MAYORES (PRIORIDAD II)
    elif fiebre and dificultad_respirar and tos:
        prioridad = "PRIORIDAD II — URGENCIA MAYOR"
        alerta_fn = st.error
        dx_principal = f"Neumonía Adquirida en la Comunidad (NAC) - {fase}."
        dx_diferenciales = ["Bronconeumonía bacteriana", "Exacerbación de EPOC / Asma", "Infección por SARS-CoV-2 / Influenza grave"]
        conducta = "Ubicación en Área de Observación de Urgencias (Tiempo máx. de espera: 15 min)."
        ordenes_medicas = [
            "Radiografía de tórax digital (PA y lateral).",
            "Hemograma, Reactantes de Fase Aguda (PCR, Procalcitonina).",
            "Evaluación de escala CURB-65 / PSI para decidir hospitalización vs. manejo ambulatorio."
        ]

    elif dolor_pecho:
        prioridad = "PRIORIDAD II — URGENCIA MAYOR"
        alerta_fn = st.error
        dx_principal = f"Dolor Torácico en Estudio en paciente {grupo_etario} ({genero})."
        dx_diferenciales = ["Costocondritis / Dolor osteomuscular", "Pleuritis viral", "Espasmo esofágico"]
        conducta = "Evaluación médica en tópico de urgencias dentro de 15-20 minutos."
        ordenes_medicas = ["ECG de control de 12 derivadas.", "Toma de presión arterial en ambos brazos y auscultación cardíaca."]

    elif fiebre and dias_sintomas > 7:
        prioridad = "PRIORIDAD II — URGENCIA MAYOR"
        alerta_fn = st.warning
        dx_principal = f"Síndrome Febril Prolongado ({dias_sintomas} días de evolución). Riesgo de complicación bacteriana sistémica."
        dx_diferenciales = ["Infección fúngica o bacteriana atípica", "Absceso pulmonar", "Endocarditis infecciosa"]
        conducta = "Atención prioritaria para abordaje diagnóstico febril."
        ordenes_medicas = ["Hemocultivos seriados (x2)", "Examen general de orina y Urocultivo", "Analítica sanguínea completa."]

    # CASO 3: URGENCIAS MENORES (PRIORIDAD III)
    elif tos and dias_sintomas > 14:
        prioridad = "PRIORIDAD III — URGENCIA MENOR"
        alerta_fn = st.warning
        dx_principal = f"Criterio de Sintomático Respiratorio ({dias_sintomas} días con tos). Descarte obligatorio de Tuberculosis Pulmonar (TBC)."
        dx_diferenciales = ["Síndrome de tos de vías aéreas superiores", "Asma bronquial variante tos", "Bronquiectasias / Secuela pulmonar"]
        conducta = "Atención ambulatoria programada con protocolo de aislamiento preventivo."
        ordenes_medicas = [
            "Solicitud de Baciloscopía en esputo (BK x2 muestras) / GeneXpert MTB/RIF.",
            "Radiografía de tórax (Tele de Tórax).",
            "Interconsulta con el servicio de Neumología."
        ]

    elif (fiebre and tos) or (fiebre and secrecion_nasal):
        if vulnerable:
            prioridad = "PRIORIDAD II — URGENCIA MAYOR"
            alerta_fn = st.warning
            dx_principal = f"Infección Respiratoria Aguda Febril en paciente vulnerable ({grupo_etario})."
            dx_diferenciales = ["Influenza A/B", "Bronquitis aguda", "Neumonitis inicial"]
            conducta = "Evaluación médica presencial dentro del turno actual."
            ordenes_medicas = ["Auscultación pulmonar detenida", "Saturación de oxígeno por oximetría de pulso."]
        else:
            prioridad = "PRIORIDAD III — URGENCIA MENOR"
            alerta_fn = st.warning
            dx_principal = f"Traqueobronquitis Aguda / Síndrome Gripal ({fase})."
            dx_diferenciales = ["Infección por Adenovirus / Rhinovirus", "Faringoamigdalitis aguda", "Sinusitis aguda febril"]
            conducta = "Atención en consultorio externo de Medicina General (espera < 60 min)."
            ordenes_medicas = ["Prescripción de sintomáticos y pautas de alarma por escrito."]

    elif dificultad_respirar:
        prioridad = "PRIORIDAD III — URGENCIA MENOR"
        alerta_fn = st.warning
        dx_principal = f"Disnea Ligera/Moderada en Estudio ({dias_sintomas} días)."
        dx_diferenciales = ["Hiperreactividad bronquial", "Crisis de ansiedad / Hiperventilación", "Desacondicionamiento físico"]
        conducta = "Evaluación ambulatoria urgente para medición de flujo espiratorio."
        ordenes_medicas = ["Oximetría de pulso", "Prueba de respuesta a broncodilatador si hay sibilancias."]

    # CASO 4: PATOLOGÍAS NO URGENTES (PRIORIDAD IV)
    elif tos or secrecion_nasal or fiebre:
        prioridad = "PRIORIDAD IV — PATOLOGÍA NO URGENTE"
        alerta_fn = st.info
        if secrecion_nasal and tos:
            dx_principal = f"Rinofaringitis Aguda / Resfriado Común ({dias_sintomas} días de evolución)."
            dx_diferenciales = ["Rinitis alérgica agudizada", "Sinusitis catarral"]
        elif fiebre:
            dx_principal = f"Síndrome Febril Agudo Autolimitado ({dias_sintomas} días) en paciente {grupo_etario}."
            dx_diferenciales = ["Viremia inicial", "Reacción vacunal / Proceso viral leve"]
        else:
            dx_principal = f"Tos Irritativa de Vías Aéreas Superiores ({dias_sintomas} días)."
            dx_diferenciales = ["Goteo postnasal", "Laringitis leve"]
        conducta = "Atención en Consulta Externa o Centro de Salud de Atención Primaria."
        ordenes_medicas = ["Manejo sintomático ambulatorio (reposo, hidratación oral, paracetamol/ibuprofeno si hay fiebre)."]

    # CASO 5: CONSULTA GENERAL PREVENTIVA (PRIORIDAD V)
    else:
        prioridad = "PRIORIDAD V — CONSULTA GENERAL / PREVENTIVA"
        alerta_fn = st.success
        dx_principal = f"Sin Criterios de Patología Respiratoria Aguda al momento de la evaluación."
        dx_diferenciales = ["Evaluación preventiva de rutina", "Control de salud periódico"]
        conducta = "Derivación a consulta externa programada o medicina preventiva."
        ordenes_medicas = ["Actualización de esquema de vacunación (Influenza / Neumococo según edad)."]

    # ---------------------------------------------------------
    # 3. IMPRESIÓN Y DESPLIEGUE EN INTERFAZ
    # ---------------------------------------------------------
    alerta_fn(f"**Nivel de Atención Asignado:** {prioridad}")

    # Cuadro de Resumen Demográfico
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Edad / Sexo", f"{edad}a / {genero[0]}")
    with col2:
        st.metric("Perfil", grupo_etario.split()[0])
    with col3:
        st.metric("Evolución", f"{dias_sintomas} días")
    with col4:
        st.metric("Riesgo Edad", "Especial" if vulnerable else "Estándar")

    st.markdown("---")
    
    st.markdown("###  Impresión Clínica Presuntiva")
    st.write(f"**Diagnóstico Principal:** {dx_principal}")
    
    if dx_diferenciales:
        st.markdown("**Diagnósticos Diferenciales a Considerar:**")
        for dx in dx_diferenciales:
            st.write(f"- *{dx}*")

    st.markdown("---")
    st.markdown("###  Conducta Asistencial y Plan de Manejo")
    st.info(f"**Conducta:** {conducta}")

    st.markdown("**Órdenes Médicas / Indicaciones Inmediatas:**")
    for om in ordenes_medicas:
        st.write(f"✓ {om}")
