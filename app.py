import streamlit as st

st.set_page_config(page_title="Neumática - Tablas de Secuencia", layout="wide")
st.title("Generador de Tablas Neumática / Electro-Neumática")

secuencia = st.text_input("Introduce la secuencia:", value="(A+B+)B-A-", label_visibility="visible")

if st.button("Generar Tabla", type="primary"):
    seq = secuencia.strip().upper().replace(" ", "")
    
    # ------------------------------------------------------------
    # 1. Parsear la secuencia (movimientos simples y en paralelo)
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # 2. Tabla Principal (con el formato correcto, sin dobles signos)
    # ------------------------------------------------------------
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")

    signal_map = {'A+':'Y1','A-':'Y2','B+':'Y3','B-':'Y4','C+':'Y5','C-':'Y6'}
    binary_map = {'A+':'A1','A-':'A0','B+':'B1','B-':'B0','C+':'C1','C-':'C0'}

    # Encabezado de secuencia: mostrar (A+ B+) en lugar de (A++B+)
    encabezado = ["Secuencia"]
    for s in steps:
        if len(s) == 1:
            encabezado.append(s[0])
        else:
            # Quitamos el signo de cada movimiento para mostrarlo limpio
            movs_limpios = [m[0] + m[1] for m in s]  # ya es A+, B+
            encabezado.append(f"({' '.join(movs_limpios)})")
    
    sensor_row = ["sensor"] + [f"K{i+1}" for i in range(len(steps))]
    signal_row = ["señales"] + [" ".join(signal_map[m] for m in s) for s in steps]
    binary_row = ["Sec. bin"] + [" ".join(binary_map[m] for m in s) for s in steps]

    table_data = [encabezado, sensor_row, signal_row, binary_row]
    st.table(list(map(list, zip(*table_data))))

    # ------------------------------------------------------------
    # 3. Bloques con la lógica correcta de condiciones
    # ------------------------------------------------------------
    st.markdown("### Bloques")

    n = len(steps)

    # Calcular el estado final después de cada paso
    # Guardamos el último estado de cada cilindro
    estado = {}
    for s in steps:
        for m in s:
            estado[m[0]] = m[1]   # '+' o '-'

    # El estado final del sistema (después del último paso)
    condiciones_iniciales = []
    # Cilindros que aparecen en la secuencia
    todos_cilindros = sorted(set(m[0] for s in steps for m in s))
    for c in todos_cilindros:
        if c in estado:
            condiciones_iniciales.append(f"{c}{estado[c]}")
        else:
            condiciones_iniciales.append(f"{c}0")  # por si acaso
    cond_inicial_str = " ".join(condiciones_iniciales)

    for idx, step in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        # ----- Primera línea del bloque -----
        if idx == 1:
            # La condición es el estado final del sistema (último paso)
            prev_cond = cond_inicial_str
            prev_sensor = "Inicio"
        else:
            # Condición: el estado binario del paso anterior (del step idx-2)
            prev_step = steps[idx-2]
            prev_cond_parts = [binary_map[m] for m in prev_step]
            prev_cond_parts.sort()
            prev_cond = " ".join(prev_cond_parts)
            prev_sensor = f"K{idx-1}"
        
        # Sensores destino y reset
        next_sensor = f"K{(idx % n) + 1}" if idx % n != 0 else "K1"
        reset_sensor = f"K{idx}"
        
        # Ajuste de espacios para que quede alineado como en tus ejemplos
        # Usamos un ancho fijo de 6 para cada campo, pero tú quieres exactamente el formato visual
        # Haré una línea con espacios manuales como en tu ejemplo:
        # "Inicio     B0     K2     K1"
        line1 = f"{prev_sensor}     {prev_cond}     {next_sensor}     {reset_sensor}"
        st.text(line1)
        
        # ----- Segunda línea del bloque -----
        signals = " ".join(signal_map[m] for m in step)
        line2 = f"K{idx}                          {signals}"
        st.text(line2)
        st.text("")  # línea vacía entre bloques

    st.caption("")  # sin mensajes extras
