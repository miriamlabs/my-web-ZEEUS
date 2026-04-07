import streamlit as st
import pandas as pd
from fpdf import FPDF
from deep_translator import GoogleTranslator
from streamlit_javascript import st_javascript
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA Y MARCA ---
st.set_page_config(
    page_title="ZEEUS - Zero Emissions Entrepreneurship",
    page_icon="🌱",
    layout="wide"
)

# --- 2. DETECCIÓN DE IDIOMA E IA DE TRADUCCIÓN ---
def get_browser_language():
    lang = st_javascript('window.navigator.language')
    if lang:
        lang_code = lang.split('-')[0]
        mapping = {"es": "Español", "en": "English", "fr": "Français", "de": "Deutsch"}
        return mapping.get(lang_code, "English")
    return "English"

@st.cache_data
def trad(texto, idioma_destino):
    if idioma_destino == "Español": return texto
    codigos = {"English": "en", "Français": "fr", "Deutsch": "de"}
    try:
        return GoogleTranslator(source='auto', target=codigos.get(idioma_destino, "en")).translate(texto)
    except:
        return texto

# --- 3. ESTILO VISUAL OFICIAL (Basado en GUIDELINES KIT) ---
# Colores: Verde Lima #B9E021, Verde Marca #39B54A, Verde Oscuro #00654A
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, #B9E021 0%, #8CC63F 45%, #39B54A 100%);
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
    }}
    h1, h2, h3, p, label, span {{
        color: #00654A !important;
        font-family: 'Helvetica', sans-serif;
    }}
    .stMetric {{
        background-color: rgba(255, 255, 255, 0.4);
        padding: 15px;
        border-radius: 15px;
    }}
    .stButton>button {{
        background-color: #00654A !important;
        color: white !important;
        border-radius: 25px;
        border: none;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. CEREBRO DE DATOS EUROPEOS (NACE -> ODS -> ESRS) ---
sectores_europa = {
    "C10 - Alimentación": {"nace": "10.00", "ods": [2, 12, 15], "esrs": "E4 Biodiversity"},
    "D35 - Energía": {"nace": "35.11", "ods": [7, 13], "esrs": "E1 Climate Change"},
    "J62 - Tecnología/IT": {"nace": "62.01", "ods": [4, 9], "esrs": "S1 Own Workforce"},
    "M70 - Consultoría": {"nace": "70.22", "ods": [8, 17], "esrs": "G1 Business Conduct"}
}

# --- 5. LÓGICA DE IDIOMA ---
if 'lang' not in st.session_state:
    st.session_state.lang = get_browser_language()

# --- 6. SIDEBAR (ENTRADAS 1 Y 2) ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 50px; margin-bottom: -20px;'>Z.</h1>", unsafe_allow_html=True)
    st.caption("Zero Emissions Entrepreneurship")
    
    idioma_sel = st.selectbox("🌐 Language", ["Español", "English", "Français", "Deutsch"], 
                              index=["Español", "English", "Français", "Deutsch"].index(st.session_state.lang))
    st.session_state.lang = idioma_sel
    L = st.session_state.lang

    st.header(trad("📋 Datos de la Startup", L))
    nombre = st.text_input(trad("Nombre de la Startup", L), "EcoTech Europe")
    sector_key = st.selectbox(trad("Sector NACE", L), list(sectores_europa.keys()))
    etapa = st.select_slider(trad("Etapa de Desarrollo", L), 
                             options=["Ideation", "Validation", "Prototype", "Pre-Launch", "Launch"])

# --- 7. CUERPO PRINCIPAL ---
if nombre:
    st.title(f"🌱 {trad('Evaluación de Sostenibilidad', L)}")
    st.subheader(f"{nombre} | {sector_key} | {etapa}")

    tab1, tab2, tab3 = st.tabs([trad("📝 Evaluación ESRS", L), trad("📊 Dashboard ODS", L), trad("📄 Exportar", L)])

    with tab1:
        st.header(trad("Doble Materialidad (Normativa EU)", L))
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 🌍 {trad('Impacto (Inside-Out)', L)}")
            m = st.slider(trad("Magnitud", L), 0.0, 4.0, 2.0)
            e = st.slider(trad("Escala", L), 0.0, 4.0, 2.0)
            i = st.slider(trad("Irreversibilidad", L), 0.0, 4.0, 2.0)
            p = st.slider(trad("Probabilidad", L), 0.0, 4.0, 2.0)
            
        with col2:
            st.markdown(f"### 📈 {trad('Riesgo Financiero (Outside-In)', L)}")
            r_reg = st.slider(trad("Riesgo Regulatorio (Leyes EU)", L), 0.0, 4.0, 1.5)
            r_mkt = st.slider(trad("Riesgo de Mercado", L), 0.0, 4.0, 1.0)
            
        # Cálculos ZEEUS
        score_impacto = round(((m + e + i) / 3) * (p / 4) * 4, 2)
        score_financiero = round((r_reg + r_mkt) / 2, 2)

        st.markdown("---")
        c_res1, c_res2 = st.columns(2)
        c_res1.metric(trad("Materialidad de Impacto", L), f"{score_impacto}/4")
        c_res2.metric(trad("Materialidad Financiera", L), f"{score_financiero}/4")

    with tab2:
        st.header(trad("Alineación con Objetivos de Desarrollo Sostenible", L))
        info = sectores_europa[sector_key]
        
        st.write(f"**{trad('Norma Europea Aplicable', L)}:** {info['esrs']}")
        
        # Mostrar ODS como tarjetas
        ods_cols = st.columns(len(info['ods']))
        for idx, ods_num in enumerate(info['ods']):
            ods_cols[idx].success(f"🎯 ODS {ods_num}")
            
        # Gráfico de barras pro
        st.markdown("### " + trad("Resumen de Riesgos y Oportunidades", L))
        chart_data = pd.DataFrame({
            trad("Categoría", L): [trad("Ambiental", L), trad("Social", L), trad("Gobernanza", L), trad("Financiero", L)],
            "Score": [score_impacto, 1.8, 2.2, score_financiero]
        })
        st.bar_chart(chart_data, x=trad("Categoría", L), y="Score", color="#00654A")

    with tab3:
        st.header(trad("Generar Informe Oficial", L))
        st.info(trad("Este informe incluye el co-branding oficial de la Unión Europea.", L))
        
        if st.button(trad("Descargar Reporte PDF", L)):
            # Lógica simple de PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="ZEEUS SUSTAINABILITY REPORT", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Startup: {nombre}", ln=True)
            pdf.cell(200, 10, txt=f"NACE: {info['nace']}", ln=True)
            pdf.cell(200, 10, txt=f"Impact Score: {score_impacto}/4", ln=True)
            pdf.ln(20)
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(200, 10, txt="Funded by the European Union", ln=True, align='C')
            
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(label="📥 Click para bajar PDF", data=pdf_output, 
                               file_name=f"ZEEUS_{nombre}.pdf", mime="application/pdf")

else:
    st.warning("👈 " + trad("Por favor, introduce el nombre de tu startup para comenzar.", L))

# --- 8. PIE DE PÁGINA (CO-BRANDING) ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #00654A; font-size: 12px;">
        Supported by Climate KIC | Funded by the European Union | EIT Higher Education Initiative
    </div>
    """, unsafe_allow_html=True)

