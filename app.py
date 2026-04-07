import streamlit as st
import pandas as pd

# 1. Configuración de la aplicación
st.set_page_config(page_title="ZEEUS - Startup Tool", layout="wide")

st.title("🌱 ZEEUS: Evaluación de Sostenibilidad")
st.markdown("---")

# 2. Entradas Iniciales (Basics - Manual Sección 3.0)
st.sidebar.header("📋 Datos de la Startup")

nombre = st.sidebar.text_input("Nombre de la Startup", placeholder="Ej. GreenTech")
pais = st.sidebar.selectbox("País (ISO)", ["España", "México", "Colombia", "Otro"])

# Categorías NACE (Simplificadas del manual 01-99)
nace = st.sidebar.selectbox("Categoría de Negocio (NACE)", [
    "01 - Agricultura y Ganadería",
    "10 - Fabricación de Alimentos",
    "35 - Suministro de Energía",
    "62 - Programación y Consultoría IT",
    "99 - Otras actividades"
])

oferta = st.sidebar.radio("Tipo de oferta", ["Producto", "Servicio"])
lanzado = st.sidebar.checkbox("¿Ya ha sido lanzado al mercado?")

# Etapas oficiales (User Manual 3.0)
etapa = st.sidebar.select_slider(
    "Etapa Actual",
    options=["Ideation", "Validation", "Prototype", "Pre-Launch", "Launch", "Post Launch"]
)
# 3. Etapa I: Holistic Assessment (Inside-Out)
if nombre:
    st.header(f"Evaluación para {nombre}")
    st.write(f"**Sector:** {nace} | **Etapa:** {etapa}")
    
    st.subheader("📝 Evaluación de Impacto Ambiental y Social")
    st.info("Utiliza los sliders para calificar el impacto siguiendo el manual (0-4).")

    # Creamos dos columnas para organizar la evaluación
    col_input, col_result = st.columns([2, 1])

    with col_input:
        # Factores de cálculo según Manual ZEEUS
        st.write("### Criterios de Impacto")
        magnitud = st.slider("Magnitud (Gravedad del impacto)", 0.0, 4.0, 1.0, help="0: N/A, 4: Muy grave")
        escala = st.slider("Escala (Alcance geográfico/poblacional)", 0.0, 4.0, 1.0)
        irreversibilidad = st.slider("Irreversibilidad (Dificultad de reparación)", 0.0, 4.0, 1.0)
        probabilidad = st.slider("Probabilidad de ocurrencia", 0.0, 4.0, 1.0)

    # 4. Motor de Cálculo y Lógica de Interpretación (Score Interpretation_ZEEUS.pdf)
    # Fórmula: Promedio de (M+E+I) multiplicado por Probabilidad (normalizado)
    impacto_base = (magnitud + escala + irreversibilidad) / 3
    # Escalamiento sugerido por el FAQ 12: Probabilidad actúa como multiplicador
    puntaje_final = round(impacto_base * (probabilidad / 4) * 4, 2) 

    with col_result:
        st.write("### Resultado Etapa I")
        st.metric(label="Puntaje de Materialidad", value=puntaje_final)

        # Lógica de colores según el archivo "Score Interpretation"
        if puntaje_final >= 2.5:
            st.error("🔴 **ALTA PRIORIDAD**\n\nRelevancia alta: Toma acciones estratégicas.")
        elif puntaje_final >= 2.0:
            st.warning("🟡 **RELEVANTE**\n\nTema material: Revisa las recomendaciones.")
        elif puntaje_final >= 1.0:
            st.info("🔵 **BAJO**\n\nRelevancia menor: Monitorea y reevalúa luego.")
        else:
            st.success("🟢 **MUY BAJO / N/A**\n\nNo se requiere acción inmediata.")

else:
    st.warning("👈 Por favor, ingresa el nombre de la startup en la barra lateral.")
    