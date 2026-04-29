import streamlit as st

st.set_page_config(page_title="Secuencias Neumática", layout="wide")
st.title("🛠 Generador de Tablas Neumática")
st.markdown("Pega tu secuencia y genera la tabla")

secuencia_input = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="hidden")

if st.button("🚀 Generar Tabla", type="primary"):
    seq = secuencia_input.strip().upper().replace(" ", "")
    
    # Parseo
    movements = []
    i = 0
    while i < len(seq):
        if seq[i] == '(':
            j = seq.find(')', i)
            group = seq[i+1:j]
            parallel = []
            k = 0
            while k < len(group):
                if k+1 < len(group) and group[k+1] in '+-':
                    parallel.append(group[k] + group[k+1])
                    k += 2
                else:
                    k += 1
            if parallel:
                movements.append(parallel)
            i = j + 1
        else:
            if i+1 < len(seq) and seq[i+1] in '+-':
                movements.append([seq[i] + seq[i+1]])
                i += 2
            else:
                i += 1

    st.subheader(f"Secuencia: **{seq}**")

    # ==================== TABLA PRINCIPAL ====================
    st.markdown("### Tabla Principal")

    seq_header = ["Secuencia"] + [f"({'+'.join(m)})" if len(m)>1 else m[0] for m in movements]
    sensor_row = ["sensor"]    + [f"K{i+1}" for i in range(len(movements))]
    
    signal_map = {'A+':'Y1','A-':'Y2','B+':'Y3','B-':'Y4','C+':'Y5','C-':'Y6'}
    binary_map = {'A+':'A1','A-':'A0','B+':'B1','B-':'B0','C+':'C1','C-':'C0'}

    signal_row = ["señales"] + [" ".join(signal_map.get(move, "??") for move in step) for step in movements]
    binary_row = ["Sec. bin"] + [" ".join(binary_map.get(move, "??") for move in step) for step in movements]

    table_data = [seq_header, sensor_row, signal_row, binary_row]
    table_transposed = list(map(list, zip(*table_data)))

    st.table(table_transposed)

    # ==================== BLOQUES ====================
    st.markdown("### Bloques")

    for idx, step in enumerate(movements, 1):
        move_str = " + ".join(step) if len(step) > 1 else step[0]
        
        st.markdown(f"**Bloque {idx}**")
        st.text(f"Inicio     B0     K{idx}     K{idx if idx==1 else idx-1 if idx>1 else 1}")
        st.text(f"K{idx}                       Y{','.join([str(list(signal_map.values()).index(signal_map[m])+1) for m in step])}".replace("Y0","??"))
        st.text(" " * 30)   # separador visual

    st.success("Tabla generada")
