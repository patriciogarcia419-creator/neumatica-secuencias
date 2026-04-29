import streamlit as st

st.set_page_config(page_title="Secuencias Neumática", layout="wide")
st.title("🛠 Generador de Tablas Neumática")
st.markdown("Pega tu secuencia")

secuencia_input = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="hidden")

if st.button("🚀 Generar Tabla", type="primary"):
    seq = secuencia_input.strip().upper().replace(" ", "")
    
    # Parseo correcto
    movements = []
    i = 0
    while i < len(seq):
        if seq[i] == '(':
            j = seq.find(')', i)
            group = seq[i+1:j]
            parallel = []
            k = 0
            while k < len(group):
                if k + 1 < len(group) and group[k+1] in '+-':
                    parallel.append(group[k] + group[k+1])
                    k += 2
                else:
                    k += 1
            if parallel:
                movements.append(parallel)
            i = j + 1
        else:
            if i + 1 < len(seq) and seq[i+1] in '+-':
                movements.append([seq[i] + seq[i+1]])
                i += 2
            else:
                i += 1

    st.subheader(f"Secuencia: **{seq}**")

    # ==================== TABLA PRINCIPAL ====================
    st.markdown("### Tabla Principal")

    seq_header = ["Secuencia"] + [f"({'+'.join(m)})" if len(m)>1 else m[0] for m in movements]
    sensor_row = ["sensor"] + [f"K{i+1}" for i in range(len(movements))]

    signal_map = {'A+':'Y1', 'A-':'Y2', 'B+':'Y3', 'B-':'Y4', 'C+':'Y5', 'C-':'Y6'}
    binary_map = {'A+':'A1', 'A-':'A0', 'B+':'B1', 'B-':'B0', 'C+':'C1', 'C-':'C0'}

    signal_row = ["señales"] + [" ".join(signal_map.get(m, "??") for m in step) for step in movements]
    binary_row = ["Sec. bin"] + [" ".join(binary_map.get(m, "??") for m in step) for step in movements]

    table_data = [seq_header, sensor_row, signal_row, binary_row]
    table = list(map(list, zip(*table_data)))
    st.table(table)

    # ==================== BLOQUES ====================
    st.markdown("### Bloques")

    for idx, step in enumerate(movements, 1):
        move_str = " + ".join(step) if len(step) > 1 else step[0]
        
        st.markdown(f"**Bloque {idx}**")
        
        # Línea superior
        prev_k = f"K{idx-1}" if idx > 1 else "B0"
        st.text(f"Inicio     {prev_k}     K{idx}     K{idx if idx==1 else idx-1}")
        
        # Línea inferior
        signals = " ".join(signal_map.get(m, "??") for m in step)
        st.text(f"K{idx}                          {signals}")
        
        st.text("─" * 50)  # separador

    st.caption("Formato aproximado a tus tablas originales")
