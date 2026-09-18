import streamlit as st
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