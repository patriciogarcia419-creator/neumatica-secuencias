import streamlit as st

st.set_page_config(page_title="Neumática - Tablas de Secuencia", layout="wide")
st.title("Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Introduce la secuencia, ej: `(A+B+)B-A-`")

secuencia = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="visible")

if st.button("Generar Tabla", type="primary"):
    seq = secuencia.strip().upper().replace(" ", "")
    
    # Parsear
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

    signal_map = {'A+':'Y1','A-':'Y2','B+':'Y3','B-':'Y4','C+':'Y5','C-':'Y6'}
    binary_map = {'A+':'A1','A-':'A0','B+':'B1','B-':'B0','C+':'C1','C-':'C0'}
    n = len(steps)

    # ---------- Tabla Principal (con st.columns, como la que usabas) ----------
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")

    # Construir las filas
    sec_row = []
    for s in steps:
        if len(s) == 1:
            sec_row.append(s[0])
        else:
            sec_row.append(f"({' '.join(s)})")
    sensor_row = [f"K{i+1}" for i in range(n)]
    signal_row = [" ".join(signal_map[m] for m in s) for s in steps]
    binary_row = [" ".join(binary_map[m] for m in s) for s in steps]

    # Mostrar en columnas
    cols = st.columns(n)
    for j, col in enumerate(cols):
        with col:
            st.markdown(f"**{sec_row[j]}**")
            st.write(sensor_row[j])
            st.write(signal_row[j])
            st.write(binary_row[j])

    st.markdown("---")

    # ---------- Bloques (ya están correctos, no los cambio) ----------
    st.markdown("### Bloques")

    # Estados resultantes de cada paso
    step_states = []
    for s in steps:
        states = [binary_map[m] for m in s]
        states.sort()
        step_states.append(" ".join(states))
    last_step_state = step_states[-1] if step_states else ""

    w1, w2, w3, w4 = 8, 8, 5, 5

    for idx, s in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        if idx == 1:
            prev = "Inicio"
            cond = last_step_state
        else:
            prev = f"K{idx-1}"
            cond = step_states[idx-2]
        next_sensor = f"K{(idx % n) + 1}" if idx % n != 0 else "K1"
        reset = f"K{idx}"
        line1 = f"{prev:<{w1}}{cond:<{w2}}{next_sensor:<{w3}}{reset}"
        st.code(line1, language="text")
        
        # Para cada movimiento en el paso
        if len(s) == 1:
            # Movimiento individual: dos líneas (vacía + señal)
            sig = signal_map[s[0]]
            st.code(f"K{idx:<{w1-1}}{'':<{w2}}{'':<{w3}}{''}", language="text")
            st.code(f"K{idx:<{w1-1}}{'':<{w2}}{'':<{w3}}{sig}", language="text")
        else:
            # Paralelo: una línea por cada movimiento con su señal
            for mov in s:
                sig = signal_map[mov]
                st.code(f"K{idx:<{w1-1}}{'':<{w2}}{'':<{w3}}{sig}", language="text")
        
        st.markdown("")  # línea blanca

    st.caption("")
