import streamlit as st

st.set_page_config(page_title="Neumática - Tablas de Secuencia", layout="wide")
st.title("Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Introduce la secuencia, ej: `(A+B+)B-A-`")

secuencia = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="visible")

if st.button("Generar Tabla", type="primary"):
    seq = secuencia.strip().upper().replace(" ", "")
    
    # ---------- 1. Parsear la secuencia ----------
    steps = []
    i = 0
    while i < len(seq):
        if seq[i] == '(':
            j = seq.find(')', i)
            grupo = seq[i+1:j]
            movs = []
            k = 0
            while k < len(grupo):
                if k+1 < len(grupo) and grupo[k+1] in '+-':
                    movs.append(grupo[k] + grupo[k+1])
                    k += 2
                else:
                    k += 1
            if movs:
                steps.append(movs)
            i = j + 1
        else:
            if i+1 < len(seq) and seq[i+1] in '+-':
                steps.append([seq[i] + seq[i+1]])
                i += 2
            else:
                i += 1

    # Mapeos fijos
    signal_map = {'A+':'Y1','A-':'Y2','B+':'Y3','B-':'Y4','C+':'Y5','C-':'Y6'}
    binary_map = {'A+':'A1','A-':'A0','B+':'B1','B-':'B0','C+':'C1','C-':'C0'}

    n = len(steps)

    # ---------- 2. Tabla Principal (formato Excel) ----------
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")

    # Construir las filas como en Excel:
    # Fila 1: secuencia (cada celda: un movimiento o grupo)
    # Fila 2: sensor (K1, K2, ...)
    # Fila 3: señales (Y...)
    # Fila 4: Secuencia bin (A1, B0, etc.)
    
    # Encabezado de secuencia: celdas individuales
    sec_row = []
    for s in steps:
        if len(s) == 1:
            sec_row.append(s[0])
        else:
            sec_row.append(f"({' '.join(s)})")
    
    sensor_row = [f"K{i+1}" for i in range(n)]
    signal_row = [" ".join(signal_map[m] for m in s) for s in steps]
    binary_row = [" ".join(binary_map[m] for m in s) for s in steps]
    
    # Mostrar como tabla de 4 filas (cada fila es una lista de celdas)
    # Streamlit necesita que cada fila tenga el mismo número de columnas.
    # Usamos st.columns para imitar el aspecto de Excel.
    
    # Número de columnas = n
    cols = st.columns(n)
    for j, col in enumerate(cols):
        with col:
            st.markdown(f"**{sec_row[j]}**")
            st.write(sensor_row[j])
            st.write(signal_row[j])
            st.write(binary_row[j])
    
    # Separador
    st.markdown("---")
    
    # ---------- 3. Bloques (sin cambios, ya funciona) ----------
    st.markdown("### Bloques")

    # Calcular el estado resultante de cada paso
    step_states = []
    for s in steps:
        states = [binary_map[m] for m in s]
        states.sort()
        step_states.append(" ".join(states))

    last_step_state = step_states[-1] if step_states else ""

    for idx, s in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        if idx == 1:
            prev_sensor = "Inicio"
            condition = last_step_state
        else:
            prev_sensor = f"K{idx-1}"
            condition = step_states[idx-2]
        
        next_sensor = f"K{(idx % n) + 1}" if idx % n != 0 else "K1"
        reset_sensor = f"K{idx}"
        
        line1 = f"{prev_sensor}     {condition}     {next_sensor}     {reset_sensor}"
        st.text(line1)
        
        for mov in s:
            sig = signal_map[mov]
            st.text(f"K{idx}                          {sig}")
        
        st.text("")

    st.caption("")
