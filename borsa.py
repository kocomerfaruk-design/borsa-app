import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Portföy Yönetimi", page_icon="💼", layout="wide")

# --- VARSAYILAN PORTFÖYLER ---
def varsayilan_yukle():
    return {
        "Alfa Portföyü (Yüksek Risk)": [
            {"Sembol": "INVEO.IS", "Maliyet": 8.78, "Adet": 1139},
            {"Sembol": "SANEL.IS", "Maliyet": 32.00, "Adet": 312},
            {"Sembol": "KRSTL.IS", "Maliyet": 11.47, "Adet": 871},
            {"Sembol": "ISGSY.IS", "Maliyet": 73.40, "Adet": 136},
            {"Sembol": "MACKO.IS", "Maliyet": 25.78, "Adet": 388}
        ],
        "Beta Portföyü (Orta Risk)": [
            {"Sembol": "NTGAZ.IS", "Maliyet": 11.49, "Adet": 870},
            {"Sembol": "TKNSA.IS", "Maliyet": 25.48, "Adet": 392},
            {"Sembol": "ATATP.IS", "Maliyet": 156.60, "Adet": 63},
            {"Sembol": "BIZIM.IS", "Maliyet": 32.18, "Adet": 310},
            {"Sembol": "ALVES.IS", "Maliyet": 4.22, "Adet": 2369}
        ],
        "Delta Portföyü (BIST100)": [
            {"Sembol": "EKGYO.IS", "Maliyet": 25.50, "Adet": 392},
            {"Sembol": "IZENR.IS", "Maliyet": 9.53, "Adet": 1049},
            {"Sembol": "GUBRF.IS", "Maliyet": 480.50, "Adet": 20},
            {"Sembol": "KTLEV.IS", "Maliyet": 38.20, "Adet": 261}
        ]
    }

# --- HAFIZA YÖNETİMİ (Session State) ---
if 'portfoyler' not in st.session_state:
    st.session_state['portfoyler'] = varsayilan_yukle()

portfoyler = st.session_state['portfoyler']

# --- YAN MENÜ: YÖNETİM ---
st.sidebar.title("🛠️ Portföy Yönetimi")

# 1. Yeni Portföy Oluşturma
yeni_liste_adi = st.sidebar.text_input("Yeni Liste Adı", placeholder="Örn: Takip Listem")
if st.sidebar.button("Liste Oluştur"):
    if yeni_liste_adi and yeni_liste_adi not in portfoyler:
        portfoyler[yeni_liste_adi] = []
        st.rerun()

st.sidebar.markdown("---")

# 2. Portföy Seçimi
secenekler = list(portfoyler.keys())
secili_portfoy = st.sidebar.selectbox("Görüntülenecek Liste", secenekler)

st.sidebar.markdown("---")

# 3. Hisse Ekleme
st