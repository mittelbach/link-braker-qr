import streamlit as st
import cv2
import numpy as np
from PIL import Image
import sqlite3
import datetime

# 1. IDENTIDAD S&M LABS
st.set_page_config(
    page_title="LINK-BREAKER UNIVERSAL", page_icon="🔓", layout="centered"
)


# --- EL ESPÍA SOBERANO (Base de Datos interna) ---
def registrar_uso(tipo_escaneo, resultado):
    try:
        conn = sqlite3.connect("breaker_stats.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS uso (fecha TEXT, tipo TEXT, exito TEXT)"""
        )
        ahora = datetime.datetime.now().strftime("%d/%m %H:%M")
        c.execute("INSERT INTO uso VALUES (?, ?, ?)", (ahora, tipo_escaneo, resultado))
        conn.commit()
        conn.close()
    except:
        pass


# Estilo visual Cyberpunk
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00ffcc; font-family: 'Courier New', monospace; text-align: center; }
    h3 { color: #ffffff; text-align: center; font-weight: 300; }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
    .stButton>button { background-color: #00ffcc; color: black; font-weight: bold; border-radius: 10px; border: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔓 LINK-BREAKER QR")
st.markdown("### El fin del 'Tercero'. Rompé el bloqueo de links.")
st.write("---")

# 2. INTERFAZ DE NAVEGACIÓN
tab1, tab2 = st.tabs(["🌐 ESCÁNER QR (Web/Links)", "📦 CÓDIGO DE BARRAS (Facturas)"])

# --- TAB 1: MUNDO QR (OpenCV) ---
with tab1:
    st.info("🎯 **OBJETIVO:** Extraer links de Instagram, Facebook o anuncios.")
    archivo_qr = st.file_uploader(
        "Subí tu captura con QR", type=["png", "jpg", "jpeg"], key="qr_up"
    )

    if archivo_qr:
        with st.spinner("⚡ Analizando señal..."):
            img_pil = Image.open(archivo_qr)
            img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            detector = cv2.QRCodeDetector()
            url, _, _ = detector.detectAndDecode(img_cv)

            if url:
                registrar_uso("QR", "ÉXITO")
                st.balloons()
                st.success("✅ ¡ENLACE DETECTADO!")
                st.code(url)
                st.link_button(
                    "🚀 ABRIR ENLACE SOBERANO", url, use_container_width=True
                )
            else:
                st.error("No se detectó un QR. Intentá con una captura más nítida.")

# --- TAB 2: MUNDO BARRAS (PyZBar Industrial) ---
with tab2:
    st.info("📑 **OBJETIVO:** Extraer números de facturas (Luz, Gas, Claro, etc.)")
    archivo_barras = st.file_uploader(
        "Subí foto del Código de Barras", type=["png", "jpg", "jpeg"], key="bar_up"
    )

    if archivo_barras:
        with st.spinner("⚡ Escaneando factura..."):
            try:
                from pyzbar.pyzbar import decode

                # Procesamiento de imagen para máximo contraste
                img_pil_b = Image.open(archivo_barras)
                img_cv = cv2.cvtColor(np.array(img_pil_b), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

                # Aumentamos tamaño y aplicamos nitidez (Caza-Claro)
                alto, ancho = gray.shape
                gray = cv2.resize(
                    gray, (ancho * 2, alto * 2), interpolation=cv2.INTER_LANCZOS4
                )
                kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                gray = cv2.filter2D(gray, -1, kernel)

                # Filtro de limpieza (Binarización)
                _, final_img = cv2.threshold(
                    gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )

                # Motor Industrial de escaneo
                resultados = decode(final_img)

                if resultados:
                    registrar_uso("BARRAS", "ÉXITO")
                    st.balloons()
                    for obj in resultados:
                        dato = obj.data.decode("utf-8")
                        st.success(f"✅ CÓDIGO {obj.type} DETECTADO")
                        st.code(dato)
                        st.info(
                            "💡 Copiá este número para pagar en tu Home Banking o hacer lo que necesites."
                        )
                else:
                    st.error(
                        "No se detectó el código. Asegurate de que la captura sea nítida y muestre todo el código de barras."
                    )

            except ImportError:
                st.warning(
                    "Motor industrial no disponible. Verificá el archivo requirements.txt en GitHub."
                )

# 3. PANEL SECRETO S&M LABS
st.write("")
with st.expander("🔐 Panel de Auditoría"):
    clave = st.text_input("Clave de acceso", type="password")
    if clave == "laprida2024":
        try:
            import pandas as pd

            conn = sqlite3.connect("breaker_stats.db")
            df = pd.read_sql("SELECT * FROM uso ORDER BY rowid DESC", conn)
            st.write("### 📝 Historial de uso:")
            st.dataframe(df, use_container_width=True)
            conn.close()
        except:
            st.write("Aún no hay registros de uso.")

st.write("---")
st.caption("S&M Labs | Proyecto LINK-BREAKER | v1.1 Industrial")
