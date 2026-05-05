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
    
    # ================== MAPAS ACTUALIZADOS HASTA F ==================
    signal_map = {
        'A+':'Y1','A-':'Y2',
        'B+':'Y3','B-':'Y4',
        'C+':'Y5','C-':'Y6',
        'D+':'Y7','D-':'Y8',
        'E+':'Y9','E-':'Y10',
        'F+':'Y11','F-':'Y12'
    }
    
    binary_map = {
        'A+':'A1','A-':'A0',
        'B+':'B1','B-':'B0',
        'C+':'C1','C-':'C0',
        'D+':'D1','D-':'D0',
        'E+':'E1','E-':'E0',
        'F+':'F1','F-':'F0'
    }
    
    n = len(steps)
    
    # ---------- Tabla Principal ----------
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")
    
    sec_row = []
    for s in steps:
        if len(s) == 1:
            sec_row.append(s[0])
        else:
            sec_row.append(f"({' '.join(s)})")
    
    sensor_row = [f"K{i+1}" for i in range(n)]
    signal_row = [" ".join(signal_map.get(m, "??") for m in s) for s in steps]
    binary_row = [" ".join(binary_map.get(m, "??") for m in s) for s in steps]
    
    cols = st.columns(n)
    for j, col in enumerate(cols):
        with col:
            st.markdown(f"**{sec_row[j]}**")
            st.write(sensor_row[j])
            st.write(signal_row[j])
            st.write(binary_row[j])
    
    st.markdown(f"**Total de bloques: {n}**")
    st.markdown("---")
    
    # ---------- Bloques ----------
    st.markdown("### Bloques")
    
    step_states = []
    for s in steps:
        states = [binary_map.get(m, "??") for m in s]
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
       
        if len(s) == 1:
            sig = signal_map.get(s[0], "??")
            st.code(f"K{idx:<{w1-1}}{'':<{w2}}{'':<{w3}}{sig}", language="text")
        else:
            for mov in s:
                sig = signal_map.get(mov, "??")
                st.code(f"K{idx:<{w1-1}}{'':<{w2}}{'':<{w3}}{sig}", language="text")
       
        st.markdown("")

    st.caption("")
