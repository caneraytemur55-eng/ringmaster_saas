import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle,
    deneme_ekle, denemeleri_getir, deneme_durum_guncelle
)

# Veritabanını Başlat
init_db()

st.set_page_config(page_title="RingMaster SaaS v3.5 - Global Sürüm", page_icon="🥊", layout="wide")

# Lisans Durumu Kontrolü
randevu_toplam = randevu_sayisi()
IS_PRO = st.sidebar.checkbox("Pro Lisansı Aktifleştir", value=False)

st.sidebar.title("🥊 RingMaster SaaS v3.5")
if not IS_PRO:
    st.sidebar.warning(f"🔴 Deneme Sürümü: {randevu_toplam}/3 Randevu Kullanıldı")
    if randevu_toplam >= 3:
        st.sidebar.error("⚠️ Ücretsiz limit doldu! Pro Pakete geçin.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Pro Pakete Geç")
    st.sidebar.write("**₺499 / Ay** veya **$19 / Month** (Deneme Dersi & AI Asistan)")
    st.sidebar.info("Ödeme için TR IBAN / Stripe ile transfer yapıp aktifleştirebilirsiniz.")
else:
    st.sidebar.success("🟢 PRO PAKET AKTİF")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🥊 Deneme Dersi (Lead)",
    "👤 Üye Yönetimi & Kuşak", 
    "📅 Randevu & Ders", 
    "💰 Aidat Takip Paneli", 
    "📱 WhatsApp & SMS Otomasyonu",
    "🤖 AI RingMaster Asistan"
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# --- TAB 1: DENEME DERSİ (LEAD YÖNETİMİ) ---
with tab1:
    st.subheader("🥊 Potansiyel Sporcu Deneme Dersi Kaydı")
    with st.form("deneme_form", clear_on_submit=True):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            d_ad = st.text_input("Aday Sporcu Adı Soyadı")
            d_tel = st.text_input("Telefon (örn: 905xxxxxxxxx)")
            d_brans = st.selectbox("İlgilendiği Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col_d2:
            d_tarih = st.date_input("Deneme Dersi Tarihi", datetime.date.today())
            d_saat = st.time_input("Deneme Dersi Saati", datetime.time(19, 0))
            d_not = st.text_input("Not (Örn: Daha önce boks yapmış, kilo vermek istiyor)", "")
        
        submit_d = st.form_submit_button("➕ Deneme Dersi Randevusu Oluştur")
        if submit_d:
            if d_ad and d_tel:
                deneme_ekle(d_ad, d_tel, d_brans, str(d_tarih), str(d_saat), d_not)
                st.success(f"🎉 {d_ad} için deneme dersi randevusu kaydoldu!")
                st.rerun()
            else:
                st.error("Lütfen Ad Soyad ve Telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("📌 Planlanan Deneme Dersleri & Dönüşüm Paneli")
    denemeler = denemeleri_getir()
    if denemeler:
        for den in denemeler:
            den_id, den_ad, den_tel, den_brans, den_tarih, den_saat, den_durum, den_not = den
            col_x1, col_x2, col_x3, col_x4 = st.columns([2, 2, 2, 2])
            
            col_x1.write(f"**{den_ad}** ({den_brans})\n\n📞 {den_tel}")
            col_x2.write(f"🗓️ **{den_tarih} - {den_saat}**\n\n📝 Not: _{den_not}_")
            
            yeni_d_durum = col_x3.selectbox("Katılım Durumu", ["Bekliyor", "Derse Geldi 🟢", "Gelmedi 🔴"], index=["Bekliyor", "Derse Geldi 🟢", "Gelmedi 🔴"].index(den_durum) if den_durum in ["Bekliyor", "Derse Geldi 🟢", "Gelmedi 🔴"] else 0, key=f"dd_{den_id}")
            if yeni_d_durum != den_durum:
                deneme_durum_guncelle(den_id, yeni_d_durum)
                st.rerun()
                
            if col_x4.button("🏆 Asil Üye Yap & Kaydet", key=f"btn_convert_{den_id}"):
                bugun_str = str(datetime.date.today())
                uye_ekle(den_ad, den_tel, den_brans, "Beyaz Kuşak / Başlangıç", bugun_str, "Ödeme Bekliyor", bugun_str)
                deneme_durum_guncelle(den_id, "Kayıt Oldu 🏆")
                st.success(f"🔥 TEBRİKLER! {den_ad} başarıyla Asil Üye yapıldı ve Üye Listesine aktarıldı!")
                st.rerun()
            st.markdown("---")
    else:
        st.info("Henüz planlanmış deneme dersi bulunmuyor.")

# --- TAB 2: ÜYE YÖNETİMİ & KUŞAK SINAVI ---
with tab2:
    st.subheader("Yeni Sporcu Kaydı (Manuel)")
    with st.form("uye_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad_soyad = st.text_input("Sporcu Adı Soyadı")
            telefon = st.text_input("Telefon (Ülke Kodu ile örn: 905xxxxxxxxx)")
            brans = st.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col2:
            kusak = st.selectbox("Mevcut Kuşak / Seviye", KUSAKLAR)
            aidat_tarihi = st.date_input("Son Aidat Ödeme Tarihi", datetime.date.today())
            son_sinav_tarihi = st.date_input("Son Kuşak Sınavı / Başlangıç Tarihi", datetime.date.today())
            aidat_durumu = st.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
        
        submit = st.form_submit_button("➕ Sporcuyu Kaydet")
        if submit:
            if ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu, str(son_sinav_tarihi))
                st.success(f"{ad_soyad} başarıyla kaydedildi!")
                st.rerun()
            else:
                st.error("Lütfen ad soyad ve telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("🥋 Kuşak Derece Sınavı Uyarı & Takip Paneli")
    uyeler = uyeleri_getir()
    if uyeler:
        bugun = datetime.date.today()
        for u in uyeler:
            u_id = u[0]
            u_ad = u[1]
            u_tel = u[2]
            u_brans = u[3]
            u_kusak = u[4]
            u_sinav_t_str = u[7] if len(u) > 7 and u[7] else str(bugun)
            
            try:
                u_sinav_t = datetime.datetime.strptime(u_sinav_t_str, "%Y-%m-%d").date()
            except ValueError:
                u_sinav_t = bugun

            gecen_gun = (bugun - u_sinav_t).days
            
            if gecen_gun >= 90:
                sinav_durumu = f"🔴 **Sınav Vakti Geldi!** ({gecen_gun} gündür aynı kuşakta)"
            elif gecen_gun >= 75:
                sinav_durumu = f"🟡 **Sınav Yaklaştı** ({gecen_gun} gün oldu)"
            else:
                sinav_durumu = f"🟢 **Normal** ({gecen_gun} gündür mevcut kuşakta)"

            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            col_a.write(f"**{u_ad}** ({u_brans})")
            col_b.write(f"🥋 **{u_kusak}**\n\n{sinav_durumu}")
            
            yeni_k = col_c.selectbox("Kuşak / Derece Yükselt", KUSAKLAR, index=KUSAKLAR.index(u_kusak) if u_kusak in KUSAKLAR else 0, key=f"k_{u_id}")
            if col_d.button("🥋 Sınavı Geçti / Yükselt", key=f"btn_k_{u_id}"):
                kusak_guncelle(u_id, yeni_k, str(bugun))
                st.success(f"🎉 {u_ad} yeni kuşağa geçti! Sınav tarihi güncellendi.")
                st.rerun()
            st.markdown("---")
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")

# --- TAB 3: RANDEVU TAKVİMİ ---
with tab3:
    st.subheader("Yeni Randevu / Antrenman Oluştur")
    uyeler = uyeleri_getir()
    
    if not IS_PRO and randevu_toplam >= 3:
        st.error("🔴 Ücretsiz deneme limitiniz (3 Randevu) doldu. Yeni randevu eklemek için Pro Pakete geçin.")
    else:
        if uyeler:
            uye_dict = {f"{u[1]} ({u[3]})": u[0] for u in uyeler}
            secilen_uye_str = st.selectbox("Sporcu Seç", list(uye_dict.keys()))
            secilen_id = uye_dict[secilen_uye_str]
            
            col_r1, col_r2 = st.columns(2)
            tarih = col_r1.date_input("Randevu Tarihi", datetime.date.today())
            saat = col_r2.time_input("Randevu Saati", datetime.time(18, 0))
            
            if st.button("📅 Randevuyu Onayla ve Kaydet"):
                randevu_ekle(secilen_id, str(tarih), str(saat))
                st.success("Randevu başarıyla eklendi!")
                st.rerun()
        else:
            st.warning("Randevu oluşturabilmek için önce 'Üye Yönetimi' sekmesinden üye eklemelisiniz.")

    st.markdown("---")
    st.subheader("📌 Planlanan Antrenmanlar")
    randevular = randevulari_getir()
    if randevular:
        for r in randevular:
            st.write(f"🗓️ **{r[3]} - {r[4]}** | 🥊 **{r[1]}** ({r[2]}) - Durum: `{r[5]}`")
    else:
        st.info("Planlanmış randevu bulunmuyor.")

# --- TAB 4: AİDAT TAKİP PANELSİ ---
with tab4:
    st.subheader("💰 Sporcu Aidat Durumları ve Kasası")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u[0], u[1], u[2], u[3], u[4], u[5], u[6]
            col_m1, col_m2, col_m3, col_m4 = st.columns([2, 2, 2, 2])
            
            col_m1.write(f"**{u_ad}**")
            col_m2.write(f"🗓️ Son Tarih: **{u_aidat_t}**")
            
            durum_renk = "🟢 Ödendi" if u_aidat_d == "Ödendi" else "🔴 Ödeme Bekliyor"
            col_m3.write(f"Durum: **{durum_renk}**")
            
            yeni_aidat_d = col_m4.selectbox("Durum Değiştir", ["Ödendi", "Ödeme Bekliyor"], index=0 if u_aidat_d == "Ödendi" else 1, key=f"a_{u_id}")
            if yeni_aidat_d != u_aidat_d:
                aidat_durum_guncelle(u_id, yeni_aidat_d)
                st.success(f"{u_ad} aidat durumu güncellendi!")
                st.rerun()
    else:
        st.info("Sistemde henüz üye yok.")

# --- TAB 5: WHATSAPP & SMS OTOMASYONU ---
with tab5:
    st.subheader("📱 WhatsApp & SMS Mesaj Fırlatıcı")
    uyeler = uyeleri_getir()
    denemeler = denemeleri_getir()
    
    mesaj_hedef = st.radio("Mesaj Alıcısı", ["Kayıtlı Sporcular", "Deneme Dersi Adayları"])
    
    if mesaj_hedef == "Deneme Dersi Adayları" and denemeler:
        secilen_d_str = st.selectbox("Aday Seç", [f"{d[1]} ({d[3]} - {d[4]} {d[5]})" for d in denemeler])
        d_data = [d for d in denemeler if f"{d[1]} ({d[3]} - {d[4]} {d[5]})" == secilen_d_str][0]
        
        varsayilan_mesaj = f"Merhaba {d_data[1]}, RingMaster Salonu ücretsiz deneme dersi randevunuz {d_data[4]} saat {d_data[5]} olarak planlanmıştır. Havlu ve rahat spor kıyafetlerinizle salonda olmanızı bekliyoruz! 🥊"
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        
        encoded_msg = urllib.parse.quote(mesaj_metni)
        wa_url = f"https://wa.me/{d_data[2]}?text={encoded_msg}"
        sms_url = f"sms:{d_data[2]}?body={encoded_msg}"
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp İle Gönder</button></a>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown(f'<a href="{sms_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 Direct SMS / iMessage İle Gönder</button></a>', unsafe_allow_html=True)

    elif mesaj_hedef == "Kayıtlı Sporcular" and uyeler:
        secilen_w_uye = st.selectbox("Sporcu Seç", [f"{u[1]} ({u[3]})" for u in uyeler], key="wa_select")
        secilen_w_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_w_uye][0]
        u_data = [u for u in uyeler if u[0] == secilen_w_id][0]
        
        mesaj_tipi = st.radio("Mesaj Tipi Seçin", ["Kuşak Sınavı Daveti", "Randevu Hatırlatma", "Aidat Hatırlatma"])
        
        if mesaj_tipi == "Kuşak Sınavı Daveti":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Salonu Kuşak Derece Sınavınız yaklaşmıştır. Lütfen antrenörünüzle iletişime geçiniz. 🥋🥊"
        elif mesaj_tipi == "Randevu Hatırlatma":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Boks Salonu antrenman randevunuz planlanmıştır. Lütfen vaktinde salonda olunuz. 🥊"
        else:
            varsayilan_mesaj = f"Merhaba {u_data[1]}, Salon aidat ödemenizin son günü {u_data[5]}'dir. Lütfen ödemenizi gerçekleştiriniz. Teşekkürler! 💰"
            
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        encoded_msg = urllib.parse.quote(mesaj_metni)
        wa_url = f"https://wa.me/{u_data[2]}?text={encoded_msg}"
        sms_url = f"sms:{u_data[2]}?body={encoded_msg}"
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp İle Gönder</button></a>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown(f'<a href="{sms_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 Direct SMS / iMessage İle Gönder</button></a>', unsafe_allow_html=True)
    else:
        st.info("Gönderilecek veri bulunmuyor.")

# --- TAB 6: AI RİNGMASTER ASİSTAN ---
with tab6:
    st.subheader("🤖 AI RingMaster Koç & İdari Asistan")
    st.write("Dövüş sporları ve salon yönetimine özel yapay zeka asistanı. Tek tıkla antrenman programı veya ikna mesajı oluşturun!")
    
    ai_gorev = st.selectbox("AI Asistandan Ne İstiyorsunuz?", [
        "🥊 Özelleştirilmiş Dövüş / Antrenman Programı Yaz",
        "🥋 Kuşak Sınavı Hazırlık & Teknik Değerlendirme Metni",
        "🥗 Sporcu Kilo Verme / Beslenme Tavsiyesi Hazırla",
        "🔥 Deneme Dersi Sonrası Üyeliğe İkna Mesajı Hazırla"
    ])
    
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        ai_brans = st.selectbox("Branş / Seviye", ["Boks - Başlangıç", "Boks - Müsabık", "Kickboks - Orta Seviye", "Muay Thai", "Fitness"])
    with col_ai2:
        ai_hedef = st.text_input("Özel Not / Hedef (Örn: Sınav hazırlığı, patlayıcı güç)", "Deneme dersi sonrası abonelik satışı")
        
    if st.button("🚀 AI Yanıtı Üret"):
        with st.spinner("AI Antrenör düşünüyor ve metni hazırlıyor..."):
            if "Deneme Dersi" in ai_gorev:
                ai_cikti = f"""
### 🔥 Deneme Dersi Sonrası İkna & Satış Mesajı
"Harika bir antrenmandı Şampiyon! 🥊 Bugün gösterdiğin azim müthişti. {ai_hedef} hedeflerine ulaşmak için doğru yerdesin. Bu haftaya özel kontenjanımız dolmadan resmi kaydını tamamlayalım mı? Seni kadromuzda görmek isteriz!"
                """
            elif "Kuşak Sınavı" in ai_gorev:
                ai_cikti = f"""
### 🥋 Kuşak Derece Sınavı Hazırlık & Teknik Programı
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}
1. Temel Teknik Sınavı: Direk, kanca, aparkat hassasiyet testi.
2. Kondisyon & Dayanıklılık: 3 Raund lapa çalışması + 50 Şınav.
                """
            elif "Antrenman Programı" in ai_gorev:
                ai_cikti = f"""
### 🥊 {ai_brans} Akıllı Antrenman Programı
**Hedef:** {ai_hedef}
**1. Isınma (15 Dk):** 3 Raund İp Atlama & Dinamik Esnetme.
**2. Teknik (20 Dk):** Gölge Boksu & Torba Çalışması.
**3. Kondisyon (20 Dk):** Lapa Çalışması & Boks Şınavı.
                """
            else:
                ai_cikti = f"""
### 🥗 Sporcu Performans & Beslenme Rehberi
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}
- Antrenman öncesi karmaşık karbonhidrat, antrenman sonrası yüksek protein.
                """
            
            st.success("AI Yanıtı Başarıyla Oluşturuldu!")
            st.markdown(ai_cikti)
            
            enc_ai = urllib.parse.quote(ai_cikti)
            col_share1, col_share2 = st.columns(2)
            with col_share1:
                st.markdown(f'<a href="https://wa.me/?text={enc_ai}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Paylaş</button></a>', unsafe_allow_html=True)
            with col_share2:
                st.markdown(f'<a href="sms:?body={enc_ai}"><button style="background-color:#007AFF;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS / iMessage Paylaş</button></a>', unsafe_allow_html=True)import streamlit as st
import sqlite3
import urllib.parse

# --- VERİTABANI BAĞLANTISI ---
def get_db():
    conn = sqlite3.connect("ringmaster.db")
    return conn

st.set_page_config(page_title="RingMaster SaaS v3.5 Final", page_icon="🥊", layout="wide")

# --- YAN MENÜ: ÖDEME, LİSANS VE KÜRESEL AYARLAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3068/3068327.png", width=80)
st.sidebar.title("🥊 RingMaster Lisans")
st.sidebar.caption("Muğla & İzmir Pilot Sürüm")

dil_secimi = st.sidebar.selectbox("🌐 Sistem Dili / Language:", ["Türkçe (TR)", "English (US)", "Srpski (RS)"])
lisans_durumu = st.sidebar.radio("Salon Lisans Tipi:", ["🟢 Pro Paket (Aktif)", "🔴 Deneme Sürümü"])

if lisans_durumu == "🔴 Deneme Sürümü":
    st.sidebar.warning("⚠️ Deneme sürümündesiniz. Kalan Limit: 3 Randevu")
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Pro Üyelik Aktivasyonu")
    st.sidebar.write("Aylık Abonelik: **₺499 / Ay** veya **$29 / Mo**")
    
    with st.sidebar.expander("📌 IBAN / QR ile Öde (TR)"):
        st.write("**TR12 0006 2000 0000 0000 0000 00**")
        st.caption("Açıklama kısmına Salon Adı yazınız.")
        st.info("Ödeme sonrası destek hattına bildirin.")
        
    stripe_payment_link = "https://buy.stripe.com/test_ringmaster_pro"
    st.sidebar.markdown(f'''
        <a href="{stripe_payment_link}" target="_blank">
            <button style="background-color:#635BFF; color:white; border:none; padding:10px 15px; border-radius:5px; font-weight:bold; width:100%; cursor:pointer; margin-top:5px;">
                💳 Stripe ile Öde ($29)
            </button>
        </a>
    ''', unsafe_allow_html=True)
else:
    st.sidebar.success("✅ Lisansınız Sınırsız ve Aktif!")

st.title("🥊 RingMaster - Dövüş Salonu Yönetim Paneli v3.5")
st.caption("Boks, Kickboks & Lapa Özel Randevu Sistem")
st.write("---")

# --- TAB MENÜSÜ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔥 Ders/Lapa Randevusu Al", 
    "📅 Aktif Randevu Listesi", 
    "📊 Salon İstatistikleri",
    "➕ Yeni Üye Kaydı", 
    "📋 Ders & Kontenjan Ekle"
])

# 1. TAB: RANDEVU AL
with tab1:
    st.header("🥊 Antrenman/Lapa Yerini Ayırt")
    conn = get_db()
    cursor = conn.cursor()
    
    uyeler = cursor.execute("SELECT id, ad_soyad, telefon FROM uyeler").fetchall()
    dersler = cursor.execute("SELECT id, ders_adi, hoca_adi, tarih_saat, kontenjan FROM dersler").fetchall()
    
    if uyeler and dersler:
        uye_dict = {f"{u[1]} (ID: {u[0]})": (u[0], u[1], u[2]) for u in uyeler}
        ders_dict = {f"{d[1]} - {d[2]} ({d[3]}) [Kontenjan: {d[4]}]": (d[0], d[1], d[3]) for d in dersler}
        
        secilen_uye_key = st.selectbox("Dövüşçü Seçin:", options=list(uye_dict.keys()))
        secilen_ders_key = st.selectbox("Ders / Lapa Seansı Seçin:", options=list(ders_dict.keys()))
        
        if st.button("Randevuyu Mühürle! 🔥"):
            u_id, u_ad, u_tel = uye_dict[secilen_uye_key]
            d_id, d_ad, d_saat = ders_dict[secilen_ders_key]
            
            cursor.execute("INSERT INTO randevular (uye_id, ders_id) VALUES (?, ?)", (u_id, d_id))
            conn.commit()
            
            st.success("✅ Randevu başarıyla veritabanına işlendi!")
            
            mesaj = f"Merhaba {u_ad}, RingMaster üzerinden {d_saat} saatindeki '{d_ad}' dersine randevun onaylandı! Ekipmanlarını unutma, ring seni bekliyor! 🥊"
            encoded_mesaj = urllib.parse.quote(mesaj)
            wa_url = f"https://wa.me/{u_tel}?text={encoded_mesaj}"
            
            st.markdown(f'''
                <a href="{wa_url}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">
                        📱 Dövüşçüye WhatsApp Onay Mesajı Gönder
                    </button>
                </a>
            ''', unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ Randevu alabilmek için önce veritabanına en az 1 Üye ve 1 Ders eklenmelidir.")
    conn.close()

# 2. TAB: AKTİF RANDEVU LİSTESİ
with tab2:
    st.header("📅 Salon Aktif Randevuları")
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
    SELECT r.id, u.ad_soyad, u.telefon, d.ders_adi, d.hoca_adi, d.tarih_saat, r.durum
    FROM randevular r
    JOIN uyeler u ON r.uye_id = u.id
    JOIN dersler d ON r.ders_id = d.id
    WHERE r.durum = 'Onaylandı'
    """
    randevular = cursor.execute(query).fetchall()
    
    if randevular:
        for r in randevular:
            r_id, u_ad, u_tel, d_ad, h_ad, d_saat, durum = r
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"🥊 **{u_ad}** ({u_tel})")
                st.caption(f"Ders: {d_ad} | Antrenör: {h_ad} | Zaman: {d_saat}")
            with col2:
                st.info(f"Durum: {durum}")
            with col3:
                if st.button("İptal Et ❌", key=f"iptal_{r_id}"):
                    cursor.execute("UPDATE randevular SET durum = 'İptal Edildi' WHERE id = ?", (r_id,))
                    conn.commit()
                    st.warning("Randevu İptal Edildi!")
                    st.rerun()
            st.write("---")
    else:
        st.write("Henüz aktif bir randevu bulunmuyor.")
    conn.close()

# 3. TAB: İSTATİSTİKLER (YENİ)
with tab3:
    st.header("📊 Salon Performans & Analiz")
    conn = get_db()
    cursor = conn.cursor()
    
    toplam_uye = cursor.execute("SELECT COUNT(*) FROM uyeler").fetchone()[0]
    toplam_ders = cursor.execute("SELECT COUNT(*) FROM dersler").fetchone()[0]
    toplam_randevu = cursor.execute("SELECT COUNT(*) FROM randevular WHERE durum = 'Onaylandı'").fetchone()[0]
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Kayıtlı Dövüşçü", f"{toplam_uye} Sporcu")
    col_b.metric("Aktif Programlanan Ders", f"{toplam_ders} Seans")
    col_c.metric("Tamamlanan Randevu", f"{toplam_randevu} Katılım")
    
    st.write("---")
    st.subheader("💡 Hızlı Analiz")
    st.caption("Salondaki en popüler dersler ve doluluk verileri bu alanda otomatik raporlanır.")
    conn.close()

# 4. TAB: ÜYE KAYIT
with tab4:
    st.header("🥊 Yeni Dövüşçü Kaydı")
    ad_soyad = st.text_input("Ad Soyad:")
    telefon = st.text_input("Telefon (Örn: 905xxxxxxxxx):", help="WhatsApp bildirimi için ülke koduyla girin.")
    brans = st.selectbox("Branş:", ["Boks", "Kickboks", "Wing Chun", "Keysi / Taktik", "MMA / Grappling"])
    seviye = st.selectbox("Seviye:", ["Başlangıç", "Orta Sıklet", "Sparring Grubu / Pro"])
    
    if st.button("Üyeyi Kaydet 📝"):
        if ad_soyad and telefon:
            conn = get_db()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO uyeler (ad_soyad, telefon, brans, seviye) VALUES (?, ?, ?, ?)",
                               (ad_soyad, telefon, brans, seviye))
                conn.commit()
                st.success(f"✅ {ad_soyad} sisteme başarıyla eklendi!")
            except sqlite3.IntegrityError:
                st.error("❌ Bu telefon numarası zaten kayıtlı!")
            conn.close()
        else:
            st.error("Lütfen ad soyad ve telefon alanlarını doldurun!")

# 5. TAB: DERS EKLE
with tab5:
    st.header("📋 Yeni Ders veya Lapa Seansı Tanımla")
    ders_adi = st.text_input("Ders Başlığı (Örn: Özel Lapa Seansı / Akşam Sparring):")
    hoca_adi = st.text_input("Antrenör Adı:")
    tarih_saat = st.text_input("Tarih ve Saat (Örn: Pazartesi 19:00):")
    kontenjan = st.number_input("Maksimum Kontenjan:", min_value=1, value=10)
    
    if st.button("Dersi Programına Ekle 🎯"):
        if ders_adi and hoca_adi:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO dersler (ders_adi, hoca_adi, tarih_saat, kontenjan) VALUES (?, ?, ?, ?)",
                           (ders_adi, hoca_adi, tarih_saat, kontenjan))
            conn.commit()
            st.success(f"✅ '{ders_adi}' programlandı!")
            conn.close()
        else:
            st.error("Eksik bilgi girdiniz!")
            import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle
)

# Veritabanını Başlat
init_db()

st.set_page_config(page_title="RingMaster SaaS v3.5 - Ege Pilot", page_icon="🥊", layout="wide")

# Lisans Durumu Kontrolü (Free Trial: Max 3 Randevu)
randevu_toplam = randevu_sayisi()
IS_PRO = st.sidebar.checkbox("Pro Lisansı Aktifleştir", value=False)

st.sidebar.title("🥊 RingMaster SaaS v3.5")
if not IS_PRO:
    st.sidebar.warning(f"🔴 Deneme Sürümü: {randevu_toplam}/3 Randevu Kullanıldı")
    if randevu_toplam >= 3:
        st.sidebar.error("⚠️ Ücretsiz limit doldu! Pro Pakete geçin.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Pro Pakete Geç")
    st.sidebar.write("**₺499 / Ay** (Sınırsız Randevu, Aidat ve Kuşak Takibi)")
    st.sidebar.info("Ödeme için TR IBAN / QR ile transfer yapıp aktifleştirebilirsiniz.")
else:
    st.sidebar.success("🟢 PRO PAKET AKTİF")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

tab1, tab2, tab3, tab4 = st.tabs(["👤 Üye Yönetimi & Kuşak", "📅 Randevu & Ders", "💰 Aidat Takip Paneli", "📱 WhatsApp Otomasyonu"])

# KUŞAK LİSTESİ
KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# --- TAB 1: ÜYE YÖNETİMİ & KUŞAK ---
with tab1:
    st.subheader("Yeni Sporcu Kaydı")
    with st.form("uye_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad_soyad = st.text_input("Sporcu Adı Soyadı")
            telefon = st.text_input("Telefon (Başında 90 ile örn: 905xxxxxxxxx)")
            brans = st.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col2:
            kusak = st.selectbox("Kuşak / Seviye", KUSAKLAR)
            aidat_tarihi = st.date_input("Son Aidat Ödeme Tarihi", datetime.date.today())
            aidat_durumu = st.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
        
        submit = st.form_submit_button("➕ Sporcuyu Kaydet")
        if submit:
            if ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu)
                st.success(f"{ad_soyad} başarıyla kaydedildi!")
                st.rerun()
            else:
                st.error("Lütfen ad soyad ve telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("📋 Kayıtlı Sporcular ve Kuşak Dereceleri")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            col_a.write(f"**{u_ad}** ({u_brans})")
            col_b.write(f"📞 {u_tel}")
            col_c.write(f"🥋 **{u_kusak}**")
            
            # Kuşak Atlatma Seçeneği
            yeni_k = col_d.selectbox("Kuşak Güncelle", KUSAKLAR, index=KUSAKLAR.index(u_kusak) if u_kusak in KUSAKLAR else 0, key=f"k_{u_id}")
            if yeni_k != u_kusak:
                kusak_guncelle(u_id, yeni_k)
                st.success(f"{u_ad} kişisinin kuşağı güncellendi!")
                st.rerun()
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")

# --- TAB 2: RANDEVU TAKVİMİ ---
with tab2:
    st.subheader("Yeni Randevu / Antrenman Oluştur")
    uyeler = uyeleri_getir()
    
    if not IS_PRO and randevu_toplam >= 3:
        st.error("🔴 Ücretsiz deneme limitiniz (3 Randevu) doldu. Yeni randevu eklemek için Pro Pakete geçin.")
    else:
        if uyeler:
            uye_dict = {f"{u[1]} ({u[3]})": u[0] for u in uyeler}
            secilen_uye_str = st.selectbox("Sporcu Seç", list(uye_dict.keys()))
            secilen_id = uye_dict[secilen_uye_str]
            
            col_r1, col_r2 = st.columns(2)
            tarih = col_r1.date_input("Randevu Tarihi", datetime.date.today())
            saat = col_r2.time_input("Randevu Saati", datetime.time(18, 0))
            
            if st.button("📅 Randevuyu Onayla ve Kaydet"):
                randevu_ekle(secilen_id, str(tarih), str(saat))
                st.success("Randevu başarıyla eklendi!")
                st.rerun()
        else:
            st.warning("Randevu oluşturabilmek için önce 'Üye Yönetimi' sekmesinden üye eklemelisiniz.")

    st.markdown("---")
    st.subheader("📌 Planlanan Antrenmanlar")
    randevular = randevulari_getir()
    if randevular:
        for r in randevular:
            st.write(f"🗓️ **{r[3]} - {r[4]}** | 🥊 **{r[1]}** ({r[2]}) - Durum: `{r[5]}`")
    else:
        st.info("Planlanmış randevu bulunmuyor.")

# --- TAB 3: AİDAT TAKİP PANELSİ ---
with tab3:
    st.subheader("💰 Sporcu Aidat Durumları ve Kasası")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u
            col_m1, col_m2, col_m3, col_m4 = st.columns([2, 2, 2, 2])
            
            col_m1.write(f"**{u_ad}**")
            col_m2.write(f"🗓️ Son Tarih: **{u_aidat_t}**")
            
            durum_renk = "🟢 Ödendi" if u_aidat_d == "Ödendi" else "🔴 Ödeme Bekliyor"
            col_m3.write(f"Durum: **{durum_renk}**")
            
            yeni_aidat_d = col_m4.selectbox("Durum Değiştir", ["Ödendi", "Ödeme Bekliyor"], index=0 if u_aidat_d == "Ödendi" else 1, key=f"a_{u_id}")
            if yeni_aidat_d != u_aidat_d:
                aidat_durum_guncelle(u_id, yeni_aidat_d)
                st.success(f"{u_ad} aidat durumu güncellendi!")
                st.rerun()
    else:
        st.info("Sistemde henüz üye yok.")

# --- TAB 4: WHATSAPP OTOMASYONU ---
with tab4:
    st.subheader("📱 Tek Tıkla WhatsApp Mesaj Fırlatıcı")
    uyeler = uyeleri_getir()
    if uyeler:
        secilen_w_uye = st.selectbox("Mesaj Gönderilecek Sporcu", list(uye_dict.keys()), key="wa_select")
        secilen_w_id = uye_dict[secilen_w_uye]
        u_data = [u for u in uyeler if u[0] == secilen_w_id][0]
        
        mesaj_tipi = st.radio("Mesaj Tipi Seçin", ["Randevu Hatırlatma", "Aidat Hatırlatma"])
        
        if mesaj_tipi == "Randevu Hatırlatma":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Boks Salonu antrenman randevunuz planlanmıştır. Lütfen vaktinde salonda olunuz. 🥊"
        else:
            varsayilan_mesaj = f"Merhaba {u_data[1]}, Salon aidat ödemenizin son günü {u_data[5]}'dir. Lütfen ödemenizi gerçekleştiriniz. Teşekkürler! 💰"
            
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        
        encoded_msg = urllib.parse.quote(mesaj_metni)
        wa_url = f"https://wa.me/{u_data[2]}?text={encoded_msg}"
        
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Üzerinden Gönder</button></a>', unsafe_allow_html=True)
    else:
        st.info("Kayıtlı üye bulunmuyor.")
import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle
)

# Veritabanını Başlat
init_db()

st.set_page_config(page_title="RingMaster SaaS v3.5 - Ege Pilot", page_icon="🥊", layout="wide")

# Lisans Durumu Kontrolü (Free Trial: Max 3 Randevu)
randevu_toplam = randevu_sayisi()
IS_PRO = st.sidebar.checkbox("Pro Lisansı Aktifleştir", value=False)

st.sidebar.title("🥊 RingMaster SaaS v3.5")
if not IS_PRO:
    st.sidebar.warning(f"🔴 Deneme Sürümü: {randevu_toplam}/3 Randevu Kullanıldı")
    if randevu_toplam >= 3:
        st.sidebar.error("⚠️ Ücretsiz limit doldu! Pro Pakete geçin.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Pro Pakete Geç")
    st.sidebar.write("**₺499 / Ay** (Sınırsız Randevu, AI Asistan, Aidat & Kuşak)")
    st.sidebar.info("Ödeme için TR IBAN / QR ile transfer yapıp aktifleştirebilirsiniz.")
else:
    st.sidebar.success("🟢 PRO PAKET AKTİF")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Üye Yönetimi & Kuşak", 
    "📅 Randevu & Ders", 
    "💰 Aidat Takip Paneli", 
    "📱 WhatsApp Otomasyonu",
    "🤖 AI RingMaster Asistan"
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# --- TAB 1: ÜYE YÖNETİMİ & KUŞAK ---
with tab1:
    st.subheader("Yeni Sporcu Kaydı")
    with st.form("uye_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad_soyad = st.text_input("Sporcu Adı Soyadı")
            telefon = st.text_input("Telefon (Başında 90 ile örn: 905xxxxxxxxx)")
            brans = st.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col2:
            kusak = st.selectbox("Kuşak / Seviye", KUSAKLAR)
            aidat_tarihi = st.date_input("Son Aidat Ödeme Tarihi", datetime.date.today())
            aidat_durumu = st.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
        
        submit = st.form_submit_button("➕ Sporcuyu Kaydet")
        if submit:
            if ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu)
                st.success(f"{ad_soyad} başarıyla kaydedildi!")
                st.rerun()
            else:
                st.error("Lütfen ad soyad ve telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("📋 Kayıtlı Sporcular ve Kuşak Dereceleri")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            col_a.write(f"**{u_ad}** ({u_brans})")
            col_b.write(f"📞 {u_tel}")
            col_c.write(f"🥋 **{u_kusak}**")
            
            yeni_k = col_d.selectbox("Kuşak Güncelle", KUSAKLAR, index=KUSAKLAR.index(u_kusak) if u_kusak in KUSAKLAR else 0, key=f"k_{u_id}")
            if yeni_k != u_kusak:
                kusak_guncelle(u_id, yeni_k)
                st.success(f"{u_ad} kişisinin kuşağı güncellendi!")
                st.rerun()
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")

# --- TAB 2: RANDEVU TAKVİMİ ---
with tab2:
    st.subheader("Yeni Randevu / Antrenman Oluştur")
    uyeler = uyeleri_getir()
    
    if not IS_PRO and randevu_toplam >= 3:
        st.error("🔴 Ücretsiz deneme limitiniz (3 Randevu) doldu. Yeni randevu eklemek için Pro Pakete geçin.")
    else:
        if uyeler:
            uye_dict = {f"{u[1]} ({u[3]})": u[0] for u in uyeler}
            secilen_uye_str = st.selectbox("Sporcu Seç", list(uye_dict.keys()))
            secilen_id = uye_dict[secilen_uye_str]
            
            col_r1, col_r2 = st.columns(2)
            tarih = col_r1.date_input("Randevu Tarihi", datetime.date.today())
            saat = col_r2.time_input("Randevu Saati", datetime.time(18, 0))
            
            if st.button("📅 Randevuyu Onayla ve Kaydet"):
                randevu_ekle(secilen_id, str(tarih), str(saat))
                st.success("Randevu başarıyla eklendi!")
                st.rerun()
        else:
            st.warning("Randevu oluşturabilmek için önce 'Üye Yönetimi' sekmesinden üye eklemelisiniz.")

    st.markdown("---")
    st.subheader("📌 Planlanan Antrenmanlar")
    randevular = randevulari_getir()
    if randevular:
        for r in randevular:
            st.write(f"🗓️ **{r[3]} - {r[4]}** | 🥊 **{r[1]}** ({r[2]}) - Durum: `{r[5]}`")
    else:
        st.info("Planlanmış randevu bulunmuyor.")

# --- TAB 3: AİDAT TAKİP PANELSİ ---
with tab3:
    st.subheader("💰 Sporcu Aidat Durumları ve Kasası")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u
            col_m1, col_m2, col_m3, col_m4 = st.columns([2, 2, 2, 2])
            
            col_m1.write(f"**{u_ad}**")
            col_m2.write(f"🗓️ Son Tarih: **{u_aidat_t}**")
            
            durum_renk = "🟢 Ödendi" if u_aidat_d == "Ödendi" else "🔴 Ödeme Bekliyor"
            col_m3.write(f"Durum: **{durum_renk}**")
            
            yeni_aidat_d = col_m4.selectbox("Durum Değiştir", ["Ödendi", "Ödeme Bekliyor"], index=0 if u_aidat_d == "Ödendi" else 1, key=f"a_{u_id}")
            if yeni_aidat_d != u_aidat_d:
                aidat_durum_guncelle(u_id, yeni_aidat_d)
                st.success(f"{u_ad} aidat durumu güncellendi!")
                st.rerun()
    else:
        st.info("Sistemde henüz üye yok.")

# --- TAB 4: WHATSAPP OTOMASYONU ---
with tab4:
    st.subheader("📱 Tek Tıkla WhatsApp Mesaj Fırlatıcı")
    uyeler = uyeleri_getir()
    if uyeler:
        secilen_w_uye = st.selectbox("Mesaj Gönderilecek Sporcu", [f"{u[1]} ({u[3]})" for u in uyeler], key="wa_select")
        secilen_w_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_w_uye][0]
        u_data = [u for u in uyeler if u[0] == secilen_w_id][0]
        
        mesaj_tipi = st.radio("Mesaj Tipi Seçin", ["Randevu Hatırlatma", "Aidat Hatırlatma"])
        
        if mesaj_tipi == "Randevu Hatırlatma":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Boks Salonu antrenman randevunuz planlanmıştır. Lütfen vaktinde salonda olunuz. 🥊"
        else:
            varsayilan_mesaj = f"Merhaba {u_data[1]}, Salon aidat ödemenizin son günü {u_data[5]}'dir. Lütfen ödemenizi gerçekleştiriniz. Teşekkürler! 💰"
            
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        
        encoded_msg = urllib.parse.quote(mesaj_metni)
        wa_url = f"https://wa.me/{u_data[2]}?text={encoded_msg}"
        
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Üzerinden Gönder</button></a>', unsafe_allow_html=True)
    else:
        st.info("Kayıtlı üye bulunmuyor.")

# --- TAB 5: AI RİNGMASTER ASİSTAN ---
with tab5:
    st.subheader("🤖 AI RingMaster Koç & İdari Asistan")
    st.write("Dövüş sporları ve salon yönetimine özel yapay zeka asistanı. Tek tıkla antrenman programı veya ikna mesajı oluşturun!")
    
    ai_gorev = st.selectbox("AI Asistandan Ne İstiyorsunuz?", [
        "🥊 Özelleştirilmiş Antrenman Programı Yaz",
        "🥗 Sporcu Kilo Verme / Beslenme Tavsiyesi Hazırla",
        "🔥 Sporu Bırakan / Devamsız Üyeyi Geri Çağırma Mesajı"
    ])
    
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        ai_brans = st.selectbox("Branş / Seviye", ["Boks - Başlangıç", "Boks - Müsabık", "Kickboks - Orta Seviye", "Muay Thai", "Fitness"])
    with col_ai2:
        ai_hedef = st.text_input("Özel Not / Hedef (Örn: Patlayıcı güç, 5 kg verme)", "Patlayıcı güç ve kondisyon artırımı")
        
    if st.button("🚀 AI Yanıtı Üret"):
        with st.spinner("AI Antrenör düşünüyor ve programı hazırlıyor..."):
            if "Antrenman Programı" in ai_gorev:
                ai_cikti = f"""
### 🥊 {ai_brans} Akıllı Antrenman Programı
**Hedef:** {ai_hedef}

**1. Isınma & Mobilite (15 Dk):**
- 3 Raund İp Atlama (Raund aralarında 30 sn şınav/mekik)
- Omuz ve Kalça Dinamik Esnetme

**2. Teknik & Gölge Boksu (20 Dk):**
- 3 Raund Gölge Boksu (Direk - Kanca kombinasyonları)
- 3 Raund Torba Çalışması (Yüksek tempo patlayıcı vuruşlar)

**3. Lapa / Lapa ve Kondisyon (20 Dk):**
- 4 Raund Lapa / Sparring Mekaniği
- 100 Adet Patlayıcı Boks Şınavı & Plank (3 Set)

**4. Soğuma (5 Dk):** Statik esnetme.
                """
            elif "Beslenme" in ai_gorev:
                ai_cikti = f"""
### 🥗 Sporcu Performans & Beslenme Rehberi
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}

1. **Antrenman Öncesi (1.5 Saat Önce):** Karmaşık karbonhidrat (Yulaf + Muz veya Pirinç patlağı) ve su tüketimi.
2. **Antrenman Sonrası (İlk 45 Dk):** Yüksek protein (Tavuk/Yumurta/Lop Et) + Glikojen depoları için hafif meyve.
3. **Hidrasyon:** Antrenman boyunca en az 1.5 Litre elektrolitli su.
4. **Yasaklar:** Gazlı içecekler ve ağır hamur işleri tamamen kesilmeli!
                """
            else:
                ai_cikti = f"""
### 🔥 Üye İkna & Geri Çağırma WhatsApp Şablonu

"Selam Şampiyon! 🥊 Uzun zamandır salonda göremiyoruz seni, antrenman ritmin aksamasın. {ai_hedef} hedeflerimize ulaşmak için seni bu hafta ringde bekliyoruz. Unutma, en zor antrenman salona gelene kadardır! Bu akşamki seansa yazıyorum seni?"
                """
            
            st.success("AI Yanıtı Başarıyla Oluşturuldu!")
            st.markdown(ai_cikti)
            
            # Tek tıkla kopyalama veya WhatsApp'a atma hazırlığı
            enc_ai = urllib.parse.quote(ai_cikti)
            st.markdown(f'<a href="https://wa.me/?text={enc_ai}" target="_blank"><button style="background-color:#25D366;color:white;padding:8px 16px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 Bu AI Metnini WhatsApp'ta Paylaş</button></a>', unsafe_allow_html=True)
import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle
)

# Veritabanını Başlat
init_db()

st.set_page_config(page_title="RingMaster SaaS v3.5 - Global Sürüm", page_icon="🥊", layout="wide")

# Lisans Durumu Kontrolü (Free Trial: Max 3 Randevu)
randevu_toplam = randevu_sayisi()
IS_PRO = st.sidebar.checkbox("Pro Lisansı Aktifleştir", value=False)

st.sidebar.title("🥊 RingMaster SaaS v3.5")
if not IS_PRO:
    st.sidebar.warning(f"🔴 Deneme Sürümü: {randevu_toplam}/3 Randevu Kullanıldı")
    if randevu_toplam >= 3:
        st.sidebar.error("⚠️ Ücretsiz limit doldu! Pro Pakete geçin.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Pro Pakete Geç")
    st.sidebar.write("**₺499 / Ay** veya **$19 / Month** (SMS & WhatsApp Otomasyonu)")
    st.sidebar.info("Ödeme için TR IBAN / Stripe ile transfer yapıp aktifleştirebilirsiniz.")
else:
    st.sidebar.success("🟢 PRO PAKET AKTİF")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Üye Yönetimi & Kuşak", 
    "📅 Randevu & Ders", 
    "💰 Aidat Takip Paneli", 
    "📱 WhatsApp & SMS Otomasyonu",
    "🤖 AI RingMaster Asistan"
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# --- TAB 1: ÜYE YÖNETİMİ & KUŞAK ---
with tab1:
    st.subheader("Yeni Sporcu Kaydı")
    with st.form("uye_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad_soyad = st.text_input("Sporcu Adı Soyadı")
            telefon = st.text_input("Telefon (Ülke Kodu ile örn: +1234567890 veya 905xxxxxxxxx)")
            brans = st.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col2:
            kusak = st.selectbox("Kuşak / Seviye", KUSAKLAR)
            aidat_tarihi = st.date_input("Son Aidat Ödeme Tarihi", datetime.date.today())
            aidat_durumu = st.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
        
        submit = st.form_submit_button("➕ Sporcuyu Kaydet")
        if submit:
            if ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu)
                st.success(f"{ad_soyad} başarıyla kaydedildi!")
                st.rerun()
            else:
                st.error("Lütfen ad soyad ve telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("📋 Kayıtlı Sporcular ve Kuşak Dereceleri")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            col_a.write(f"**{u_ad}** ({u_brans})")
            col_b.write(f"📞 {u_tel}")
            col_c.write(f"🥋 **{u_kusak}**")
            
            yeni_k = col_d.selectbox("Kuşak Güncelle", KUSAKLAR, index=KUSAKLAR.index(u_kusak) if u_kusak in KUSAKLAR else 0, key=f"k_{u_id}")
            if yeni_k != u_kusak:
                kusak_guncelle(u_id, yeni_k)
                st.success(f"{u_ad} kişisinin kuşağı güncellendi!")
                st.rerun()
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")

# --- TAB 2: RANDEVU TAKVİMİ ---
with tab2:
    st.subheader("Yeni Randevu / Antrenman Oluştur")
    uyeler = uyeleri_getir()
    
    if not IS_PRO and randevu_toplam >= 3:
        st.error("🔴 Ücretsiz deneme limitiniz (3 Randevu) doldu. Yeni randevu eklemek için Pro Pakete geçin.")
    else:
        if uyeler:
            uye_dict = {f"{u[1]} ({u[3]})": u[0] for u in uyeler}
            secilen_uye_str = st.selectbox("Sporcu Seç", list(uye_dict.keys()))
            secilen_id = uye_dict[secilen_uye_str]
            
            col_r1, col_r2 = st.columns(2)
            tarih = col_r1.date_input("Randevu Tarihi", datetime.date.today())
            saat = col_r2.time_input("Randevu Saati", datetime.time(18, 0))
            
            if st.button("📅 Randevuyu Onayla ve Kaydet"):
                randevu_ekle(secilen_id, str(tarih), str(saat))
                st.success("Randevu başarıyla eklendi!")
                st.rerun()
        else:
            st.warning("Randevu oluşturabilmek için önce 'Üye Yönetimi' sekmesinden üye eklemelisiniz.")

    st.markdown("---")
    st.subheader("📌 Planlanan Antrenmanlar")
    randevular = randevulari_getir()
    if randevular:
        for r in randevular:
            st.write(f"🗓️ **{r[3]} - {r[4]}** | 🥊 **{r[1]}** ({r[2]}) - Durum: `{r[5]}`")
    else:
        st.info("Planlanmış randevu bulunmuyor.")

# --- TAB 3: AİDAT TAKİP PANELSİ ---
with tab3:
    st.subheader("💰 Sporcu Aidat Durumları ve Kasası")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u
            col_m1, col_m2, col_m3, col_m4 = st.columns([2, 2, 2, 2])
            
            col_m1.write(f"**{u_ad}**")
            col_m2.write(f"🗓️ Son Tarih: **{u_aidat_t}**")
            
            durum_renk = "🟢 Ödendi" if u_aidat_d == "Ödendi" else "🔴 Ödeme Bekliyor"
            col_m3.write(f"Durum: **{durum_renk}**")
            
            yeni_aidat_d = col_m4.selectbox("Durum Değiştir", ["Ödendi", "Ödeme Bekliyor"], index=0 if u_aidat_d == "Ödendi" else 1, key=f"a_{u_id}")
            if yeni_aidat_d != u_aidat_d:
                aidat_durum_guncelle(u_id, yeni_aidat_d)
                st.success(f"{u_ad} aidat durumu güncellendi!")
                st.rerun()
    else:
        st.info("Sistemde henüz üye yok.")

# --- TAB 4: WHATSAPP & SMS OTOMASYONU ---
with tab4:
    st.subheader("📱 WhatsApp & SMS Mesaj Fırlatıcı (Global / US Compatible)")
    uyeler = uyeleri_getir()
    if uyeler:
        secilen_w_uye = st.selectbox("Mesaj Gönderilecek Sporcu", [f"{u[1]} ({u[3]})" for u in uyeler], key="wa_select")
        secilen_w_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_w_uye][0]
        u_data = [u for u in uyeler if u[0] == secilen_w_id][0]
        
        mesaj_tipi = st.radio("Mesaj Tipi Seçin", ["Randevu Hatırlatma", "Aidat Hatırlatma"])
        
        if mesaj_tipi == "Randevu Hatırlatma":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Boks Salonu antrenman randevunuz planlanmıştır. Lütfen vaktinde salonda olunuz. 🥊"
        else:
            varsayilan_mesaj = f"Merhaba {u_data[1]}, Salon aidat ödemenizin son günü {u_data[5]}'dir. Lütfen ödemenizi gerçekleştiriniz. Teşekkürler! 💰"
            
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        
        encoded_msg = urllib.parse.quote(mesaj_metni)
        
        # WhatsApp URL
        wa_url = f"https://wa.me/{u_data[2]}?text={encoded_msg}"
        
        # SMS Protocol URL (ABD / Global SMS)
        sms_url = f"sms:{u_data[2]}?body={encoded_msg}"
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp İle Gönder</button></a>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown(f'<a href="{sms_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 Direct SMS / iMessage İle Gönder (US/Global)</button></a>', unsafe_allow_html=True)
    else:
        st.info("Kayıtlı üye bulunmuyor.")

# --- TAB 5: AI RİNGMASTER ASİSTAN ---
with tab5:
    st.subheader("🤖 AI RingMaster Koç & İdari Asistan")
    st.write("Dövüş sporları ve salon yönetimine özel yapay zeka asistanı. Tek tıkla antrenman programı veya ikna mesajı oluşturun!")
    
    ai_gorev = st.selectbox("AI Asistandan Ne İstiyorsunuz?", [
        "🥊 Özelleştirilled Dövüş / Antrenman Programı Yaz",
        "🥗 Sporcu Kilo Verme / Beslenme Tavsiyesi Hazırla",
        "🔥 Sporu Bırakan / Devamsız Üyeyi Geri Çağırma Mesajı"
    ])
    
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        ai_brans = st.selectbox("Branş / Seviye", ["Boks - Başlangıç", "Boks - Müsabık", "Kickboks - Orta Seviye", "Muay Thai", "Fitness"])
    with col_ai2:
        ai_hedef = st.text_input("Özel Not / Hedef (Örn: Patlayıcı güç, 5 kg verme)", "Patlayıcı güç ve kondisyon artırımı")
        
    if st.button("🚀 AI Yanıtı Üret"):
        with st.spinner("AI Antrenör düşünüyor ve programı hazırlıyor..."):
            if "Antrenman Programı" in ai_gorev:
                ai_cikti = f"""
### 🥊 {ai_brans} Akıllı Antrenman Programı
**Hedef:** {ai_hedef}

**1. Isınma & Mobilite (15 Dk):**
- 3 Raund İp Atlama (Raund aralarında 30 sn şınav/mekik)
- Omuz ve Kalça Dinamik Esnetme

**2. Teknik & Gölge Boksu (20 Dk):**
- 3 Raund Gölge Boksu (Direk - Kanca kombinasyonları)
- 3 Raund Torba Çalışması (Yüksek tempo patlayıcı vuruşlar)

**3. Lapa / Lapa ve Kondisyon (20 Dk):**
- 4 Raund Lapa / Sparring Mekaniği
- 100 Adet Patlayıcı Boks Şınavı & Plank (3 Set)

**4. Soğuma (5 Dk):** Statik esnetme.
                """
            elif "Beslenme" in ai_gorev:
                ai_cikti = f"""
### 🥗 Sporcu Performans & Beslenme Rehberi
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}

1. **Antrenman Öncesi (1.5 Saat Önce):** Karmaşık karbonhidrat (Yulaf + Muz veya Pirinç patlağı) ve su tüketimi.
2. **Antrenman Sonrası (İlk 45 Dk):** Yüksek protein (Tavuk/Yumurta/Lop Et) + Glikojen depoları için hafif meyve.
3. **Hidrasyon:** Antrenman boyunca en az 1.5 Litre elektrolitli su.
4. **Yasaklar:** Gazlı içecekler ve ağır hamur işleri tamamen kesilmeli!
                """
            else:
                ai_cikti = f"""
### 🔥 Üye İkna & Geri Çağırma WhatsApp / SMS Şablonu

"Selam Şampiyon! 🥊 Uzun zamandır salonda göremiyoruz seni, antrenman ritmin aksamasın. {ai_hedef} hedeflerimize ulaşmak için seni bu hafta ringde bekliyoruz. Unutma, en zor antrenman salona gelene kadardır! Bu akşamki seanse yazıyorum seni?"
                """
            
            st.success("AI Yanıtı Başarıyla Oluşturuldu!")
            st.markdown(ai_cikti)
            
            enc_ai = urllib.parse.quote(ai_cikti)
            col_share1, col_share2 = st.columns(2)
            with col_share1:
                st.markdown(f'<a href="https://wa.me/?text={enc_ai}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Paylaş</button></a>', unsafe_allow_html=True)
            with col_share2:
                st.markdown(f'<a href="sms:?body={enc_ai}"><button style="background-color:#007AFF;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS / iMessage Paylaş</button></a>', unsafe_allow_html=True)
import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle
)

# Veritabanını Başlat
init_db()

st.set_page_config(page_title="RingMaster SaaS v3.5 - Global Sürüm", page_icon="🥊", layout="wide")

# Lisans Durumu Kontrolü
randevu_toplam = randevu_sayisi()
IS_PRO = st.sidebar.checkbox("Pro Lisansı Aktifleştir", value=False)

st.sidebar.title("🥊 RingMaster SaaS v3.5")
if not IS_PRO:
    st.sidebar.warning(f"🔴 Deneme Sürümü: {randevu_toplam}/3 Randevu Kullanıldı")
    if randevu_toplam >= 3:
        st.sidebar.error("⚠️ Ücretsiz limit doldu! Pro Pakete geçin.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Pro Pakete Geç")
    st.sidebar.write("**₺499 / Ay** veya **$19 / Month** (Kuşak Sınav Takibi & Otomasyon)")
    st.sidebar.info("Ödeme için TR IBAN / Stripe ile transfer yapıp aktifleştirebilirsiniz.")
else:
    st.sidebar.success("🟢 PRO PAKET AKTİF")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Üye Yönetimi & Kuşak Sınavı", 
    "📅 Randevu & Ders", 
    "💰 Aidat Takip Paneli", 
    "📱 WhatsApp & SMS Otomasyonu",
    "🤖 AI RingMaster Asistan"
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# --- TAB 1: ÜYE YÖNETİMİ & KUŞAK SINAVI ---
with tab1:
    st.subheader("Yeni Sporcu Kaydı")
    with st.form("uye_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad_soyad = st.text_input("Sporcu Adı Soyadı")
            telefon = st.text_input("Telefon (Ülke Kodu ile örn: 905xxxxxxxxx)")
            brans = st.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col2:
            kusak = st.selectbox("Mevcut Kuşak / Seviye", KUSAKLAR)
            aidat_tarihi = st.date_input("Son Aidat Ödeme Tarihi", datetime.date.today())
            son_sinav_tarihi = st.date_input("Son Kuşak Sınavı / Başlangıç Tarihi", datetime.date.today())
            aidat_durumu = st.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
        
        submit = st.form_submit_button("➕ Sporcuyu Kaydet")
        if submit:
            if ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu, str(son_sinav_tarihi))
                st.success(f"{ad_soyad} başarıyla kaydedildi!")
                st.rerun()
            else:
                st.error("Lütfen ad soyad ve telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("🥋 Kuşak Derece Sınavı Uyarı & Takip Paneli")
    uyeler = uyeleri_getir()
    if uyeler:
        bugun = datetime.date.today()
        for u in uyeler:
            u_id = u[0]
            u_ad = u[1]
            u_tel = u[2]
            u_brans = u[3]
            u_kusak = u[4]
            u_sinav_t_str = u[7] if len(u) > 7 and u[7] else str(bugun)
            
            try:
                u_sinav_t = datetime.datetime.strptime(u_sinav_t_str, "%Y-%m-%d").date()
            except ValueError:
                u_sinav_t = bugun

            gecen_gun = (bugun - u_sinav_t).days
            
            # Sınav Uyarı Mantığı (Örn: 90 gün / 3 ay üzeri sınav vakti geldi)
            if gecen_gun >= 90:
                sinav_durumu = f"🔴 **Sınav Vakti Geldi!** ({gecen_gun} gündür aynı kuşakta)"
            elif gecen_gun >= 75:
                sinav_durumu = f"🟡 **Sınav Yaklaştı** ({gecen_gun} gün oldu)"
            else:
                sinav_durumu = f"🟢 **Normal** ({gecen_gun} gündür mevcut kuşakta)"

            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            col_a.write(f"**{u_ad}** ({u_brans})")
            col_b.write(f"🥋 **{u_kusak}**\n\n{sinav_durumu}")
            
            yeni_k = col_c.selectbox("Kuşak / Derece Yükselt", KUSAKLAR, index=KUSAKLAR.index(u_kusak) if u_kusak in KUSAKLAR else 0, key=f"k_{u_id}")
            if col_d.button("🥋 Sınavı Geçti / Yükselt", key=f"btn_k_{u_id}"):
                kusak_guncelle(u_id, yeni_k, str(bugun))
                st.success(f"🎉 {u_ad} yeni kuşağa geçti! Sınav tarihi güncellendi.")
                st.rerun()
            st.markdown("---")
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")

# --- TAB 2: RANDEVU TAKVİMİ ---
with tab2:
    st.subheader("Yeni Randevu / Antrenman Oluştur")
    uyeler = uyeleri_getir()
    
    if not IS_PRO and randevu_toplam >= 3:
        st.error("🔴 Ücretsiz deneme limitiniz (3 Randevu) doldu. Yeni randevu eklemek için Pro Pakete geçin.")
    else:
        if uyeler:
            uye_dict = {f"{u[1]} ({u[3]})": u[0] for u in uyeler}
            secilen_uye_str = st.selectbox("Sporcu Seç", list(uye_dict.keys()))
            secilen_id = uye_dict[secilen_uye_str]
            
            col_r1, col_r2 = st.columns(2)
            tarih = col_r1.date_input("Randevu Tarihi", datetime.date.today())
            saat = col_r2.time_input("Randevu Saati", datetime.time(18, 0))
            
            if st.button("📅 Randevuyu Onayla ve Kaydet"):
                randevu_ekle(secilen_id, str(tarih), str(saat))
                st.success("Randevu başarıyla eklendi!")
                st.rerun()
        else:
            st.warning("Randevu oluşturabilmek için önce 'Üye Yönetimi' sekmesinden üye eklemelisiniz.")

    st.markdown("---")
    st.subheader("📌 Planlanan Antrenmanlar")
    randevular = randevulari_getir()
    if randevular:
        for r in randevular:
            st.write(f"🗓️ **{r[3]} - {r[4]}** | 🥊 **{r[1]}** ({r[2]}) - Durum: `{r[5]}`")
    else:
        st.info("Planlanmış randevu bulunmuyor.")

# --- TAB 3: AİDAT TAKİP PANELSİ ---
with tab3:
    st.subheader("💰 Sporcu Aidat Durumları ve Kasası")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u[0], u[1], u[2], u[3], u[4], u[5], u[6]
            col_m1, col_m2, col_m3, col_m4 = st.columns([2, 2, 2, 2])
            
            col_m1.write(f"**{u_ad}**")
            col_m2.write(f"🗓️ Son Tarih: **{u_aidat_t}**")
            
            durum_renk = "🟢 Ödendi" if u_aidat_d == "Ödendi" else "🔴 Ödeme Bekliyor"
            col_m3.write(f"Durum: **{durum_renk}**")
            
            yeni_aidat_d = col_m4.selectbox("Durum Değiştir", ["Ödendi", "Ödeme Bekliyor"], index=0 if u_aidat_d == "Ödendi" else 1, key=f"a_{u_id}")
            if yeni_aidat_d != u_aidat_d:
                aidat_durum_guncelle(u_id, yeni_aidat_d)
                st.success(f"{u_ad} aidat durumu güncellendi!")
                st.rerun()
    else:
        st.info("Sistemde henüz üye yok.")

# --- TAB 4: WHATSAPP & SMS OTOMASYONU ---
with tab4:
    st.subheader("📱 WhatsApp & SMS Mesaj Fırlatıcı (Sınav / Aidat / Randevu)")
    uyeler = uyeleri_getir()
    if uyeler:
        secilen_w_uye = st.selectbox("Mesaj Gönderilecek Sporcu", [f"{u[1]} ({u[3]})" for u in uyeler], key="wa_select")
        secilen_w_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_w_uye][0]
        u_data = [u for u in uyeler if u[0] == secilen_w_id][0]
        
        mesaj_tipi = st.radio("Mesaj Tipi Seçin", ["Kuşak Sınavı Daveti", "Randevu Hatırlatma", "Aidat Hatırlatma"])
        
        if mesaj_tipi == "Kuşak Sınavı Daveti":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Salonu Kuşak Derece Sınavınız yaklaşmıştır. Lütfen sınav katılımı ve derece yükseltme antrenmanları için antrenörünüzle iletişime geçiniz. 🥋🥊"
        elif mesaj_tipi == "Randevu Hatırlatma":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Boks Salonu antrenman randevunuz planlanmıştır. Lütfen vaktinde salonda olunuz. 🥊"
        else:
            varsayilan_mesaj = f"Merhaba {u_data[1]}, Salon aidat ödemenizin son günü {u_data[5]}'dir. Lütfen ödemenizi gerçekleştiriniz. Teşekkürler! 💰"
            
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        
        encoded_msg = urllib.parse.quote(mesaj_metni)
        wa_url = f"https://wa.me/{u_data[2]}?text={encoded_msg}"
        sms_url = f"sms:{u_data[2]}?body={encoded_msg}"
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp İle Gönder</button></a>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown(f'<a href="{sms_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 Direct SMS / iMessage İle Gönder</button></a>', unsafe_allow_html=True)
    else:
        st.info("Kayıtlı üye bulunmuyor.")

# --- TAB 5: AI RİNGMASTER ASİSTAN ---
with tab5:
    st.subheader("🤖 AI RingMaster Koç & İdari Asistan")
    st.write("Dövüş sporları ve salon yönetimine özel yapay zeka asistanı. Tek tıkla antrenman programı veya ikna mesajı oluşturun!")
    
    ai_gorev = st.selectbox("AI Asistandan Ne İstiyorsunuz?", [
        "🥊 Özelleştirilmiş Dövüş / Antrenman Programı Yaz",
        "🥋 Kuşak Sınavı Hazırlık & Teknik Değerlendirme Metni",
        "🥗 Sporcu Kilo Verme / Beslenme Tavsiyesi Hazırla",
        "🔥 Sporu Bırakan / Devamsız Üyeyi Geri Çağırma Mesajı"
    ])
    
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        ai_brans = st.selectbox("Branş / Seviye", ["Boks - Başlangıç", "Boks - Müsabık", "Kickboks - Orta Seviye", "Muay Thai", "Fitness"])
    with col_ai2:
        ai_hedef = st.text_input("Özel Not / Hedef (Örn: Sınav hazırlığı, patlayıcı güç)", "Kuşak sınavı derece hazırlığı")
        
    if st.button("🚀 AI Yanıtı Üret"):
        with st.spinner("AI Antrenör düşünüyor ve metni hazırlıyor..."):
            if "Kuşak Sınavı" in ai_gorev:
                ai_cikti = f"""
### 🥋 Kuşak Derece Sınavı Hazırlık & Teknik Programı
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}

1. **Temel Teknik Sınavı:** Direk, kanca, aparkat kombinasyonlarının torba ve gard üzerindeki duruş hassasiyeti.
2. **Kondisyon & Dayanıklılık:** 3 Raund kesintisiz lapa çalışması + 50 Şınav / 50 Mekik.
3. **Mesafe ve Savunma:** Blok, gard, esneme ve kontra-atak refleks testi.
4. **Disiplin ve Etik:** Salon içi duruş ve sporcu etiği değerlendirmesi.
                """
            elif "Antrenman Programı" in ai_gorev:
                ai_cikti = f"""
### 🥊 {ai_brans} Akıllı Antrenman Programı
**Hedef:** {ai_hedef}

**1. Isınma & Mobilite (15 Dk):** 3 Raund İp Atlama & Dinamik Esnetme.
**2. Teknik & Gölge Boksu (20 Dk):** 3 Raund Gölge Boksu + 3 Raund Torba Çalışması.
**3. Lapa & Kondisyon (20 Dk):** 4 Raund Lapa / Sparring Mekaniği + Boks Şınavı.
**4. Soğuma (5 Dk):** Statik esnetme.
                """
            elif "Beslenme" in ai_gorev:
                ai_cikti = f"""
### 🥗 Sporcu Performans & Beslenme Rehberi
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}
- Antrenman öncesi karmaşık karbonhidrat, antrenman sonrası yüksek protein.
- Günlük en az 2.5 Litre hidrasyon.
                """
            else:
                ai_cikti = f"""
### 🔥 Üye İkna & Geri Çağırma Şablonu
"Selam Şampiyon! 🥊 Uzun zamandır salonda göremiyoruz seni. {ai_hedef} hedeflerimiz için seni bu hafta ringde bekliyoruz!"
                """
            
            st.success("AI Yanıtı Başarıyla Oluşturuldu!")
            st.markdown(ai_cikti)
            
            enc_ai = urllib.parse.quote(ai_cikti)
            col_share1, col_share2 = st.columns(2)
            with col_share1:
                st.markdown(f'<a href="https://wa.me/?text={enc_ai}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Paylaş</button></a>', unsafe_allow_html=True)
            with col_share2:
                st.markdown(f'<a href="sms:?body={enc_ai}"><button style="background-color:#007AFF;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS / iMessage Paylaş</button></a>', unsafe_allow_html=True)
import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle,
    deneme_ekle, denemeleri_getir, deneme_durum_guncelle
)

# Veritabanını Başlat
init_db()

st.set_page_config(page_title="RingMaster SaaS v3.5 - Global Sürüm", page_icon="🥊", layout="wide")

# Lisans Durumu Kontrolü
randevu_toplam = randevu_sayisi()
IS_PRO = st.sidebar.checkbox("Pro Lisansı Aktifleştir", value=False)

st.sidebar.title("🥊 RingMaster SaaS v3.5")
if not IS_PRO:
    st.sidebar.warning(f"🔴 Deneme Sürümü: {randevu_toplam}/3 Randevu Kullanıldı")
    if randevu_toplam >= 3:
        st.sidebar.error("⚠️ Ücretsiz limit doldu! Pro Pakete geçin.")
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Pro Pakete Geç")
    st.sidebar.write("**₺499 / Ay** veya **$19 / Month** (Deneme Dersi & AI Asistan)")
    st.sidebar.info("Ödeme için TR IBAN / Stripe ile transfer yapıp aktifleştirebilirsiniz.")
else:
    st.sidebar.success("🟢 PRO PAKET AKTİF")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🥊 Deneme Dersi (Lead)",
    "👤 Üye Yönetimi & Kuşak", 
    "📅 Randevu & Ders", 
    "💰 Aidat Takip Paneli", 
    "📱 WhatsApp & SMS Otomasyonu",
    "🤖 AI RingMaster Asistan"
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# --- TAB 1: DENEME DERSİ (LEAD YÖNETİMİ) ---
with tab1:
    st.subheader("🥊 Potansiyel Sporcu Deneme Dersi Kaydı")
    with st.form("deneme_form", clear_on_submit=True):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            d_ad = st.text_input("Aday Sporcu Adı Soyadı")
            d_tel = st.text_input("Telefon (örn: 905xxxxxxxxx)")
            d_brans = st.selectbox("İlgilendiği Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col_d2:
            d_tarih = st.date_input("Deneme Dersi Tarihi", datetime.date.today())
            d_saat = st.time_input("Deneme Dersi Saati", datetime.time(19, 0))
            d_not = st.text_input("Not (Örn: Daha önce boks yapmış, kilo vermek istiyor)", "")
        
        submit_d = st.form_submit_button("➕ Deneme Dersi Randevusu Oluştur")
        if submit_d:
            if d_ad and d_tel:
                deneme_ekle(d_ad, d_tel, d_brans, str(d_tarih), str(d_saat), d_not)
                st.success(f"🎉 {d_ad} için deneme dersi randevusu kaydoldu!")
                st.rerun()
            else:
                st.error("Lütfen Ad Soyad ve Telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("📌 Planlanan Deneme Dersleri & Dönüşüm Paneli")
    denemeler = denemeleri_getir()
    if denemeler:
        for den in denemeler:
            den_id, den_ad, den_tel, den_brans, den_tarih, den_saat, den_durum, den_not = den
            col_x1, col_x2, col_x3, col_x4 = st.columns([2, 2, 2, 2])
            
            col_x1.write(f"**{den_ad}** ({den_brans})\n\n📞 {den_tel}")
            col_x2.write(f"🗓️ **{den_tarih} - {den_saat}**\n\n📝 Not: _{den_not}_")
            
            # Durum Güncelle
            yeni_d_durum = col_x3.selectbox("Katılım Durumu", ["Bekliyor", "Derse Geldi 🟢", "Gelmedi 🔴"], index=["Bekliyor", "Derse Geldi 🟢", "Gelmedi 🔴"].index(den_durum) if den_durum in ["Bekliyor", "Derse Geldi 🟢", "Gelmedi 🔴"] else 0, key=f"dd_{den_id}")
            if yeni_d_durum != den_durum:
                deneme_durum_guncelle(den_id, yeni_d_durum)
                st.rerun()
                
            # Tek Tıkla Asil Üyeye Dönüştür
            if col_x4.button("🏆 Asil Üye Yap & Kaydet", key=f"btn_convert_{den_id}"):
                bugun_str = str(datetime.date.today())
                uye_ekle(den_ad, den_tel, den_brans, "Beyaz Kuşak / Başlangıç", bugun_str, "Ödeme Bekliyor", bugun_str)
                deneme_durum_guncelle(den_id, "Kayıt Oldu 🏆")
                st.success(f"🔥 TEBRİKLER! {den_ad} başarıyla Asil Üye yapıldı ve Üye Listesine aktarıldı!")
                st.rerun()
            st.markdown("---")
    else:
        st.info("Henüz planlanmış deneme dersi bulunmuyor.")

# --- TAB 2: ÜYE YÖNETİMİ & KUŞAK SINAVI ---
with tab2:
    st.subheader("Yeni Sporcu Kaydı (Manuel)")
    with st.form("uye_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ad_soyad = st.text_input("Sporcu Adı Soyadı")
            telefon = st.text_input("Telefon (Ülke Kodu ile örn: 905xxxxxxxxx)")
            brans = st.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness / Özel Ders"])
        with col2:
            kusak = st.selectbox("Mevcut Kuşak / Seviye", KUSAKLAR)
            aidat_tarihi = st.date_input("Son Aidat Ödeme Tarihi", datetime.date.today())
            son_sinav_tarihi = st.date_input("Son Kuşak Sınavı / Başlangıç Tarihi", datetime.date.today())
            aidat_durumu = st.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
        
        submit = st.form_submit_button("➕ Sporcuyu Kaydet")
        if submit:
            if ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu, str(son_sinav_tarihi))
                st.success(f"{ad_soyad} başarıyla kaydedildi!")
                st.rerun()
            else:
                st.error("Lütfen ad soyad ve telefon alanlarını doldurun.")

    st.markdown("---")
    st.subheader("🥋 Kuşak Derece Sınavı Uyarı & Takip Paneli")
    uyeler = uyeleri_getir()
    if uyeler:
        bugun = datetime.date.today()
        for u in uyeler:
            u_id = u[0]
            u_ad = u[1]
            u_tel = u[2]
            u_brans = u[3]
            u_kusak = u[4]
            u_sinav_t_str = u[7] if len(u) > 7 and u[7] else str(bugun)
            
            try:
                u_sinav_t = datetime.datetime.strptime(u_sinav_t_str, "%Y-%m-%d").date()
            except ValueError:
                u_sinav_t = bugun

            gecen_gun = (bugun - u_sinav_t).days
            
            if gecen_gun >= 90:
                sinav_durumu = f"🔴 **Sınav Vakti Geldi!** ({gecen_gun} gündür aynı kuşakta)"
            elif gecen_gun >= 75:
                sinav_durumu = f"🟡 **Sınav Yaklaştı** ({gecen_gun} gün oldu)"
            else:
                sinav_durumu = f"🟢 **Normal** ({gecen_gun} gündür mevcut kuşakta)"

            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            col_a.write(f"**{u_ad}** ({u_brans})")
            col_b.write(f"🥋 **{u_kusak}**\n\n{sinav_durumu}")
            
            yeni_k = col_c.selectbox("Kuşak / Derece Yükselt", KUSAKLAR, index=KUSAKLAR.index(u_kusak) if u_kusak in KUSAKLAR else 0, key=f"k_{u_id}")
            if col_d.button("🥋 Sınavı Geçti / Yükselt", key=f"btn_k_{u_id}"):
                kusak_guncelle(u_id, yeni_k, str(bugun))
                st.success(f"🎉 {u_ad} yeni kuşağa geçti! Sınav tarihi güncellendi.")
                st.rerun()
            st.markdown("---")
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")

# --- TAB 3: RANDEVU TAKVİMİ ---
with tab3:
    st.subheader("Yeni Randevu / Antrenman Oluştur")
    uyeler = uyeleri_getir()
    
    if not IS_PRO and randevu_toplam >= 3:
        st.error("🔴 Ücretsiz deneme limitiniz (3 Randevu) doldu. Yeni randevu eklemek için Pro Pakete geçin.")
    else:
        if uyeler:
            uye_dict = {f"{u[1]} ({u[3]})": u[0] for u in uyeler}
            secilen_uye_str = st.selectbox("Sporcu Seç", list(uye_dict.keys()))
            secilen_id = uye_dict[secilen_uye_str]
            
            col_r1, col_r2 = st.columns(2)
            tarih = col_r1.date_input("Randevu Tarihi", datetime.date.today())
            saat = col_r2.time_input("Randevu Saati", datetime.time(18, 0))
            
            if st.button("📅 Randevuyu Onayla ve Kaydet"):
                randevu_ekle(secilen_id, str(tarih), str(saat))
                st.success("Randevu başarıyla eklendi!")
                st.rerun()
        else:
            st.warning("Randevu oluşturabilmek için önce 'Üye Yönetimi' sekmesinden üye eklemelisiniz.")

    st.markdown("---")
    st.subheader("📌 Planlanan Antrenmanlar")
    randevular = randevulari_getir()
    if randevular:
        for r in randevular:
            st.write(f"🗓️ **{r[3]} - {r[4]}** | 🥊 **{r[1]}** ({r[2]}) - Durum: `{r[5]}`")
    else:
        st.info("Planlanmış randevu bulunmuyor.")

# --- TAB 4: AİDAT TAKİP PANELSİ ---
with tab4:
    st.subheader("💰 Sporcu Aidat Durumları ve Kasası")
    uyeler = uyeleri_getir()
    if uyeler:
        for u in uyeler:
            u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d = u[0], u[1], u[2], u[3], u[4], u[5], u[6]
            col_m1, col_m2, col_m3, col_m4 = st.columns([2, 2, 2, 2])
            
            col_m1.write(f"**{u_ad}**")
            col_m2.write(f"🗓️ Son Tarih: **{u_aidat_t}**")
            
            durum_renk = "🟢 Ödendi" if u_aidat_d == "Ödendi" else "🔴 Ödeme Bekliyor"
            col_m3.write(f"Durum: **{durum_renk}**")
            
            yeni_aidat_d = col_m4.selectbox("Durum Değiştir", ["Ödendi", "Ödeme Bekliyor"], index=0 if u_aidat_d == "Ödendi" else 1, key=f"a_{u_id}")
            if yeni_aidat_d != u_aidat_d:
                aidat_durum_guncelle(u_id, yeni_aidat_d)
                st.success(f"{u_ad} aidat durumu güncellendi!")
                st.rerun()
    else:
        st.info("Sistemde henüz üye yok.")

# --- TAB 5: WHATSAPP & SMS OTOMASYONU ---
with tab5:
    st.subheader("📱 WhatsApp & SMS Mesaj Fırlatıcı")
    uyeler = uyeleri_getir()
    denemeler = denemeleri_getir()
    
    mesaj_hedef = st.radio("Mesaj Alıcısı", ["Kayıtlı Sporcular", "Deneme Dersi Adayları"])
    
    if mesaj_hedef == "Deneme Dersi Adayları" and denemeler:
        secilen_d_str = st.selectbox("Aday Seç", [f"{d[1]} ({d[3]} - {d[4]} {d[5]})" for d in denemeler])
        d_data = [d for d in denemeler if f"{d[1]} ({d[3]} - {d[4]} {d[5]})" == secilen_d_str][0]
        
        varsayilan_mesaj = f"Merhaba {d_data[1]}, RingMaster Salonu ücretsiz deneme dersi randevunuz {d_data[4]} saat {d_data[5]} olarak planlanmıştır. Havlu ve rahat spor kıyafetlerinizle salonda olmanızı bekliyoruz! 🥊"
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        
        encoded_msg = urllib.parse.quote(mesaj_metni)
        wa_url = f"https://wa.me/{d_data[2]}?text={encoded_msg}"
        sms_url = f"sms:{d_data[2]}?body={encoded_msg}"
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp İle Gönder</button></a>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown(f'<a href="{sms_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 Direct SMS / iMessage İle Gönder</button></a>', unsafe_allow_html=True)

    elif mesaj_hedef == "Kayıtlı Sporcular" and uyeler:
        secilen_w_uye = st.selectbox("Sporcu Seç", [f"{u[1]} ({u[3]})" for u in uyeler], key="wa_select")
        secilen_w_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_w_uye][0]
        u_data = [u for u in uyeler if u[0] == secilen_w_id][0]
        
        mesaj_tipi = st.radio("Mesaj Tipi Seçin", ["Kuşak Sınavı Daveti", "Randevu Hatırlatma", "Aidat Hatırlatma"])
        
        if mesaj_tipi == "Kuşak Sınavı Daveti":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Salonu Kuşak Derece Sınavınız yaklaşmıştır. Lütfen antrenörünüzle iletişime geçiniz. 🥋🥊"
        elif mesaj_tipi == "Randevu Hatırlatma":
            varsayilan_mesaj = f"Merhaba {u_data[1]}, RingMaster Boks Salonu antrenman randevunuz planlanmıştır. Lütfen vaktinde salonda olunuz. 🥊"
        else:
            varsayilan_mesaj = f"Merhaba {u_data[1]}, Salon aidat ödemenizin son günü {u_data[5]}'dir. Lütfen ödemenizi gerçekleştiriniz. Teşekkürler! 💰"
            
        mesaj_metni = st.text_area("Mesaj Metni", varsayilan_mesaj)
        encoded_msg = urllib.parse.quote(mesaj_metni)
        wa_url = f"https://wa.me/{u_data[2]}?text={encoded_msg}"
        sms_url = f"sms:{u_data[2]}?body={encoded_msg}"
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp İle Gönder</button></a>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown(f'<a href="{sms_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 Direct SMS / iMessage İle Gönder</button></a>', unsafe_allow_html=True)
    else:
        st.info("Gönderilecek veri bulunmuyor.")

# --- TAB 6: AI RİNGMASTER ASİSTAN ---
with tab6:
    st.subheader("🤖 AI RingMaster Koç & İdari Asistan")
    st.write("Dövüş sporları ve salon yönetimine özel yapay zeka asistanı. Tek tıkla antrenman programı veya ikna mesajı oluşturun!")
    
    ai_gorev = st.selectbox("AI Asistandan Ne İstiyorsunuz?", [
        "🥊 Özelleştirilmiş Dövüş / Antrenman Programı Yaz",
        "🥋 Kuşak Sınavı Hazırlık & Teknik Değerlendirme Metni",
        "🥗 Sporcu Kilo Verme / Beslenme Tavsiyesi Hazırla",
        "🔥 Deneme Dersi Sonrası Üyeliğe İkna Mesajı Hazırla"
    ])
    
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        ai_brans = st.selectbox("Branş / Seviye", ["Boks - Başlangıç", "Boks - Müsabık", "Kickboks - Orta Seviye", "Muay Thai", "Fitness"])
    with col_ai2:
        ai_hedef = st.text_input("Özel Not / Hedef (Örn: Sınav hazırlığı, patlayıcı güç)", "Deneme dersi sonrası abonelik satışı")
        
    if st.button("🚀 AI Yanıtı Üret"):
        with st.spinner("AI Antrenör düşünüyor ve metni hazırlıyor..."):
            if "Deneme Dersi" in ai_gorev:
                ai_cikti = f"""
### 🔥 Deneme Dersi Sonrası İkna & Satış Mesajı
"Harika bir antrenmandı Şampiyon! 🥊 Bugün gösterdiğin azim müthişti. {ai_hedef} hedeflerine ulaşmak için doğru yerdesin. Bu haftaya özel kontenjanımız dolmadan resmi kaydını tamamlayalım mı? Seni kadromuzda görmek isteriz!"
                """
            elif "Kuşak Sınavı" in ai_gorev:
                ai_cikti = f"""
### 🥋 Kuşak Derece Sınavı Hazırlık & Teknik Programı
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}
1. Temel Teknik Sınavı: Direk, kanca, aparkat hassasiyet testi.
2. Kondisyon & Dayanıklılık: 3 Raund lapa çalışması + 50 Şınav.
                """
            elif "Antrenman Programı" in ai_gorev:
                ai_cikti = f"""
### 🥊 {ai_brans} Akıllı Antrenman Programı
**Hedef:** {ai_hedef}
**1. Isınma (15 Dk):** 3 Raund İp Atlama & Dinamik Esnetme.
**2. Teknik (20 Dk):** Gölge Boksu & Torba Çalışması.
**3. Kondisyon (20 Dk):** Lapa Çalışması & Boks Şınavı.
                """
            else:
                ai_cikti = f"""
### 🥗 Sporcu Performans & Beslenme Rehberi
**Branş:** {ai_brans} | **Hedef:** {ai_hedef}
- Antrenman öncesi karmaşık karbonhidrat, antrenman sonrası yüksek protein.
                """
            
            st.success("AI Yanıtı Başarıyla Oluşturuldu!")
            st.markdown(ai_cikti)
            
            enc_ai = urllib.parse.quote(ai_cikti)
            col_share1, col_share2 = st.columns(2)
            with col_share1:
                st.markdown(f'<a href="https://wa.me/?text={enc_ai}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Paylaş</button></a>', unsafe_allow_html=True)
            with col_share2:
                st.markdown(f'<a href="sms:?body={enc_ai}"><button style="background-color:#007AFF;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS / iMessage Paylaş</button></a>', unsafe_allow_html=True)
