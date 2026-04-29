import streamlit as st

st.set_page_config(page_title="Secuencias Neumática", layout="wide")
st.title("🛠 Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Pega tu secuencia exactamente como antes (ej: (A+B+C+)A-B-C-)")

secuencia_input = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="hidden")

if st.button("🚀 Generar Tabla", type="primary"):
    seq = secuencia_input.strip().upper().replace(" ", "")
    
    # Parseo mejorado
    movements = []
    i = 0
    while i < len(seq):
        if seq[i] == '(':
            j = seq.find(')', i)
            group = seq[i+1:j]
            parallel = []
            k = 0
            while k < len(group):
                cyl = group[k]
                if k+1 < len(group) and group[k+1] in '+-':
                    parallel.append(cyl + group[k+1])
                    k += 2
                else:
                    k += 1
            if parallel:
                movements.append(parallel)
            i = j + 1
        else:
            cyl = seq[i]
            if i+1 < len(seq) and seq[i+1] in '+-':
                movements.append([cyl + seq[i+1]])
                i += 2
            else:
                i += 1

    st.subheader(f"Secuencia: **{seq}**")

    # === Tabla Principal ===
    st.markdown("### Tabla Principal")

    # Encabezado de secuencia
    seq_header = ["Secuencia"] + [f"({'+'.join(m)})" if len(m)>1 else m[0] for m in movements]
    
    sensor_row = ["sensor"] + [f"K{i+1}" for i in range(len(movements))]
    signal_row = ["señales"]
    binary_row = ["Sec. bin"]

    y_counter = 1
    signals_list = []
    binary_list = []

    for step in movements:
        step_signals = []
        step_binary = []
        for move in step:
            cyl = move[0]
            dir = move[1]
            step_binary.append(f"{cyl}{dir}")
            step_signals.append(f"Y{y_counter}")
            y_counter += 1
        signals_list.append(" ".join(step_signals))
        binary_list.append(" ".join(step_binary))
    
    signal_row += signals_list
    binary_row += binary_list

    # Crear tabla
    table_data = [seq_header, sensor_row, signal_row, binary_row]
    table_transposed = list(map(list, zip(*table_data)))
    
    st.table(table_transposed)

    # === Bloques ===
    st.markdown("### Bloques")

    for idx, step in enumerate(movements, 1):
        move_str = " + ".join(step) if len(step) > 1 else step[0]
        with st.expander(f"**Bloque {idx}** ─ {move_str}", expanded=True):
            st.markdown(f"**Movimiento:** `{move_str}`")
            st.markdown(f"**Sensor que habilita este bloque:** `K{idx}`")
            st.markdown(f"**Señales que se activan:** `{signals_list[idx-1]}`")
            st.markdown(f"**Estado binario:** `{binary_list[idx-1]}`")

    st.success("¡Tabla generada!")
    st.caption("Formato ajustado a tus ejemplos anteriores")
