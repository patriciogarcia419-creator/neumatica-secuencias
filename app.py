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
    
    # ---------- 3. Bloques con formato bonito y alineado ----------
    st.markdown("### Bloques")

    # Calcular estados resultantes de cada paso
    step_states = []
    for s in steps:
        states = [binary_map[m] for m in s]
        states.sort()
        step_states.append(" ".join(states))

    last_step_state = step_states[-1] if step_states else ""

    # Ancho fijo para la primera columna (máximo "Inicio" o "K99")
    max_len = max(len("Inicio"), max(len(f"K{i}") for i in range(1, n+2)))
    first_col_width = max_len + 2  # espacios extra

    # Ancho fijo para la columna de condición (la más larga entre todos los estados)
    max_cond_len = max(len(step_states[0]), max(len(s) for s in step_states)) if step_states else 0
    cond_width = max_cond_len + 2

    # Ancho fijo para las columnas de sensores (K1, K2, ...)
    sensor_width = 4  # "K99" son 3, pero dejamos 4

    for idx, s in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        # ---- Primera línea ----
        if idx == 1:
            prev_sensor = "Inicio"
            condition = last_step_state
        else:
            prev_sensor = f"K{idx-1}"
            condition = step_states[idx-2]
        
        next_sensor = f"K{(idx % n) + 1}" if idx % n != 0 else "K1"
        reset_sensor = f"K{idx}"
        
        # Formatear con espacios fijos
        line1 = f"{prev_sensor:<{first_col_width}}{condition:<{cond_width}}{next_sensor:<{sensor_width}}{reset_sensor}"
        st.code(line1, language="text")
        
        # ---- Líneas de salida (una por movimiento) ----
        # La primera columna siempre es K{idx} alineada
        # La tercera columna es la señal (Yxx)
        for mov in s:
            sig = signal_map[mov]
            # Dos espacios en medio para simular el formato original
            line = f"K{idx:<{first_col_width-1}}{'':<{cond_width}}{sig}"
            st.code(line, language="text")
        
        st.markdown("")  # línea blanca separadora

    st.caption("")
