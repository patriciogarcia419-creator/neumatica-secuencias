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
    
    signal_map = {'A+':'Y1','A-':'Y2','B+':'Y3','B-':'Y4','C+':'Y5','C-':'Y6',
                  'D+':'Y7','D-':'Y8','E+':'Y9','E-':'Y10','F+':'Y11','F-':'Y12'}
    
    binary_map = {'A+':'A1','A-':'A0','B+':'B1','B-':'B0','C+':'C1','C-':'C0',
                  'D+':'D1','D-':'D0','E+':'E1','E-':'E0','F+':'F1','F-':'F0'}
    
    n = len(steps)
    
    # Tabla Principal
    st.subheader(f"Secuencia: **{seq}**")
    st.markdown("### Tabla Principal")
    
    sec_row = [s[0] if len(s)==1 else f"({' '.join(s)})" for s in steps]
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
    
    # Bloques - Formato EXACTO que pediste
    st.markdown("### Bloques")
    
    for idx, s in enumerate(steps, start=1):
        st.markdown(f"**Bloque {idx}**")
        
        signals = " ".join(signal_map.get(m, "??") for m in s)
        
        if idx == 1:
            st.code("Inicio  B0      K2     K1", language="text")
            st.code(f"K1                      {signals}", language="text")
        else:
            prev_binary = " ".join(binary_map.get(m, "??") for m in steps[idx-2])
            st.code(f"K{idx-1}    {prev_binary}     K{idx}     K{idx-1}", language="text")
            st.code(f"K{idx}                      {signals}", language="text")
        
        st.markdown("")
