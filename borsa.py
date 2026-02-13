import streamlit as st
import yfinance as yf
import pandas as pd

# --- AYARLAR ---
st.set_page_config(page_title="Portföy Analizi", page_icon="💼", layout="wide")

# --- PORTFÖY VERİLERİ (SABİT) ---
# Web sitesinde veritabanı olmadığı için verileri buraya gömüyoruz.
# Arkadaşların girdiği an bu listeleri görecekler.

def portfoyleri_getir():
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

# Uygulama hafızasını başlat
if 'portfoyler' not in st.session_state:
    st.session_state['portfoyler'] = portfoyleri_getir()

portfoyler = st.session_state['portfoyler']

# --- YAN MENÜ ---
st.sidebar.title("🗂️ Portföy Seçimi")
secenekler = list(portfoyler.keys())
# Beta varsayılan olsun
index_secim = 0
if "Beta Portföyü (Orta Risk)" in secenekler: index_secim = secenekler.index("Beta Portföyü (Orta Risk)")

secili_portfoy = st.sidebar.selectbox("Görüntülenecek Liste", secenekler, index=index_secim)

st.sidebar.markdown("---")
st.sidebar.info("💡 Bu uygulama anlık BIST verilerini kullanarak portföy durumunu analiz eder.")

# --- ANA EKRAN ---
st.title(f"📊 {secili_portfoy}")

hisseler = portfoyler[secili_portfoy]

if st.button("🔄 Verileri Güncelle"):
    st.rerun()

# --- HESAPLAMALAR ---
tablo_verisi = []
toplam_maliyet = 0
toplam_deger = 0

# İlerleme Çubuğu (Kullanıcı beklerken sıkılmasın)
bar = st.progress(0)

for i, hisse in enumerate(hisseler):
    try:
        # Sadece anlık fiyatı çekiyoruz (Grafik verisi yok, bu yüzden çok hızlı)
        ticker = yf.Ticker(hisse["Sembol"])
        hist = ticker.history(period="1d")
        
        if not hist.empty:
            guncel_fiyat = hist