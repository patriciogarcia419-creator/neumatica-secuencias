import streamlit as st

st.set_page_config(page_title="Secuencias Neumática", layout="wide")
st.title("🛠 Generador de Tablas Neumática / Electro-Neumática")
st.markdown("**Pega tu secuencia y presiona Generar**")

secuencia_input = st.text_input(
    "Secuencia:", 
    value="A+A-(B+C+)A+A-(B-C-)",
    label_visibility="hidden"
)

if st.button("🚀 Generar Tabla", type="primary"):
    seq = secuencia_input.strip().lower().replace(" ", "")
    
    # Parsear la secuencia
    movements = []
    i = 0
    while i < len(seq):
        if seq[i] == '(':
            j = seq.find(')', i)
            if j == -1:
                j = len(seq)
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

    # Mostrar resultado
    st.subheader(f"Secuencia: **{secuencia_input.upper()}**")
    
    # Crear tabla principal
    st.markdown("### Tabla Principal")
    
    header = ["Secuencia"] + [m[0] if len(m)==1 else f"({'+'.join(m)})" for m in movements]
    
    col1 = ["sensor"]
    col2 = ["señales"]
    col3 = ["Sec. bin"]
    
    sensors = [f"K{i+1}" for i in range(len(movements))]
    signals = []
    binary = []
    
    cyl_state = {}
    signal_counter = 1
    sensor_counter = 1
    
    for step in movements:
        step_signals = []
        step_binary = []
        for move in step:
            cyl = move[0].upper()
            action = move[1]
            state = "1" if action == "+" else "0"
            step_binary.append(f"{cyl}{state}")
            
            if cyl not in cyl_state or cyl_state[cyl] != state:
                step_signals.append(f"Y{signal_counter}")
                signal_counter += 1
                cyl_state[cyl] = state
            else:
                step_signals.append(f"Y{signal_counter-1}")
        
        signals.append(" ".join(step_signals))
        binary.append(" ".join(step_binary))
        col1.append(f"K{sensor_counter}")
        sensor_counter += 1
    
    # Mostrar tabla principal
    data = [header, col1, col2 + signals, col3 + binary]
    transposed = list(map(list, zip(*data)))
    
    st.table(transposed)
    
    # Mostrar Bloques
    st.markdown("### Bloques")
    
    for idx, step in enumerate(movements, 1):
        parallel_str = " + ".join(step) if len(step) > 1 else step[0]
        with st.expander(f"**Bloque {idx}** - {parallel_str.upper()}", expanded=True):
            st.write(f"**Movimiento:** {parallel_str.upper()}")
            st.write(f"**Sensor activado:** K{idx}")
            st.write(f"**Señales activadas:** {signals[idx-1]}")
    
    st.success("¡Tabla generada correctamente!")
    st.caption("App para Automatización Industrial - Control Ladder")

st.caption("Desarrollado para ejercicios de Neumática y Electro-Neumática")
