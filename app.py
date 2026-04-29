import streamlit as st

st.set_page_config(page_title="Neumática - Tablas de Secuencia", layout="wide")
st.title("🛠 Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Introduce la secuencia (ej: `(A+B+)B-A-` o `A+B+C+A-B-C-`)")

secuencia = st.text_input("Secuencia:", value="(A+B+)B-A-", label_visibility="hidden")

if st.button("🚀 Generar Tabla", type="primary"):
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

    # ---------- 2. Tabla Principal ----------
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")

    # Mapeos fijos
    signal_map = {'A+':'Y1','A-':'Y2','B+':'Y3','B-':'Y4','C+':'Y5','C-':'Y6'}
    binary_map = {'A+':'A1','A-':'A0','B+':'B1','B-':'B0','C+':'C1','C-':'C0'}

    # Encabezados
    sec_header = ["Secuencia"] + [f"({'+'.join(s)})" if len(s)>1 else s[0] for s in steps]
    sensor_row = ["sensor"] + [f"K{i+1}" for i in range(len(steps))]
    signal_row = ["señales"] + [" ".join(signal_map[m] for m in s) for s in steps]
    binary_row = ["Sec. bin"] + [" ".join(binary_map[m] for m in s) for s in steps]

    # Mostrar tabla
    table_data = [sec_header, sensor_row, signal_row, binary_row]
    st.table(list(map(list, zip(*table_data))))

    # ---------- 3. Bloques (con el formato exacto que pediste) ----------
    st.markdown("### Bloques")

    n = len(steps)
    # Obtener todos los cilindros presentes
    cylinders = sorted(set(m[0] for s in steps for m in s))
    first_cyl = cylinders[0] if cylinders else 'A'

    # Construir cada bloque
    for idx, step in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        # --- Primera línea del bloque ---
        if idx == 1:
            # Condición inicial: todos los cilindros excepto el primero, con estado 0
            cond_parts = [f"{c}0" for c in cylinders if c != first_cyl]
            cond_str = " ".join(cond_parts)
            prev_sensor = "Inicio"
        else:
            # Condición: estado resultante del paso anterior (step idx-2)
            prev_step = steps[idx-2]
            cond_parts = [binary_map[m] for m in prev_step]  # ej: A1, B1
            # Ordenar alfabéticamente para consistencia
            cond_parts.sort()
            cond_str = " ".join(cond_parts)
            prev_sensor = f"K{idx-1}"
        
        # Números de sensores
        next_sensor = f"K{(idx % n) + 1}" if idx % n != 0 else "K1"
        reset_sensor = f"K{idx}"
        
        # Construir primera línea con los espacios adecuados
        line1 = f"{prev_sensor}     {cond_str}     {next_sensor}     {reset_sensor}"
        st.text(line1)

        # --- Segunda línea del bloque ---
        signals = " ".join(signal_map[m] for m in step)
        line2 = f"K{idx}                          {signals}"
        st.text(line2)
        st.text("")  # línea en blanco separadora

    st.caption("")  # sin mensaje extra
