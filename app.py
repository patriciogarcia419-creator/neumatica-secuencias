import streamlit as st

st.set_page_config(page_title="Secuencias Neumática", layout="wide")
st.title("🛠 Generador de Tablas Neumática / Electro-Neumática")
st.markdown("Pega tu secuencia y presiona el botón")

secuencia_input = st.text_input("Secuencia:", value="A+B+C+A-B-C-", label_visibility="hidden")

if st.button("🚀 Generar Tabla", type="primary"):
    secuencia = secuencia_input.strip().lower()
    st.subheader(f"Secuencia procesada: **{secuencia.upper()}**")
    st.info("Aquí aparecerá la tabla completa cuando implementemos la lógica completa.")
    st.write("Por ahora solo muestra la secuencia ingresada.")
    
    # Placeholder para la tabla
    st.markdown("### Tabla principal (próximamente)")
    st.markdown("### Bloques (próximamente)")

st.caption("App hecha para clase de Automatización Industrial")
