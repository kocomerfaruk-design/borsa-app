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
st.sidebar.header(f"➕ {secili_portfoy} Ekle")
with st.sidebar.form("hisse_ekle_form"):
    s_sembol = st.text_input("Sembol (Örn: THYAO.IS)").upper()
    s_maliyet = st.number_input("Maliyet", min_value=0.0, format="%.2f")
    s_adet = st.number_input("Adet", min_value=1, step=1)
    if st.form_submit_button("Hisse Ekle"):
        if s_sembol:
            portfoyler[secili_portfoy].append({
                "Sembol": s_sembol,
                "Maliyet": s_maliyet,
                "Adet": s_adet
            })
            st.rerun()

# --- ANA EKRAN ---
st.title(f"📊 {secili_portfoy} Analizi")

hisseler = portfoyler[secili_portfoy]

if not hisseler:
    st.info("Bu portföy şu an boş. Yan menüden hisse ekleyebilirsin. 👈")
else:
    if st.button("🔄 Verileri Güncelle"):
        st.rerun()

    tablo_verisi = []
    t_maliyet, t_deger = 0, 0
    
    bar = st.progress(0)
    for i, hisse in enumerate(hisseler):
        try:
            ticker = yf.Ticker(hisse["Sembol"])
            # Günlük performansı ölçmek için son 2 günün verisi çekilir
            hist = ticker.history(period="2d")
            
            # Günlük Fiyat ve Yüzde Değişim Hesaplama
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                g_fiyat = hist['Close'].iloc[-1]
                gunluk_degisim = ((g_fiyat - prev_close) / prev_close) * 100
            else:
                g_fiyat = hist['Close'].iloc[-1] if not hist.empty else hisse["Maliyet"]
                gunluk_degisim = 0.0

            # Ok İkonları
            if gunluk_degisim > 0:
                gunluk_ok = f"🟢 +%{gunluk_degisim:.2f} 🔼"
            elif gunluk_degisim < 0:
                gunluk_ok = f"🔴 %{gunluk_degisim:.2f} 🔽"
            else:
                gunluk_ok = f"⚪ %0.00 ➖"
            
            m_tutar = hisse["Maliyet"] * hisse["Adet"]
            g_tutar = g_fiyat * hisse["Adet"]
            t_maliyet += m_tutar
            t_deger += g_tutar
            
            toplam_kar_yuzdesi = ((g_fiyat - hisse["Maliyet"]) / hisse["Maliyet"] * 100) if hisse["Maliyet"] > 0 else 0
            
            tablo_verisi.append({
                "Hisse": hisse["Sembol"],
                "Adet": hisse["Adet"],
                "Maliyet": f"{hisse['Maliyet']:.2f}",
                "Fiyat": f"{g_fiyat:.2f}",
                "Günlük %": gunluk_ok,
                "Değer": round(g_tutar, 2),
                "Genel Kâr %": round(toplam_kar_yuzdesi, 2)
            })
        except:
            pass
        bar.progress((i + 1) / len(hisseler))
    bar.empty()

    # Özet Kartlar
    g_kar = t_deger - t_maliyet
    g_yuzde = (g_kar / t_maliyet * 100) if t_maliyet > 0 else 0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Yatırım", f"{t_maliyet:,.0f} TL")
    c2.metric("Güncel Değer", f"{t_deger:,.0f} TL", delta=f"{g_kar:,.0f} TL")
    c3.metric("Toplam Getiri", f"%{g_yuzde:.2f}", delta=f"%{g_yuzde:.2f}")

    st.markdown("---")
    
    # Tabloyu Gösterme
    df = pd.DataFrame(tablo_verisi)
    if not df.empty:
        df = df.sort_values("Genel Kâr %", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Hisse Silme
    st.markdown("---")
    silinecek = st.selectbox("Hisse Sil", [h['Sembol'] for h in hisseler])
    if st.button("Seçili Hisseyi Çıkar"):
        portfoyler[secili_portfoy] = [h for h in portfoyler[secili_portfoy] if h['Sembol'] != silinecek]
        st.rerun()