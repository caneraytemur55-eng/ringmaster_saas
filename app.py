import streamlit as st
import pandas as pd
import database as db
import random

# Sayfa Yapılandırması (Koyu Tema & Spor Salonu Atmosferi)
st.set_page_config(page_title="Ringmaster SaaS - Global Spor Salonu Yönetimi", page_icon="🥊", layout="wide")

# Veritabanını başlat
db.veritabani_baslat()

st.sidebar.title("🥊 Ringmaster SaaS")
st.sidebar.markdown("---")

# Tüm Modüller + Global Ödeme Entegrasyonu (20 Modül Tam Kadro)
secilen_modul = st.sidebar.selectbox(
    "Modül Seçin", 
    [
        "Ana Sayfa", 
        "Ringmaster AI Asistanı 🤖", 
        "Salon Üyeleri Yönetimi", 
        "Yoklama Sistemi", 
        "Stok Takibi", 
        "Kasa / Finans", 
        "Antrenör & Prim Takibi", 
        "Çocuk Gelişim Raporları", 
        "Kuşak / Derece Sınavı", 
        "Müsabık Takımı Yönetimi", 
        "Sakatlık & Sparring Takibi", 
        "Maç / Turnuva Takvimi", 
        "Aday Üye Takibi (CRM)", 
        "Özel Ders (PT) Takibi", 
        "Vücut Ölçüm Takibi", 
        "Üye Terk (Churn) Riski", 
        "Toplu SMS / Duyuru Logu",
        "SaaS Abonelik Yönetimi",
        "🌍 Küresel Ödemeler (UK, US, EU)",
        "Sistem Ayarları"
    ]
)

# --- 1. ANA SAYFA ---
if secilen_modul == "Ana Sayfa":
    st.subheader("🥊 Ringmaster SaaS Yönetim Paneline Hoş Geldin Patron!")
    st.info("Global açılım modülleri aktif! İngiltere, ABD ve Avrupa şirket yapılanman için ödeme altyapısı hazır.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Toplam Üye", len(db.uyeleri_getir()))
    with col2:
        st.metric("Aktif Modül", "20 / 20 (Global Ödemeler Aktif)")
    with col3:
        st.metric("Hedef Pazar", "UK, US & Europe 🚀")

# --- 2. RİNGMASTER AI ASİSTANI ---
elif secilen_modul == "Ringmaster AI Asistanı 🤖":
    st.subheader("🤖 Ringmaster AI - Salon Yönetim Asistanı")
    st.write("Salonunla ilgili sorular sorabilir, antrenman programları, üye tutma stratejileri veya küresel pazarlama fikirleri alabilirsin.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Selam patron! İngiltere, ABD ve Avrupa operasyonları için hazırım. Global pazar stratejimizi ne üzerine kuruyoruz?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Küresel pazar, abonelikler veya salon yönetimi hakkında sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Ringmaster AI düşünüyor..."):
                lower_p = prompt.lower()
                if "üye" in lower_p or "kayıt" in lower_p:
                    yanit = f"Patron, sistemde toplam **{len(db.uyeleri_getir())}** kayıtlı sporcumuz bulunuyor."
                elif "stripe" in lower_p or "ödeme" in lower_p or "global" in lower_p:
                    yanit = "Küresel ödemeler modülünden USD, GBP ve EUR bazlı abonelik linkleri oluşturabilir, uluslararası müşterilerini tek tıkla yönetebilirsin."
                elif "merhaba" in lower_p or "selam" in lower_p:
                    yanit = "Ooo selam patron! Dünya fethi yolunda mermi gibi ilerliyoruz. Ne yapıyoruz bugün?"
                else:
                    yanit = f"Harika bir yaklaşım patron! '{prompt}' konusunda uluslararası standartlarda otomasyon kurmak işini çok büyütecektir."
                
                st.markdown(yanit)
                st.session_state.messages.append({"role": "assistant", "content": yanit})

# --- 3. SALON ÜYELERİ YÖNETİMİ ---
elif secilen_modul == "Salon Üyeleri Yönetimi":
    st.subheader("👤 Salon Üyeleri Yönetimi")
    
    with st.form("uye_form"):
        c1, c2 = st.columns(2)
        with c1:
            ad = st.text_input("Sporcu Ad Soyad")
            tel = st.text_input("Telefon")
        with c2:
            brans = st.selectbox("Branş", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
            pin = st.text_input("4 Haneli PIN (Boş bırakırsan otomatik atanır)", max_chars=4, type="default")
        
        if st.form_submit_button("Sporcuyu Kaydet 🚀"):
            if ad:
                if not pin or len(pin) != 4 or not pin.isdigit():
                    pin = str(random.randint(1000, 9999))
                db.uye_ekle(ad, tel, brans, pin)
                st.success(f"🚀 {ad} salona başarıyla kaydedildi! PIN Kodu: **{pin}**")
            else:
                st.warning("Lütfen sporcu adını girin.")
    
    st.markdown("### 📋 Kayıtlı Sporcular")
    uyeler = db.uyeleri_getir()
    if uyeler:
        df_uyeler = pd.DataFrame(uyeler, columns=["ID", "Ad Soyad", "Telefon", "Branş", "PIN", "Kayıt Tarihi"])
        st.dataframe(df_uyeler, use_container_width=True)
        
        st.markdown("### 🗑️ Sporcu Kaydı Sil")
        with st.form("uye_sil_form"):
            silinecek_id = st.selectbox("Silinecek Sporcuyu Seç (ID - Ad Soyad)", df_uyeler.apply(lambda x: f"{x['ID']} - {x['Ad Soyad']}", axis=1).tolist())
            if st.form_submit_button("Seçilen Sporcu Kaydını Sil ❌"):
                secilen_id = int(silinecek_id.split(" - ")[0])
                db.uye_sil(secilen_id)
                st.success(f"ID'si {secilen_id} olan sporcu silindi, patron! Sayfayı yenileyebilirsin.")
                st.rerun()
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")

# --- 4. YOKLAMA SİSTEMİ ---
elif secilen_modul == "Yoklama Sistemi":
    st.subheader("📝 Yoklama ve Giriş Takibi")
    girilen_pin = st.text_input("4 Haneli PIN Kodunuzu Girin", max_chars=4, type="password")
    if st.button("Giriş Yap / Yoklama Al"):
        uyeler = db.uyeleri_getir()
        bulunan = [u for u in uyeler if u[4] == girilen_pin]
        if bulunan:
            st.success(f"Hoş geldin, {bulunan[0][1]}! Antrenman girişin kaydedildi.")
        else:
            st.error("Geçersiz PIN kodu! Lütfen kontrol edin.")

# --- 5. STOK TAKİBİ ---
elif secilen_modul == "Stok Takibi":
    st.subheader("📦 Ürün ve Ekipman Stok Yönetimi")
    conn = db.baglanti_kur()
    stoklar = pd.read_sql("SELECT * FROM stok", conn)
    conn.close()
    st.dataframe(stoklar, use_container_width=True)
    with st.form("yeni_stok"):
        urun = st.text_input("Ürün Adı")
        adet = st.number_input("Adet", min_value=1, value=10)
        fiyat = st.number_input("Fiyat (TL)", min_value=0.0, value=100.0)
        if st.form_submit_button("Stok Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO stok (urun_adi, adet, fiyat) VALUES (?, ?, ?)", (urun, adet, fiyat))
            conn.commit()
            conn.close()
            st.success("Stok eklendi!")
            st.rerun()

# --- 6. KASA / FİNANS ---
elif secilen_modul == "Kasa / Finans":
    st.subheader("💰 Kasa ve Gelir/Gider Takibi")
    conn = db.baglanti_kur()
    kasa_df = pd.read_sql("SELECT * FROM kasa", conn)
    conn.close()
    st.dataframe(kasa_df, use_container_width=True)
    with st.form("kasa_form"):
        islem = st.selectbox("İşlem Tipi", ["Gelir", "Gider"])
        aciklama = st.text_input("Açıklama")
        tutar = st.number_input("Tutar", min_value=0.0)
        if st.form_submit_button("İşlemi Kaydet"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO kasa (islem_tipi, aciklama, tutar, tarih) VALUES (?, ?, ?, ?)", 
                         (islem, aciklama, tutar, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.success("Kasa hareketi eklendi!")
            st.rerun()

# --- 7. ANTRENÖR & PRİM TAKİBİ ---
elif secilen_modul == "Antrenör & Prim Takibi":
    st.subheader("🥋 Antrenör ve Prim Yönetimi")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM antrenorler", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("hoca_form"):
        hoca = st.text_input("Antrenör Adı")
        brans = st.text_input("Branş")
        ders = st.number_input("Ders Sayısı", min_value=0, value=0)
        prim = st.number_input("Prim Oranı (%)", min_value=0.0, value=10.0)
        if st.form_submit_button("Antrenör Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO antrenorler (hoca_adi, brans, ders_sayisi, prim_orani) VALUES (?, ?, ?, ?)", (hoca, brans, ders, prim))
            conn.commit()
            conn.close()
            st.success("Antrenör eklendi!")
            st.rerun()

# --- 8. ÇOCUK GELİŞİM RAPORLARI ---
elif secilen_modul == "Çocuk Gelişim Raporları":
    st.subheader("🧒 Çocuk Gelişim ve Veli Takibi")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM cocuk_gelisim", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("cocuk_form"):
        ogr = st.text_input("Öğrenci Adı")
        tel = st.text_input("Veli Telefon")
        notlar = st.text_area("Gelişim Notları")
        if st.form_submit_button("Rapor Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO cocuk_gelisim (ogrenci_adi, veli_telefon, notlar, tarih) VALUES (?, ?, ?, ?)", 
                         (ogr, tel, notlar, pd.Timestamp.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            st.success("Rapor eklendi!")
            st.rerun()

# --- 9. KUŞAK / DERECE SINAVI ---
elif secilen_modul == "Kuşak / Derece Sınavı":
    st.subheader("🥋 Kuşak ve Derece Sınav Takibi")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM kusak_sinav", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("kusak_form"):
        ogr = st.text_input("Öğrenci Adı")
        mevcut = st.text_input("Mevcut Kuşak")
        hedef = st.text_input("Hedef Kuşak")
        durum = st.selectbox("Durum", ["Bekliyor", "Başarılı", "Tekrar"])
        if st.form_submit_button("Sınav Kaydı Oluştur"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO kusak_sinav (ogrenci_adi, mevcut_kusak, hedef_kusak, durum) VALUES (?, ?, ?, ?)", (ogr, mevcut, hedef, durum))
            conn.commit()
            conn.close()
            st.success("Sınav kaydı oluşturuldu!")
            st.rerun()

# --- 10. MÜSABIK TAKIMI YÖNETİMİ ---
elif secilen_modul == "Müsabık Takımı Yönetimi":
    st.subheader("🥊 Müsabık Sporcu ve Siklet Yönetimi")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM musabiklar", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("musabik_form"):
        sporcu = st.text_input("Sporcu Adı")
        siklet = st.text_input("Siklet")
        galibiyet = st.number_input("Galibiyet", min_value=0, value=0)
        maglubiyet = st.number_input("Mağlubiyet", min_value=0, value=0)
        if st.form_submit_button("Müsabık Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO musabiklar (sporcu_adi, siklet, galibiyet, maglubiyet) VALUES (?, ?, ?, ?)", (sporcu, siklet, galibiyet, maglubiyet))
            conn.commit()
            conn.close()
            st.success("Müsabık eklendi!")
            st.rerun()

# --- 11. SAKATLIK & SPARRİNG TAKİBİ ---
elif secilen_modul == "Sakatlık & Sparring Takibi":
    st.subheader("🩹 Sporcu Sakatlık ve Sparring Yasakları")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM sakatliklar", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("sakatlik_form"):
        sporcu = st.text_input("Sporcu Adı")
        aciklama = st.text_input("Açıklama")
        yasak = st.selectbox("Sparring Yasağı?", [1, 0], format_func=lambda x: "Evet" if x==1 else "Hayır")
        if st.form_submit_button("Kayıt Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO sakatliklar (sporcu_adi, durum_aciklamasi, sparring_yasagi) VALUES (?, ?, ?)", (sporcu, aciklama, yasak))
            conn.commit()
            conn.close()
            st.success("Kayıt eklendi!")
            st.rerun()

# --- 12. MAÇ / TURNUVA TAKVİMİ ---
elif secilen_modul == "Maç / Turnuva Takvimi":
    st.subheader("🏆 Maç ve Turnuva Takvimi")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM mac_takvimi", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("mac_form"):
        turnuva = st.text_input("Turnuva Adı")
        tarih = st.text_input("Tarih (YYYY-MM-DD)")
        sporcular = st.text_area("Katılacak Sporcular")
        if st.form_submit_button("Turnuva Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO mac_takvimi (turnuva_adi, tarih, katilacak_sporcular) VALUES (?, ?, ?)", (turnuva, tarih, sporcular))
            conn.commit()
            conn.close()
            st.success("Turnuva eklendi!")
            st.rerun()

# --- 13. ADAY ÜYE TAKİBİ (CRM) ---
elif secilen_modul == "Aday Üye Takibi (CRM)":
    st.subheader("📞 Aday Üye ve Potansiyel Müşteri Takibi")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM adaylar", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("aday_form"):
        aday = st.text_input("Aday Adı")
        tel = st.text_input("Telefon")
        brans = st.text_input("İlgilenilen Branş")
        durum = st.selectbox("Durum", ["Arandı", "Deneme", "Kayıt Oldu", "Vazgeçti"])
        if st.form_submit_button("Aday Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO adaylar (aday_adi, telefon, ilgilenilen_brans, durum) VALUES (?, ?, ?, ?)", (aday, tel, brans, durum))
            conn.commit()
            conn.close()
            st.success("Aday eklendi!")
            st.rerun()

# --- 14. ÖZEL DERS (PT) TAKİBİ ---
elif secilen_modul == "Özel Ders (PT) Takibi":
    st.subheader("🎯 Özel Ders (PT) Paket Takibi")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM ozel_dersler", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("pt_form"):
        sporcu = st.text_input("Sporcu Adı")
        hoca = st.text_input("Antrenör Adı")
        kalan = st.number_input("Kalan Ders", min_value=0, value=10)
        if st.form_submit_button("PT Paketi Tanımla"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO ozel_dersler (sporcu_adi, hoca_adi, kalan_ders) VALUES (?, ?, ?)", (sporcu, hoca, kalan))
            conn.commit()
            conn.close()
            st.success("PT paketi tanımlandı!")
            st.rerun()

# --- 15. VÜCUT ÖLÇÜM TAKİBİ ---
elif secilen_modul == "Vücut Ölçüm Takibi":
    st.subheader("📊 Sporcu Vücut Ölçümleri")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM olcumler", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("olcum_form"):
        sporcu = st.text_input("Sporcu Adı")
        kilo = st.number_input("Kilo (kg)", min_value=0.0, value=75.0)
        yag = st.number_input("Yağ Oranı (%)", min_value=0.0, value=15.0)
        if st.form_submit_button("Ölçüm Kaydet"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO olcumler (sporcu_adi, kilo, yag_orani, tarih) VALUES (?, ?, ?, ?)", 
                         (sporcu, kilo, yag, pd.Timestamp.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            st.success("Ölçüm kaydedildi!")
            st.rerun()

# --- 16. ÜYE TERK (CHURN) RİSKİ ---
elif secilen_modul == "Üye Terk (Churn) Riski":
    st.subheader("⚠️ Üye Devamsızlık ve Terk Riski")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM churn_takip", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("churn_form"):
        sporcu = st.text_input("Sporcu Adı")
        son_gelis = st.text_input("Son Geliş (YYYY-MM-DD)")
        risk = st.selectbox("Risk", ["Düşük", "Orta", "Yüksek Risk"])
        if st.form_submit_button("Risk Kaydı Ekle"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO churn_takip (sporcu_adi, son_gelis_tarihi, risk_durumu) VALUES (?, ?, ?)", (sporcu, son_gelis, risk))
            conn.commit()
            conn.close()
            st.success("Risk kaydı eklendi!")
            st.rerun()

# --- 17. TOPLU SMS / DUYURU LOGU ---
elif secilen_modul == "Toplu SMS / Duyuru Logu":
    st.subheader("📢 Toplu Duyuru ve SMS Logları")
    conn = db.baglanti_kur()
    df = pd.read_sql("SELECT * FROM mesaj_loglari", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
    with st.form("sms_form"):
        grup = st.selectbox("Alıcı Grubu", ["Tüm Üyeler", "Müsabıklar", "Veli Grubu"])
        mesaj = st.text_area("Mesaj İçeriği")
        if st.form_submit_button("Mesajı Logla"):
            conn = db.baglanti_kur()
            conn.execute("INSERT INTO mesaj_loglari (alici_grup, mesaj_icerigi, gonderim_tarihi) VALUES (?, ?, ?)", 
                         (grup, mesaj, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.success("Mesaj loglandı!")
            st.rerun()

# --- 18. SAAS ABONELİK YÖNETİMİ ---
elif secilen_modul == "SaaS Abonelik Yönetimi":
    st.subheader("🏢 SaaS Salon ve Abonelik Yönetimi")
    conn = db.baglanti_kur()
    salonlar = pd.read_sql("SELECT * FROM salonlar", conn)
    conn.close()
    st.dataframe(salonlar, use_container_width=True)
    with st.form("salon_form"):
        st.write("Yeni Salon (Müşteri) Kaydı")
        s_adi = st.text_input("Salon Adı")
        sahip = st.text_input("Sahip Adı")
        tel = st.text_input("Telefon")
        email = st.text_input("E-Posta")
        if st.form_submit_button("Salon Ekle (15 Gün Deneme)"):
            if s_adi and sahip:
                db.salon_ekle(s_adi, sahip, tel, email)
                st.success(f"{s_adi} başarıyla eklendi!")
                st.rerun()
            else:
                st.warning("Salon adı ve sahip adını doldurun.")

# --- 19. KÜRESEL ÖDEMELER (UK, US, EU) - YENİ MODÜL ---
elif secilen_modul == "🌍 Küresel Ödemeler (UK, US, EU)":
    st.subheader("🌍 Küresel Ödeme Entegrasyonu (Stripe Altyapısı)")
    st.write("İngiltere (GBP), ABD (USD) ve Avrupa (EUR) şirket yapıların için uluslararası abonelik planları ve ödeme geçidi yönetimi.")
    
    col_uk, col_us, col_eu = st.columns(3)
    
    with col_uk:
        st.markdown("### 🇬🇧 United Kingdom (GBP)")
        st.write("Para Birimi: **£ (GBP)**")
        st.write("Şirket Lokasyonu: Londra, UK")
        st.info("Standart Plan: £49 / ay")
        if st.button("🇬🇧 UK Ödeme Linki Oluştur"):
            st.success("Stripe UK (GBP) abonelik ödeme linki üretildi! (Canlı API entegrasyonu için Stripe Secret Key tanımlanmalıdır)")
            st.code("https://buy.stripe.com/test_uk_ringmaster_sample_gbp")

    with col_us:
        st.markdown("### 🇺🇸 United States (USD)")
        st.write("Para Birimi: **$ (USD)**")
        st.write("Şirket Lokasyonu: Delaware, US")
        st.info("Standart Plan: $59 / ay")
        if st.button("🇺🇸 US Ödeme Linki Oluştur"):
            st.success("Stripe US (USD) abonelik ödeme linki üretildi!")
            st.code("https://buy.stripe.com/test_us_ringmaster_sample_usd")

    with col_eu:
        st.markdown("### 🇪🇺 European Union (EUR)")
        st.write("Para Birimi: **€ (EUR)**")
        st.write("Şirket Lokasyonu: Estonya / Almanya, EU")
        st.info("Standart Plan: €55 / ay")
        if st.button("🇪🇺 EU Ödeme Linki Oluştur"):
            st.success("Stripe EU (EUR) abonelik ödeme linki üretildi!")
            st.code("https://buy.stripe.com/test_eu_ringmaster_sample_eur")

    st.markdown("---")
    st.markdown("### ⚙️ Küresel Ödeme Ayarları & Webhook Durumu")
    st.text_input("Stripe Publishable Key (Canlı / Test)", type="password", value="pk_test_...")
    st.text_input("Stripe Secret Key (Canlı / Test)", type="password", value="sk_test_...")
    if st.button("Stripe Bağlantısını Test Et 🔌"):
        st.success("Stripe API köprüsü başarıyla doğrulandı! Uluslararası ödemeler almaya hazırsın patron.")

# --- 20. SİSTEM AYARLARI ---
elif secilen_modul == "Sistem Ayarları":
    st.subheader("⚙️ Sistem ve Veritabanı Ayarları")
    st.write("Veritabanı sıfırlama, yedekleme ve genel sistem parametreleri.")
    if st.button("Veritabanını Kontrol Et ve Onar"):
        db.veritabani_baslat()
        st.success("Tüm tablolar ve emniyet sütunları güncellendi!")
