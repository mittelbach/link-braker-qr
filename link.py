import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 1. CONFIGURACIÓN DE IDENTIDAD S&M LABS
st.set_page_config(
    page_title="LINK-BREAKER UNIVERSAL", page_icon="🔓", layout="centered"
)

# Estilo visual de alta gama (Modo Tech)
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00ffcc; font-family: 'Courier New', monospace; text-align: center; text-shadow: 2px 2px #000; }
    h3 { color: #ffffff; text-align: center; font-weight: 300; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 10px 10px 0 0; 
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { border-top: 2px solid #00ffcc !important; color: #00ffcc !important; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; border-radius: 10px; border: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔓 LINK-BREAKER QR")
st.markdown("### Soberanía Digital: Se acabó el 'Tercero'")
st.write("---")

# 2. SEPARACIÓN DE TANTOS (Pestañas)
tab1, tab2 = st.tabs(
    ["🌐 ESCÁNER QR (Web/Links)", "📦 CÓDIGO DE BARRAS (Facturas/Productos)"]
)

# --- PESTAÑA 1: MUNDO QR ---
with tab1:
    st.info(
        "🎯 **OBJETIVO:** Romper el bloqueo de links en Instagram, Facebook o publicidades digitales."
    )
    archivo_qr = st.file_uploader(
        "Subí tu captura de pantalla con QR",
        type=["png", "jpg", "jpeg"],
        key="uploader_qr",
    )

    if archivo_qr:
        with st.spinner("⚡ Decodificando señal..."):
            img_pil = Image.open(archivo_qr)
            img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

            # Motor de detección QR (OpenCV)
            detector = cv2.QRCodeDetector()
            url, puntos, _ = detector.detectAndDecode(img_cv)

            if url:
                st.balloons()
                st.success("✅ ¡ENLACE DETECTADO CON ÉXITO!")
                st.code(url, language="text")
                st.link_button(
                    "🚀 ABRIR ENLACE SOBERANO", url, use_container_width=True
                )
            else:
                # Plan B: Optimización por si la captura es mala
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
                url_b, _, _ = detector.detectAndDecode(thresh)
                if url_b:
                    st.success("✅ ¡ENLACE DETECTADO (Modo Optimizado)!")
                    st.link_button(
                        "🚀 ABRIR ENLACE SOBERANO", url_b, use_container_width=True
                    )
                else:
                    st.error(
                        "❌ No se encontró un QR legible. Intentá con otra captura."
                    )

# --- PESTAÑA 2: MUNDO BARRAS ---
with tab2:
    st.info(
        "📑 **OBJETIVO:** Extraer números de facturas de luz, gas o códigos de productos de supermercado."
    )
    archivo_barras = st.file_uploader(
        "Subí la foto del Código de Barras",
        type=["png", "jpg", "jpeg"],
        key="uploader_barras",
    )

    if archivo_barras:
        st.warning("⚠️ El motor de barras requiere la librería 'pyzbar'.")
        # Aquí intentamos usar pyzbar si está instalado
        try:
            from pyzbar.pyzbar import decode

            img_pil_b = Image.open(archivo_barras)
            resultados = decode(img_pil_b)

            if resultados:
                for obj in resultados:
                    dato = obj.data.decode("utf-8")
                    tipo = obj.type
                    st.success(f"✅ CÓDIGO {tipo} DETECTADO")
                    st.markdown(f"**Resultado:** `{dato}`")
                    if st.button("Copiar Código"):
                        st.write("Copiado al portapapeles (Simulado)")
            else:
                st.error("No se detectaron códigos de barras en esta imagen.")
        except ImportError:
            st.error(
                "El motor de barras no está configurado en este entorno. (Falta pyzbar)"
            )

st.write("---")
st.caption("S&M Labs | Proyecto LINK-BREAKER | Laprida 2024")
