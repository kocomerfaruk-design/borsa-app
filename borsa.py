import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime, date

# --- AYARLAR ---
DOSYA_ADI = "portfoy_verileri.json"
st.set_page_config(page_title="Pro Portföy Yönetimi", page_icon="📈", layout="wide")

# --- VERİTABANI YÖNETİMİ ---
def veri_yukle():
    if not os.path.exists(DOSYA_ADI):
        return {} 
    with open(DOSYA_ADI, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def veri_kaydet(veri):
    with open(DOSYA_ADI, "w") as f:
        json.dump(veri, f, default=str) # Tarih formatı hatası olmaması için str

# Verileri Çek
portfoyler = veri_yukle()

# --- OTOMATİK PORTFÖY YÜKLEYİCİ (TARİHLİ!) ---

# 1. Alfa Portföyü (Başlangıç: 2024-09-01)
if "Alfa Portföyü" not in portfoyler:
    portfoyler["Alfa Portföyü"] = [
        {"Sembol": "INVEO.IS", "Maliyet": 8.78, "Adet": 1139, "Tarih": "2024-09-01"},
        {"Sembol": "SANEL.IS", "Maliyet": 32.00, "Adet": 312, "Tarih": "2024-09-01"},
        {"Sembol": "KRSTL.IS", "Maliyet": 11.47, "Adet": 871, "Tarih": "2024-09-01"},
        {"Sembol": "ISGSY.IS", "Maliyet": 73.40, "Adet": 136, "Tarih": "2024-09-01"},
        {"Sembol": "MACKO.IS", "Maliyet": 25.78, "Adet": 388, "Tarih": "2024-09-01"}
    ]
    veri_kaydet(portfoyler)

# 2. Beta Portföyü (Başlangıç: 2024-09-01)
if "Beta Portföyü" not in portfoyler:
    portfoyler["Beta Portföyü"] = [
        {"Sembol": "NTGAZ.IS", "Maliyet": 11.49, "Adet": 870, "Tarih": "2024-09-01"},
        {"Sembol": "TKNSA.IS", "Maliyet": 25.48, "Adet": 392, "Tarih": "2024-09-01"},
        {"Sembol": "ATATP.IS", "Maliyet": 156.60, "Adet": 63, "Tarih": "2024-09-01"},
        {"Sembol": "BIZIM.IS", "Maliyet": 32.18, "Adet": 310, "Tarih": "2024-09-01"},
        {"Sembol": "ALVES.IS", "Maliyet": 4.22, "Adet": 2369, "Tarih": "2024-09-01"}
    ]
    veri_kaydet(portfoyler)

# 3. Delta Portföyü (Başlangıç: 2026-01-01)
if "Delta Portföyü" not in portfoyler:
    portfoyler["Delta Portföyü"] = [
        {"Sembol": "EKGYO.IS", "Maliyet": 25.50, "Adet": 392, "Tarih": "2026-01-01"},
        {"Sembol": "IZENR.IS", "Maliyet": 9.53, "Adet": 1049, "Tarih": "2026-01-01"},
        {"Sembol": "GUBRF.IS", "Maliyet": 480.50, "Adet": 20, "Tarih": "2026-01-01"},
        {"Sembol": "KTLEV.IS", "Maliyet": 38.20, "Adet": 261, "Tarih": "2026-01-01"}
    ]
    veri_kaydet(portfoyler)

if not portfoyler:
    portfoyler = {"Ana Portföy": []}
    veri_kaydet(portfoyler)

# --- YAN MENÜ ---
st.sidebar.title("🗂️ Portföylerim")

# Yeni Liste Ekleme
yeni_portfoy_adi = st.sidebar.text_input("Yeni Liste Oluştur", placeholder="Örn: Takip Listesi")
if st.sidebar.button("Listeyi Ekle"):
    if yeni_portfoy_adi and yeni_portfoy_adi not in portfoyler:
        portfoyler[yeni_portfoy_adi] = []
        veri_kaydet(portfoyler)
        st.rerun()

# Portföy Seçimi
secenekler = list(portfoyler.keys())
index_secim = 0
if "Beta Portföyü" in secenekler: index_secim = secenekler.index("Beta Portföyü")
secili_portfoy = st.sidebar.selectbox("Çalışılacak Liste", secenekler, index=index_secim)

# Silme Butonu
if st.sidebar.button(f"🗑️ '{secili_portfoy}' Sil"):
    if len(portfoyler) > 1:
        del portfoyler[secili_portfoy]
        veri_kaydet(portfoyler)
        st.rerun()

st.sidebar.markdown("---")

# --- HİSSE EKLEME (TARİHLİ) ---
st.sidebar.header(f"➕ {secili_portfoy} Ekle")
yeni_sembol = st.sidebar.text_input("Sembol", placeholder="THYAO.IS").upper()
yeni_fiyat = st.sidebar.number_input("Maliyet", min_value=0.0, format="%.2f")
yeni_adet = st.sidebar.number_input("Adet", min_value=0, step=1)
# İşte Yeni Özellik: TARİH SEÇİCİ
yeni_tarih = st.sidebar.date_input("Alım Tarihi", value=date.today())

if st.sidebar.button("Hisse Ekle"):
    if yeni_sembol and yeni_adet > 0:
        portfoyler[secili_portfoy].append({
            "Sembol": yeni_sembol, 
            "Maliyet": yeni_fiyat, 
            "Adet": yeni_adet,
            "Tarih": str(yeni_tarih)
        })
        veri_kaydet(portfoyler)
        st.sidebar.success("Eklendi!")
        st.rerun()

# --- ANA EKRAN ---
st.title(f"📊 {secili_portfoy} Analizi")

hisseler = portfoyler[secili_portfoy]

if not hisseler:
    st.info("Bu liste şu an boş. Sol taraftan hisse ekleyin.")
else:
    if st.button("🔄 Verileri Güncelle"):
        st.rerun()

    tablo_verisi = []
    toplam_maliyet = 0
    toplam_deger = 0

    bar = st.progress(0)
    for i, hisse in enumerate(hisseler):
        try:
            ticker = yf.Ticker(hisse["Sembol"])
            
            # Veri çekme (Eğer tarih varsa o tarihten al yoksa son 1 ay)
            baslangic_tarihi = hisse.get("Tarih", "2024-01-01")
            hist = ticker.history(start=baslangic_tarihi)
            
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
                "Alım Tarihi": baslangic_tarihi,
                "Adet": hisse["Adet"],
                "Ort. Maliyet": f"{hisse['Maliyet']:.2f}",
                "Anlık Fiyat": f"{guncel_fiyat:.2f}",
                "Kâr/Zarar": round(kar_tl, 2),
                "Getiri %": round(kar_yuzde, 2)
            })
        except:
            st.error(f"{hisse['Sembol']} verisi alınamadı.")
        
        bar.progress((i + 1) / len(hisseler))
    
    bar.empty()

    # Özet Kartlar
    genel_kar = toplam_deger - toplam_maliyet
    genel_yuzde = (genel_kar / toplam_maliyet * 100) if toplam_maliyet > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Yatırım", f"{toplam_maliyet:,.2f} TL")
    c2.metric("Güncel Değer", f"{toplam_deger:,.2f} TL", delta=f"{genel_kar:,.2f} TL")
    c3.metric("Genel Getiri", f"%{genel_yuzde:.2f}", delta=f"%{genel_yuzde:.2f}")

    st.markdown("---")
    
    # --- GRAFİK BÖLÜMÜ (YENİ!) ---
    col_tablo, col_grafik = st.columns([1.5, 2]) # Tablo dar, grafik geniş olsun
    
    with col_tablo:
        st.subheader("📋 Hisse Listesi")
        if tablo_verisi:
            df = pd.DataFrame(tablo_verisi).sort_values("Getiri %", ascending=False)
            st.dataframe(df[["Hisse", "Getiri %", "Kâr/Zarar", "Alım Tarihi"]], use_container_width=True)
            
            # Silme işlemi
            silinecek = st.selectbox("Çıkarılacak Hisse", [h['Sembol'] for h in hisseler], key="sil_key")
            if st.button("Seçili Hisseyi Çıkar"):
                portfoyler[secili_portfoy] = [h for h in portfoyler[secili_portfoy] if h['Sembol'] != silinecek]
                veri_kaydet(portfoyler)
                st.rerun()

    with col_grafik:
        st.subheader("📈 Tarihsel Performans Grafiği")
        # Kullanıcı hangi hissenin grafiğini görmek istiyor?
        secilen_grafik_hisse = st.selectbox("Grafiğini incelemek istediğin hisseyi seç:", [h['Sembol'] for h in hisseler])
        
        if secilen_grafik_hisse:
            # Seçilen hissenin verilerini bul
            hisse_detay = next((item for item in hisseler if item["Sembol"] == secilen_grafik_hisse), None)
            
            if hisse_detay:
                with st.spinner(f"{secilen_grafik_hisse} grafiği hazırlanıyor..."):
                    # O hissenin alım tarihinden bugüne verisini çek
                    baslangic = hisse_detay.get("Tarih", "2024-01-01")
                    ticker = yf.Ticker(secilen_grafik_hisse)
                    tarihsel_veri = ticker.history(start=baslangic)
                    
                    if not tarihsel_veri.empty:
                        # Maliyet çizgisini de grafiğe ekleyelim mi? Harika olur.
                        # Ama Streamlit'in basit grafiğinde sadece kapanışı gösterelim şimdilik karışmasın.
                        st.line_chart(tarihsel_veri['Close'], color="#00FF00")
                        st.info(f"📅 Grafik Başlangıcı: {baslangic} (Alım Tarihin)")
                    else:
                        st.warning("Bu tarih aralığı için grafik verisi bulunamadı.")