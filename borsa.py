import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

# --- YARDIMCI FONKSİYON: GEÇMİŞ HİSSE SAYISINI BULMA ---
def o_tarihteki_hisse_sayisini_bul(ticker_obj, alis_tarihi):
    try:
        guncel_hisse_sayisi = ticker_obj.info.get('sharesOutstanding', 0)
        if not guncel_hisse_sayisi:
            return 0
        
        bolunmeler = ticker_obj.actions[ticker_obj.actions['Stock Splits'] > 0] if not ticker_obj.actions.empty else pd.DataFrame()
        
        if not bolunmeler.empty:
            gelecek_bolunmeler = bolunmeler[bolunmeler.index > pd.to_datetime(alis_tarihi, utc=True)]
            gecmis_hisse_sayisi = guncel_hisse_sayisi
            for ratio in gelecek_bolunmeler['Stock Splits']:
                if ratio > 0:
                    gecmis_hisse_sayisi = gecmis_hisse_sayisi / ratio
            return gecmis_hisse_sayisi
        else:
            return guncel_hisse_sayisi
    except:
        return ticker_obj.info.get('sharesOutstanding', 0)



# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Portföy Yönetimi", page_icon="💼", layout="wide")

# --- VARSAYILAN PORTFÖYLER ---
def varsayilan_yukle():
    return {
        "Alfa Portföyü (Yüksek Risk)": [
            {"Sembol": "A1CAP.IS", "Maliyet": 17.58, "Adet": 283, "Tarih": "2025-03-03"},
            {"Sembol": "ESCOM.IS", "Maliyet": 5.87, "Adet": 849, "Tarih": "2025-03-03"},
            {"Sembol": "KRSTL.IS", "Maliyet": 9.97, "Adet": 500, "Tarih": "2025-03-03"},
            {"Sembol": "LMKDC.IS", "Maliyet": 30.88, "Adet": 161, "Tarih": "2025-03-03"},
        ],

        "Halka Arz Portföyü (~2000 TL)": [
            {"Sembol": "KOTON.IS", "Maliyet": 30.50, "Adet": 65, "Tarih": "2024-04-30"},
            {"Sembol": "LILAK.IS", "Maliyet": 37.39, "Adet": 53, "Tarih": "2024-04-30"},
            {"Sembol": "RGYAS.IS", "Maliyet": 135.00, "Adet": 14, "Tarih": "2024-04-17"},
            {"Sembol": "ENTRA.IS", "Maliyet": 10.00, "Adet": 200, "Tarih": "2024-03-27"},
            {"Sembol": "ODINE.IS", "Maliyet": 30.00, "Adet": 66, "Tarih": "2024-03-13"},
            {"Sembol": "MOGAN.IS", "Maliyet": 11.33, "Adet": 176, "Tarih": "2024-02-28"},
            {"Sembol": "ARTMS.IS", "Maliyet": 25.35, "Adet": 78, "Tarih": "2024-02-27"},
            {"Sembol": "YIGIT.IS", "Maliyet": 34.68, "Adet": 57, "Tarih": "2024-05-29"},
            {"Sembol": "ALKLC.IS", "Maliyet": 22.98, "Adet": 87, "Tarih": "2024-05-29"},
            {"Sembol": "OZYSR.IS", "Maliyet": 28.00, "Adet": 71, "Tarih": "2024-05-23"},
            {"Sembol": "ONRYT.IS", "Maliyet": 49.50, "Adet": 40, "Tarih": "2024-05-22"},
            {"Sembol": "HRKET.IS", "Maliyet": 70.00, "Adet": 28, "Tarih": "2024-05-15"},
            {"Sembol": "KOCMT.IS", "Maliyet": 20.50, "Adet": 97, "Tarih": "2024-05-09"},
            {"Sembol": "ALTNY.IS", "Maliyet": 32.00, "Adet": 62, "Tarih": "2024-05-08"},
            {"Sembol": "TCKRC.IS", "Maliyet": 24.00, "Adet": 83, "Tarih": "2024-08-14"},
            {"Sembol": "BAHKM.IS", "Maliyet": 51.00, "Adet": 39, "Tarih": "2024-08-05"},
            {"Sembol": "DCTTR.IS", "Maliyet": 14.00, "Adet": 142, "Tarih": "2024-07-25"},
            {"Sembol": "SEGMN.IS", "Maliyet": 30.00, "Adet": 66, "Tarih": "2024-06-26"},
            {"Sembol": "EFOR.IS", "Maliyet": 14.50, "Adet": 137, "Tarih": "2024-06-26"},
            {"Sembol": "HOROZ.IS", "Maliyet": 55.00, "Adet": 36, "Tarih": "2024-05-29"},
            {"Sembol": "BINBN.IS", "Maliyet": 91.85, "Adet": 21, "Tarih": "2024-10-03"},
            {"Sembol": "CGCAM.IS", "Maliyet": 20.00, "Adet": 100, "Tarih": "2024-12-11"},
            {"Sembol": "DURKN.IS", "Maliyet": 17.00, "Adet": 117, "Tarih": "2024-09-11"},
            {"Sembol": "CEMZY.IS", "Maliyet": 15.30, "Adet": 130, "Tarih": "2024-08-29"},
            {"Sembol": "OZATD.IS", "Maliyet": 105.00, "Adet": 19, "Tarih": "2024-08-27"},
            {"Sembol": "AHSGY.IS", "Maliyet": 25.20, "Adet": 79, "Tarih": "2024-08-21"},
            {"Sembol": "GUNDG.IS", "Maliyet": 35.00, "Adet": 57, "Tarih": "2024-08-15"},
            {"Sembol": "MOPAS.IS", "Maliyet": 35.00, "Adet": 57, "Tarih": "2025-01-21"},
            {"Sembol": "SRNIT.IS", "Maliyet": 12.00, "Adet": 166, "Tarih": "2025-01-27"},
            {"Sembol": "AKFIS.IS", "Maliyet": 38.70, "Adet": 51, "Tarih": "2025-01-15"},
            {"Sembol": "GLRMK.IS", "Maliyet": 125.00, "Adet": 16, "Tarih": "2025-01-08"},
            {"Sembol": "EGEGY.IS", "Maliyet": 15.00, "Adet": 133, "Tarih": "2025-01-06"},
            {"Sembol": "ARMGD.IS", "Maliyet": 40.00, "Adet": 50, "Tarih": "2024-12-25"},
            {"Sembol": "SMRVA.IS", "Maliyet": 22.00, "Adet": 90, "Tarih": "2024-12-12"},
            {"Sembol": "BALSU.IS", "Maliyet": 17.57, "Adet": 113, "Tarih": "2025-02-12"},
            {"Sembol": "KLYPV.IS", "Maliyet": 70.30, "Adet": 28, "Tarih": "2025-02-05"},
            {"Sembol": "ENDAE.IS", "Maliyet": 17.44, "Adet": 114, "Tarih": "2025-02-05"},
            {"Sembol": "VSNMD.IS", "Maliyet": 37.44, "Adet": 53, "Tarih": "2025-02-03"},
            {"Sembol": "DSTKF.IS", "Maliyet": 46.98, "Adet": 42, "Tarih": "2025-01-29"},
            {"Sembol": "BIGEN.IS", "Maliyet": 12.14, "Adet": 164, "Tarih": "2025-01-28"},
            {"Sembol": "VAKFA.IS", "Maliyet": 14.20, "Adet": 140, "Tarih": "2025-11-12"},
            {"Sembol": "ECOGR.IS", "Maliyet": 10.40, "Adet": 192, "Tarih": "2025-10-22"},
            {"Sembol": "MARMR.IS", "Maliyet": 1.36, "Adet": 1470, "Tarih": "2025-09-16"},
            {"Sembol": "DOFRB.IS", "Maliyet": 45.00, "Adet": 44, "Tarih": "2025-09-03"},
            {"Sembol": "DMLKT.IS", "Maliyet": 7.59, "Adet": 263, "Tarih": "2025-08-04"},
            {"Sembol": "BULGS.IS", "Maliyet": 12.18, "Adet": 164, "Tarih": "2025-02-14"},
            {"Sembol": "UCAY.IS", "Maliyet": 18.00, "Adet": 111, "Tarih": "2026-01-14"},
            {"Sembol": "FRMPL.IS", "Maliyet": 30.24, "Adet": 66, "Tarih": "2026-01-07"},
            {"Sembol": "ZGYO.IS", "Maliyet": 9.77, "Adet": 204, "Tarih": "2026-01-07"},
            {"Sembol": "MEYSU.IS", "Maliyet": 7.50, "Adet": 266, "Tarih": "2026-01-05"},
            {"Sembol": "ARFYE.IS", "Maliyet": 19.50, "Adet": 102, "Tarih": "2025-12-25"},
            {"Sembol": "ZERGY.IS", "Maliyet": 13.00, "Adet": 153, "Tarih": "2025-12-10"},
            {"Sembol": "PAHOL.IS", "Maliyet": 1.50, "Adet": 1333, "Tarih": "2025-11-12"},
            {"Sembol": "ATATR.IS", "Maliyet": 11.20, "Adet": 178, "Tarih": "2026-02-11"},
            {"Sembol": "BESTE.IS", "Maliyet": 14.70, "Adet": 136, "Tarih": "2026-02-05"},
            {"Sembol": "AKHAN.IS", "Maliyet": 21.50, "Adet": 93, "Tarih": "2026-01-28"},
            {"Sembol": "NETCD.IS", "Maliyet": 46.00, "Adet": 43, "Tarih": "2026-01-28"},
        ]
    }

# --- HAFIZA YÖNETİMİ ---
if 'portfoyler' not in st.session_state:
    st.session_state['portfoyler'] = varsayilan_yukle()

portfoyler = st.session_state['portfoyler']

# --- YAN MENÜ: YÖNETİM ---
st.sidebar.title("🛠️ Portföy Yönetimi")

yeni_liste_adi = st.sidebar.text_input("Yeni Liste Adı", placeholder="Örn: Takip Listem")
if st.sidebar.button("Liste Oluştur"):
    if yeni_liste_adi and yeni_liste_adi not in portfoyler:
        portfoyler[yeni_liste_adi] = []
        st.rerun()

st.sidebar.markdown("---")
secenekler = list(portfoyler.keys())
secili_portfoy = st.sidebar.selectbox("Görüntülenecek Liste", secenekler)
st.sidebar.markdown("---")

st.sidebar.header(f"➕ {secili_portfoy} Ekle")
with st.sidebar.form("hisse_ekle_form"):
    s_sembol = st.text_input("Sembol (Örn: THYAO.IS)").upper()
    s_maliyet = st.number_input("Maliyet", min_value=0.0, format="%.2f")
    s_adet = st.number_input("Adet", min_value=1, step=1)
    s_tarih = st.date_input("Alım Tarihi", value=date.today())
    
    if st.form_submit_button("Hisse Ekle"):
        if s_sembol:
            portfoyler[secili_portfoy].append({
                "Sembol": s_sembol,
                "Maliyet": s_maliyet,
                "Adet": s_adet,
                "Tarih": str(s_tarih)
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
            hist = ticker.history(period="1d")
            g_fiyat = hist['Close'].iloc[-1] if not hist.empty else hisse["Maliyet"]
            
            alis_tarihi = hisse.get("Tarih", "2024-01-01")
            
            # --- 1. SPLIT KONTROLÜ: Alış tarihinden sonra gerçek bölünme oldu mu? ---
            guncel_adet = hisse["Adet"]
            split_notu = "-"
            try:
                if hasattr(ticker, 'actions') and not ticker.actions.empty:
                    bolunmeler = ticker.actions[ticker.actions['Stock Splits'] > 0]
                    if not bolunmeler.empty:
                        alis_dt = pd.to_datetime(alis_tarihi, utc=True)
                        sonraki = bolunmeler[bolunmeler.index > alis_dt]
                        if not sonraki.empty:
                            carpan = 1.0
                            for ratio in sonraki['Stock Splits']:
                                carpan *= ratio
                            guncel_adet = hisse["Adet"] * carpan
                            split_notu = f"✅ {carpan:.0f}x"
            except:
                pass

            # --- 2. PİYASA DEĞERİ HESABI ---
            alis_hisse_sayisi = o_tarihteki_hisse_sayisini_bul(ticker, alis_tarihi)
            alis_ani_pd = (alis_hisse_sayisi * hisse["Maliyet"]) / 1_000_000_000 if alis_hisse_sayisi else 0

            guncel_pd = ticker.info.get('marketCap', 0)
            guncel_pd_milyar = guncel_pd / 1_000_000_000 if guncel_pd else 0

            # --- 3. KÂR/ZARAR: PD BÜYÜMESI BAZLI (split'ten bağımsız, her zaman doğru) ---
            m_tutar = hisse["Maliyet"] * hisse["Adet"]

            if alis_ani_pd > 0 and guncel_pd_milyar > 0:
                kar_yuzde = (guncel_pd_milyar / alis_ani_pd - 1) * 100
                kar_tl = m_tutar * (kar_yuzde / 100)
                g_tutar = m_tutar + kar_tl
            else:
                # PD verisi yoksa güncel adet × fiyat ile hesapla (split yansır)
                g_tutar = g_fiyat * guncel_adet
                kar_tl = g_tutar - m_tutar
                kar_yuzde = ((g_tutar - m_tutar) / m_tutar * 100) if m_tutar > 0 else 0

            t_maliyet += m_tutar
            t_deger += g_tutar

            tablo_verisi.append({
                "Hisse": hisse["Sembol"],
                "Alış Tarihi": alis_tarihi,
                "İlk Adet": hisse["Adet"],
                "Güncel Adet": int(guncel_adet) if guncel_adet == int(guncel_adet) else round(guncel_adet, 2),
                "Maliyet": f"{hisse['Maliyet']:.2f}",
                "Fiyat": f"{g_fiyat:.2f}",
                "Alış PD (Mlyr)": round(alis_ani_pd, 2) if alis_ani_pd > 0 else "-",
                "Güncel PD (Mlyr)": round(guncel_pd_milyar, 2) if guncel_pd_milyar > 0 else "-",
                "Değer (TL)": round(g_tutar, 2),
                "Kâr (TL)": round(kar_tl, 2),
                "Kâr %": round(kar_yuzde, 2)
            })
        except:
            pass
        bar.progress((i + 1) / len(hisseler))
    bar.empty()

    # Özet Kartlar
    g_kar = t_deger - t_maliyet
    g_yuzde = (g_kar / t_maliyet * 100) if t_maliyet > 0 else 0

    # delta_color: "normal" yeşil/kırmızı, "off" gri/nötr
    deger_renk = "normal" if g_kar != 0 else "off"
    getiri_renk = "normal" if g_yuzde != 0 else "off"

    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Yatırım", f"{t_maliyet:,.0f} TL")
    c2.metric("Güncel Değer", f"{t_deger:,.0f} TL", delta=f"{g_kar:,.0f} TL", delta_color=deger_renk)
    c3.metric("Toplam Getiri", f"%{g_yuzde:.2f}", delta=f"%{g_yuzde:.2f}", delta_color=getiri_renk)

    st.markdown("---")
    
    if tablo_verisi:
        siralama_secimi = st.radio(
            "Tablo Sıralaması:",
            ["Kâr % (Yüksekten Düşüğe)", "Alış Tarihi (Eskiden Yeniye)", "Alış Tarihi (Yeniden Eskiye)"],
            horizontal=True
        )
        
        df = pd.DataFrame(tablo_verisi)
        
        if siralama_secimi == "Kâr % (Yüksekten Düşüğe)":
            df = df.sort_values("Kâr %", ascending=False)
        elif siralama_secimi == "Alış Tarihi (Eskiden Yeniye)":
            df = df.sort_values("Alış Tarihi", ascending=True)
        elif siralama_secimi == "Alış Tarihi (Yeniden Eskiye)":
            df = df.sort_values("Alış Tarihi", ascending=False)
        
        def kirmizi_yesil_boya(val):
            if isinstance(val, (int, float)):
                if val > 0:
                    return 'color: #00CC00; font-weight: bold;'
                elif val < 0:
                    return 'color: #FF0000; font-weight: bold;'
            return ''
        
        try:
            styled_df = df.style.format(precision=2).map(kirmizi_yesil_boya, subset=["Kâr (TL)", "Kâr %"])
        except AttributeError:
            styled_df = df.style.format(precision=2).applymap(kirmizi_yesil_boya, subset=["Kâr (TL)", "Kâr %"])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Hisse Silme
    st.markdown("---")
    silinecek = st.selectbox("Hisse Sil", [h['Sembol'] for h in hisseler])
    if st.button("Seçili Hisseyi Çıkar"):
        portfoyler[secili_portfoy] = [h for h in portfoyler[secili_portfoy] if h['Sembol'] != silinecek]
        st.rerun()