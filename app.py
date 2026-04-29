import streamlit as st

st.set_page_config(page_title="Neumática - Tablas de Secuencia", layout="wide")
st.title("Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Introduce la secuencia, ej: `(A+B+)B-A-`")

secuencia = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="visible")

if st.button("Generar Tabla", type="primary"):
    seq = secuencia.strip().upper().replace(" ", "")
    
    # ---------- 1. Parsear la secuencia ----------
    steps = []          # lista de pasos, cada paso es lista de strings ["A+","B+"] o ["B-"]
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

    # ---------- 2. Tabla Principal ----------
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")

    # Encabezado de secuencia
    sec_header = ["Secuencia"]
    for s in steps:
        if len(s) == 1:
            sec_header.append(s[0])
        else:
            sec_header.append(f"({' '.join(s)})")
    
    sensor_row = ["sensor"] + [f"K{i+1}" for i in range(n)]
    signal_row = ["señales"] + [" ".join(signal_map[m] for m in s) for s in steps]
    # Secuencia bin: estado DESPUÉS de cada paso (lo que se activa)
    bin_after = ["Sec. bin"] + [" ".join(binary_map[m] for m in s) for s in steps]

    table_data = [sec_header, sensor_row, signal_row, bin_after]
    st.table(list(map(list, zip(*table_data))))

    # ---------- 3. Bloques ----------
    st.markdown("### Bloques")

    # Calcular el estado resultante de cada paso (para usar como condición del bloque siguiente)
    # Guardamos para cada paso la lista de estados que produce
    step_states = []  # lista de strings con los estados (ej: "A1 B1")
    for s in steps:
        states = [binary_map[m] for m in s]
        states.sort()
        step_states.append(" ".join(states))

    # Para el bloque 1, la condición es el estado del último paso
    last_step_state = step_states[-1] if step_states else ""

    for idx, s in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        # ---- Primera línea ----
        if idx == 1:
            prev_sensor = "Inicio"
            condition = last_step_state
        else:
            prev_sensor = f"K{idx-1}"
            condition = step_states[idx-2]  # estado del paso anterior
        
        next_sensor = f"K{(idx % n) + 1}" if idx % n != 0 else "K1"
        reset_sensor = f"K{idx}"
        
        # Usamos espacios fijos para que se vea como en tu ejemplo
        line1 = f"{prev_sensor}     {condition}     {next_sensor}     {reset_sensor}"
        st.text(line1)
        
        # ---- Líneas de salida (una por cada movimiento del paso) ----
        for mov in s:
            sig = signal_map[mov]
            st.text(f"K{idx}                          {sig}")
        
        st.text("")  # línea vacía entre bloques

    st.caption("")  # sin mensajes extra
