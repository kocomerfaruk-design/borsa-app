import streamlit as st
import yfinance as yf

# Sayfa ayarları (Sekme başlığı ve ikon)
st.set_page_config(page_title="Pro Borsa Takip", page_icon="🚀", layout="wide")

st.title("🚀 Pro Borsa Analizi")
st.markdown("---")

# --- YAN MENÜ (INPUT) ---
st.sidebar.header("⚙️ Portföy Ayarları")
hisse_sembolu = st.sidebar.text_input("Hisse Sembolü (Örn: THYAO.IS, AAPL)", "THYAO.IS")
alis_fiyati = st.sidebar.number_input("Alış Fiyatın (TL/Dolar)", min_value=0.01, value=100.0, step=0.1)
adet = st.sidebar.number_input("Kaç Adet?", min_value=1, value=10)

if st.sidebar.button("Analiz Et"):
    try:
        # Verileri çekiyoruz
        with st.spinner(f'{hisse_sembolu} verileri internetten çekiliyor...'):
            hisse = yf.Ticker(hisse_sembolu)
            gecmis_veri = hisse.history(period="1mo")
            guncel_fiyat = gecmis_veri['Close'].iloc[-1]
        
        # --- HESAPLAMALAR ---
        maliyet = alis_fiyati * adet
        guncel_deger = guncel_fiyat * adet
        kar_zarar_tl = guncel_deger - maliyet
        
        # Yüzde Hesaplama Formülü: ((Yeni - Eski) / Eski) * 100
        yuzde_kar = ((guncel_fiyat - alis_fiyati) / alis_fiyati) * 100
        
        # --- GÖRSELLEŞTİRME (4 SÜTUN) ---
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Anlık Fiyat", f"{guncel_fiyat:.2f}")
        col2.metric("Toplam Değer", f"{guncel_deger:.2f}")
        col3.metric("Net Kâr/Zarar (TL)", f"{kar_zarar_tl:.2f} TL", delta=kar_zarar_tl)
        
        # İşte istediğin Yüzde Göstergesi (Delta rengi otomatik yeşil/kırmızı olur)
        col4.metric("Kâr Oranı (%)", f"%{yuzde_kar:.2f}", delta=f"%{yuzde_kar:.2f}")

        # --- GRAFİK ---
        st.markdown("---")
        st.subheader(f"📈 {hisse_sembolu} - 30 Günlük Trend")
        st.area_chart(gecmis_veri['Close'], color="#00FF00" if yuzde_kar > 0 else "#FF0000")
        
        # --- DURUM MESAJI ---
        if yuzde_kar > 0:
            st.success(f"Tebrikler! Paran %{yuzde_kar:.2f} oranında değerlendi! 🤑")
        elif yuzde_kar < 0:
            st.error(f"Dikkat! Şu an %{yuzde_kar:.2f} zarardasın. Sabırlı ol. 📉")
        else:
            st.warning("Başabaş noktasındasın.")
            
    except Exception as e:
        st.error(f"Hata oluştu! Sembolü kontrol et. (Hata detayı: {e})")
else:
    st.info("👈 Sol menüden hisseni gir ve 'Analiz Et' butonuna bas.")