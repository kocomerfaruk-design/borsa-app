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
            guncel_fiyat = hist['Close'].iloc[-1]
        else:
            guncel_fiyat = hisse["Maliyet"]
        
        maliyet_tutar = hisse["Maliyet"] * hisse["Adet"]
        guncel_tutar = guncel_fiyat * hisse["Adet"]
        kar_tl = guncel_tutar - maliyet_tutar
        kar_yuzde = ((guncel_fiyat - hisse["Maliyet"]) / hisse["Maliyet"] * 100) if hisse["Maliyet"] > 0 else 0
        
        toplam_maliyet += maliyet_tutar
        toplam_deger += guncel_tutar
        
        tablo_verisi.append({
            "Hisse": hisse["Sembol"],
            "Adet": hisse["Adet"],
            "Ort. Maliyet": f"{hisse['Maliyet']:.2f}",
            "Anlık Fiyat": f"{guncel_fiyat:.2f}",
            "Piyasa Değeri": round(guncel_tutar, 2),
            "Kâr/Zarar (TL)": round(kar_tl, 2),
            "Getiri %": round(kar_yuzde, 2)
        })
    except:
        pass
    bar.progress((i + 1) / len(hisseler))

bar.empty()

# --- ÖZET KARTLAR ---
genel_kar = toplam_deger - toplam_maliyet
genel_yuzde = (genel_kar / toplam_maliyet * 100) if toplam_maliyet > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Toplam Yatırım", f"{toplam_maliyet:,.2f} TL")
col2.metric("Güncel Değer", f"{toplam_deger:,.2f} TL", delta=f"{genel_kar:,.2f} TL")
col3.metric("Genel Getiri", f"%{genel_yuzde:.2f}", delta=f"%{genel_yuzde:.2f}")

st.markdown("---")

# --- DETAYLI TABLO ---
if tablo_verisi:
    df = pd.DataFrame(tablo_verisi)
    # En çok kazandıran en üstte olsun
    df = df.sort_values("Getiri %", ascending=False)
    
    st.subheader("📋 Hisse Senedi Detayları")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("Veri bulunamadı.")