import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle,
    deneme_ekle, denemeleri_getir, deneme_durum_guncelle
)

# Veritabanı Kurulumu
init_db()

st.set_page_config(page_title="RingMaster SaaS v3.5", page_icon="🥊", layout="wide")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

randevu_toplam = randevu_sayisi()
IS_PRO = st.sidebar.checkbox("Pro Lisansı Aktifleştir", value=True)

if not IS_PRO:
    st.sidebar.warning(f"🔴 Deneme Sürümü: {randevu_toplam}/3 Randevu")
else:
    st.sidebar.success("🟢 PRO PAKET AKTİF")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🥊 Deneme Dersi (Lead)",
    "👤 Üye Yönetimi & Kuşak", 
    "📅 Randevu & Ders", 
    "💰 Aidat Takip Paneli", 
    "📱 WhatsApp & SMS Otomasyonu",
    "🤖 AI RingMaster Chat Koç"
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# --- TAB 1: DENEME DERSİ ---
with tab1:
    st.subheader("🥊 Potansiyel Sporcu Deneme Dersi Kaydı")
    with st.form("deneme_form", clear_on_submit=True):
        col_d1, col_d2 = st.columns(2)
        d_ad = col_d1.text_input("Aday Sporcu Adı Soyadı")
        d_tel = col_d1.text_input("Telefon (örn: 905xxxxxxxxx)")
        d_brans = col_d1.selectbox("İlgilendiği Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness"])
        d_tarih = col_d2.date_input("Deneme Dersi Tarihi", datetime.date.today())
        d_saat = col_d2.time_input("Deneme Dersi Saati", datetime.time(19, 0))
        d_not = col_d2.text_input("Not", "")
        
        submit_d = st.form_submit_button("➕ Deneme Dersi Kaydet")
        if submit_d and d_ad and d_tel:
            deneme_ekle(d_ad, d_tel, d_brans, str(d_tarih), str(d_saat), d_not)
            st.success(f"{d_ad} kaydoldu!")

    st.markdown("---")
    st.subheader("📌 Deneme Dersleri Listesi")
    denemeler = denemeleri_getir()
    if denemeler:
        for den in denemeler:
            st.write(f"👤 **{den[1]}** ({den[3]}) - 📞 {den[2]} | 🗓️ {den[4]} {den[5]} | Durum: `{den[6]}`")
    else:
        st.info("Planlanmış deneme dersi yok.")

# --- TAB 2: ÜYE YÖNETİMİ ---
with tab2:
    st.subheader("Yeni Sporcu Kaydı")
    with st.form("uye_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        ad_soyad = col1.text_input("Adı Soyadı")
        telefon = col1.text_input("Telefon (örn: 905xxxxxxxxx)")
        brans = col1.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness"])
        kusak = col2.selectbox("Mevcut Kuşak", KUSAKLAR)
        aidat_tarihi = col2.date_input("Son Aidat Tarihi", datetime.date.today())
        aidat_durumu = col2.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
        
        submit = st.form_submit_button("➕ Sporcuyu Kaydet")
        if submit and ad_soyad and telefon:
            uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu, str(datetime.date.today()))
            st.success(f"{ad_soyad} başarıyla eklendi!")

    st.markdown("---")
    st.subheader("📋 Kayıtlı Sporcular")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            st.write(f"🥊 **{u[1]}** | Branş: {u[3]} | 🥋 Kuşak: **{u[4]}** | Aidat: `{u[6]}`")
    else:
        st.info("Kayıtlı sporcu yok.")

# --- TAB 3: RANDEVULAR ---
with tab3:
    st.subheader("Randevu Takvimi")
    randevular = randevulari_getir()
    if randevular:
        for r in randevular:
            st.write(f"🗓️ **{r[3]} {r[4]}** - 🥊 **{r[1]}** ({r[2]})")
    else:
        st.info("Randevu bulunmuyor.")

# --- TAB 4: AİDAT ---
with tab4:
    st.subheader("💰 Aidat Takibi")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            st.write(f"👤 **{u[1]}** - Son Tarih: {u[5]} - Durum: **{u[6]}**")

# --- TAB 5: WHATSAPP / SMS ---
with tab5:
    st.subheader("📱 İletişim Otomasyonu")
    st.write("Sporcularınıza doğrudan mesaj veya SMS gönderebilirsiniz.")

# --- TAB 6: AI RİNGMASTER CHAT KOÇ (YENİ CANLI CHAT MODU) ---
with tab6:
    st.subheader("🤖 AI RingMaster Canlı Chat Asistanı")
    st.write("7/24 Salon Yönetim, Antrenman ve İkna Koçunuz. İstediğiniz soruyu sorun veya tavsiye isteyin!")

    # Chat Geçmişi Başlatma
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Selam Şampiyon! 🥊 Ben RingMaster AI Koçun. Bugün antrenman programı mı yazalım, ikna mesajı mı oluşturalım yoksa sporcu tavsiyesi mi istersin?"}
        ]

    # Geçmiş Mesajları Ekrana Yazma
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcı Mesaj Girişi
    if prompt := st.chat_input("RingMaster AI Koç'a bir soru sorun veya komut verin..."):
        # Kullanıcı mesajını ekle ve göster
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Yanıt Mantığı
        p_lower = prompt.lower()
        if "antrenman" in p_lower or "program" in p_lower:
            response = """
### 🥊 Özelleştirilmiş Antrenman Programı
**1. Isınma (15 Dk):** 3 Raund İp Atlama & Omuz Mobilite  
**2. Teknik (20 Dk):** 3 Raund Gölge Boksu (Direk-Kanca) + 3 Raund Torba  
**3. Kondisyon (20 Dk):** 4 Raund Lapa & 50 Şınav / Plank  
**4. Soğuma (5 Dk):** Statik esnetme.
            """
        elif "aidat" in p_lower or "mesaj" in p_lower or "ikna" in p_lower:
            response = """
### 📱 Üye İkna & Hatırlatma Metni
"Selam Şampiyon! 🥊 RingMaster Salonu antrenman ritmini aksatmaman için seni bu akşam salona bekliyoruz. Unutma, en zor adım salona gelene kadardır! 💥"
            """
        elif "beslenme" in p_lower or "kilo" in p_lower:
            response = """
### 🥗 Sporcu Beslenme Tavsiyesi
- **Antrenman Öncesi:** Yulaf + Muz (1.5 saat önce).
- **Antrenman Sonrası:** Tavuk / Yumurta + Pirinç.
- **Hidrasyon:** Antrenmanda en az 1.5 L su.
            """
        else:
            response = f"Anlaşıldı Şampiyon! **'{prompt}'** ile ilgili salon yönetiminde sana destek olmaya hazırım. Antrenman, aidat takibi veya üye ikna metinleri için komut verebilirsin! 🥊"

        # AI yanıtını ekle ve göster
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
