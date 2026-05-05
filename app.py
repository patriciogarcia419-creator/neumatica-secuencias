import streamlit as st

st.set_page_config(page_title="Neumática - Tablas de Secuencia", layout="wide")
st.title("Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Introduce la secuencia, ej: `(A+B+)B-A-` o `A+B+C+D+E+F-`")

secuencia = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="visible")

if st.button("🚀 Generar Tabla", type="primary"):
    seq = secuencia.strip().upper().replace(" ", "")
   
    # Parsear secuencia
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

    # ==================== MAPAS ACTUALIZADOS HASTA F ====================
    signal_map = {
        'A+':'Y1', 'A-':'Y2',
        'B+':'Y3', 'B-':'Y4',
        'C+':'Y5', 'C-':'Y6',
        'D+':'Y7', 'D-':'Y8',
        'E+':'Y9', 'E-':'Y10',
        'F+':'Y11','F-':'Y12'
    }
    binary_map = {
        'A+':'A1', 'A-':'A0',
        'B+':'B1', 'B-':'B0',
        'C+':'C1', 'C-':'C0',
        'D+':'D1', 'D-':'D0',
        'E+':'E1', 'E-':'E0',
        'F+':'F1', 'F-':'F0'
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
            sec_row.append(f"({' + '.join(s)})")

    sensor_row = [f"K{i+1}" for i in range(n)]
    signal_row = [" ".join(signal_map.get(m, "??") for m in s) for s in steps]
    binary_row = [" ".join(binary_map.get(m, "??") for m in s) for s in steps]

    # Mostrar en columnas (mejor para varias columnas)
    cols = st.columns(n)
    for j, col in enumerate(cols):
        with col:
            st.markdown(f"**{sec_row[j]}**")
            st.write("**sensor**")
            st.write(sensor_row[j])
            st.write("**señales**")
            st.write(signal_row[j])
            st.write("**Sec. bin**")
            st.write(binary_row[j])

    st.markdown("---")

    # ---------- Bloques ----------
    st.markdown("### Bloques")

    for idx, s in enumerate(steps, start=1):
        move_str = " + ".join(s) if len(s) > 1 else s[0]
        signals = " ".join(signal_map.get(m, "??") for m in s)
        
        st.markdown(f"**Bloque {idx}** ─ {move_str}")
        
        if idx == 1:
            st.text("Inicio     B0     K2     K1")
            st.text(f"K1                          {signals}")
        else:
            prev_binary = " ".join(binary_map.get(m, "??") for m in steps[idx-2])
            st.text(f"K{idx-1}      {prev_binary}     K{idx}     K{idx-1}")
            st.text(f"K{idx}                          {signals}")
        
        st.text("─" * 60)

    st.caption("Generador actualizado hasta cilindro F")
