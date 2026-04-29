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

    # ---------- 2. Tabla Principal (formato Excel, compacta) ----------
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")

    sec_row = []
    for s in steps:
        if len(s) == 1:
            sec_row.append(s[0])
        else:
            sec_row.append(f"({' '.join(s)})")
    
    sensor_row = [f"K{i+1}" for i in range(n)]
    signal_row = [" ".join(signal_map[m] for m in s) for s in steps]
    binary_row = [" ".join(binary_map[m] for m in s) for s in steps]
    
    cols = st.columns(n)
    for j, col in enumerate(cols):
        with col:
            st.markdown(f"**{sec_row[j]}**")
            st.write(sensor_row[j])
            st.write(signal_row[j])
            st.write(binary_row[j])
    
    st.markdown("---")
    
    # ---------- 3. Bloques con formato de tabla (barras y separadores) ----------
    st.markdown("### Bloques")

    # Calcular estados resultantes de cada paso
    step_states = []
    for s in steps:
        states = [binary_map[m] for m in s]
        states.sort()
        step_states.append(" ".join(states))

    last_step_state = step_states[-1] if step_states else ""

    for idx, s in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        # ---- Fila de condiciones (cabecera del bloque) ----
        if idx == 1:
            prev_sensor = "Inicio"
            condition = last_step_state
        else:
            prev_sensor = f"K{idx-1}"
            condition = step_states[idx-2]
        
        next_sensor = f"K{(idx % n) + 1}" if idx % n != 0 else "K1"
        reset_sensor = f"K{idx}"
        
        # Construir la tabla en markdown
        # Primera fila: | Inicio | A0 | K2 | K1 |
        row1 = f"| {prev_sensor} | {condition} | {next_sensor} | {reset_sensor} |"
        # Separador: | --- | --- | --- | --- |
        separator = "| --- | --- | --- | --- |"
        
        # Filas de señales: una por movimiento en este paso
        # | K1 |   |   | Y1 |
        signal_rows = []
        for mov in s:
            sig = signal_map[mov]
            signal_rows.append(f"| K{idx} |   |   | {sig} |")
        
        # Mostrar la tabla
        st.markdown(row1)
        st.markdown(separator)
        for sr in signal_rows:
            st.markdown(sr)
        
        st.markdown("")  # línea blanca entre bloques

    st.caption("")
