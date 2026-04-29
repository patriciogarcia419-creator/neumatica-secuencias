import streamlit as st

st.set_page_config(page_title="Secuencias Neumática", layout="wide")
st.title("🛠 Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Pega tu secuencia (ejemplo: (A+B+)B-A- )")

secuencia_input = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="hidden")

if st.button("🚀 Generar Tabla", type="primary"):
    seq = secuencia_input.strip().upper().replace(" ", "")
    
    # Parseo de la secuencia
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

    # === Tabla Principal ===
    st.markdown("### Tabla Principal")

    seq_header = ["Secuencia"] + [f"({'+'.join(m)})" if len(m) > 1 else m[0] for m in movements]
    sensor_row = ["sensor"] + [f"K{i+1}" for i in range(len(movements))]
    
    signal_row = ["señales"]
    binary_row = ["Sec. bin"]

    signal_map = {'A+': 'Y1', 'A-': 'Y2', 'B+': 'Y3', 'B-': 'Y4', 
                  'C+': 'Y5', 'C-': 'Y6'}

    binary_map = {'A+': 'A1', 'A-': 'A0', 'B+': 'B1', 'B-': 'B0', 
                  'C+': 'C1', 'C-': 'C0'}

    signals_list = []
    binary_list = []

    for step in movements:
        step_signals = [signal_map.get(move, "Y?") for move in step]
        step_binary  = [binary_map.get(move, "?") for move in step]
        
        signals_list.append(" ".join(step_signals))
        binary_list.append(" ".join(step_binary))

    signal_row += signals_list
    binary_row += binary_list

    # Crear y mostrar tabla
    table_data = [seq_header, sensor_row, signal_row, binary_row]
    table_transposed = list(map(list, zip(*table_data)))
    st.table(table_transposed)

    # === Bloques ===
    st.markdown("### Bloques")

    for idx, step in enumerate(movements, 1):
        move_str = " + ".join(step) if len(step) > 1 else step[0]
        with st.expander(f"**Bloque {idx}** ─ {move_str}", expanded=True):
            st.markdown(f"**Movimiento:** `{move_str}`")
            st.markdown(f"**Sensor:** `K{idx}`")
            st.markdown(f"**Señales:** `{signals_list[idx-1]}`")
            st.markdown(f"**Binario:** `{binary_list[idx-1]}`")

    st.success("¡Tabla generada correctamente!")
    st.caption("Formato ajustado a tu convención fija de Y y estados binarios")
