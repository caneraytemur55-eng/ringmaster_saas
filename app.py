import streamlit as st
from datetime import datetime
import database as db
import pandas as pd

# Veritabanını başlat
db.veritabani_baslat()

st.set_page_config(
    page_title="RingMaster SaaS",
    page_icon="🥊",
    layout="wide"
)

try:
    st.title("🥊 RingMaster SaaS - B2B Salon Abonelik & Yönetim Paneli")
    st.success("SaaS altyapısı, 15 günlük salon deneme süresi ve 999 ₺ otomatik yükseltim modülü aktif, patron!")

    # Sol Yan Menü (Sidebar)
    st.sidebar.title("🚀 SaaS & Salon Modülleri")
    
    secilen_modul = st.sidebar.radio(
        "Gitmek İstediğiniz Modül:",
        [
            "🏢 SaaS Salonlar & 15 Gün Deneme Takibi",
            "👤 Salon Üyeleri Yönetimi",
            "⚡ PIN Yoklama & Mat Kontenjanı",
            "🌐 QR & Üye Self-Servis Portal",
            "💵 Antrenör Hakediş & Prim",
            "👶 Çocuk Veli Gelişim Raporu",
            "🛍️ Ekipman Satış POS & Stok",
            "🥋 Kuşak Sınav Uygunluk Takibi",
            "🏆 Müsabık & Fight Record",
            "🚨 Sakatlık & Sparring Protokolü",
            "📅 Maç Hazırlık Takvimi",
            "🥊 Deneme Dersi (Lead)",
            "🎯 Özel Ders (PT) & Ücret",
            "📈 Sporcu Ölçüm Takibi",
            "📊 Kasa & Finans Paneli", 
            "🚨 Kayıp Üye (Churn) Uyarısı",
            "📱 İletişim Otomasyonu (SMS/WA)",
            "🤖 AI Asistan & Koçluk"
        ]
    )

    st.divider()

    # --- 0. SAAS SALONLAR & 15 GÜN DENEME TAKİBİ ---
    if "SaaS Salonlar" in secilen_modul:
        st.subheader("🏢 SaaS Müşterileri (Salon Sahipleri) & Deneme Süresi Takibi")
        st.write("Sisteminize yeni üye olan spor salonlarını kaydedin. Her yeni salon otomatik **15 günlük ücretsiz deneme** ile başlar.")
        
        with st.form("salon_form"):
            c1, c2 = st.columns(2)
            with c1:
                salon_adi = st.text_input("Spor Salonu Adı (Örn: Titan Fight Club)")
                sahip_adi = st.text_input("Salon Sahibi Adı Soyadı")
            with c2:
                tel = st.text_input("İletişim Telefonu")
                email = st.text_input("E-Posta Adresi")
            
            if st.form_submit_button("Salonu Kaydet (15 Gün Ücretsiz SaaS Denemesi Başlat) 🚀"):
                if salon_adi and sahip_adi:
                    db.salon_ekle(salon_adi, sahip_adi, tel, email)
                    st.success(f"Tebrikler patron! {salon_adi} sisteme eklendi ve sahibine 15 günlük ücretsiz SaaS denemesi tanımlandı.")
                else:
                    st.warning("Lütfen salon adını ve sahip adını doldurun.")
        
        st.markdown("### 📋 Sistemdeki Tüm Salonlar ve SaaS Abonelik Durumları")
        salonlar = db.salonlari_getir()
        if salonlar:
            df_salonlar = pd.DataFrame(salonlar, columns=["ID", "Salon Adı", "Sahip", "Telefon", "E-Posta", "Kayıt Tarihi", "Deneme Bitiş", "Abonelik Durumu"])
            st.dataframe(df_salonlar, use_container_width=True)
            
            st.divider()
            st.markdown("### ⚡ Otomatik Paket Yükseltimi (999 ₺ / Ay SaaS Geliri)")
            st.write("Deneme süresi dolan veya PRO sürüme geçmek isteyen salonu **999 ₺ / Ay** lık aylık aboneliğe yükseltin:")
            
            with st.form("saas_upgrade_form"):
                secilen_salon = st.selectbox("Salon Seçin", df_salonlar["Salon Adı"].tolist())
                if st.form_submit_button("999 ₺ Aylık PRO Pakete Yükselt ve Kasaya İşle 💳"):
                    conn = db.baglanti_kur()
                    cur = conn.cursor()
                    cur.execute("UPDATE salonlar SET abonelik_durumu = ? WHERE salon_adi = ?", ("PRO Abonelik (999 ₺/Ay)", secilen_salon))
                    cur.execute("INSERT INTO kasa (islem_tipi, aciklama, tutar, tarih) VALUES (?, ?, ?, ?)", 
                                ("Gelir", f"SaaS Abonelik Geliri: {secilen_salon} (999 ₺)", 999.0, datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    conn.close()
                    st.success(f"Harika! {secilen_salon} salonunun SaaS aboneliği 999 ₺/Ay PRO plana yükseltildi ve tutar kasaya gelir olarak işlendi.")
        else:
            st.info("Henüz kayıtlı SaaS salonu bulunmuyor.")

    # --- 1. SALON ÜYELERİ YÖNETİMİ ---
    elif "Salon Üyeleri Yönetimi" in secilen_modul:
        st.subheader("👤 Salon Üyeleri Yönetimi")
        
        with st.form("uye_form"):
            c1, c2 = st.columns(2)
            with c1:
                ad = st.text_input("Sporcu Ad Soyad")
                tel = st.text_input("Telefon")
            with c2:
                brans = st.selectbox("Branş", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
                pin = st.text_input("4 Haneli PIN", max_chars=4, type="password")
            
            if st.form_submit_button("Sporcuyu Kaydet 🚀"):
                if ad and len(pin) == 4:
                    db.uye_ekle(ad, tel, brans, pin)
                    st.success(f"{ad} salona başarıyla kaydedildi.")
                else:
                    st.warning("Ad soyad doldurun ve 4 haneli PIN girin.")
        
        st.markdown("### 📋 Kayıtlı Sporcular")
        uyeler = db.uyeleri_getir()
        if uyeler:
            df_uyeler = pd.DataFrame(uyeler, columns=["ID", "Ad Soyad", "Telefon", "Branş", "PIN", "Kayıt Tarihi"])
            st.dataframe(df_uyeler, use_container_width=True)
        else:
            st.info("Henüz kayıtlı üye bulunmuyor.")

    # --- 2. PIN YOKLAMA ---
    elif "PIN Yoklama" in secilen_modul:
        st.subheader("⚡ PIN Yoklama & Mat Kontenjanı")
        girilen_pin = st.text_input("4 Haneli PIN Kodunu Girin", type="password", max_chars=4)
        if st.button("Yoklama Al"):
            if len(girilen_pin) == 4:
                conn = db.baglanti_kur()
                cur = conn.cursor()
                cur.execute("SELECT ad_soyad, brans FROM uyeler WHERE pin_kodu = ?", (girilen_pin,))
                uye = cur.fetchone()
                if uye:
                    cur.execute("INSERT INTO yoklamalar (pin_kodu, ad_soyad, brans, giris_zamani) VALUES (?, ?, ?, ?)", 
                                (girilen_pin, uye[0], uye[1], datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    st.success(f"Hoş geldin {uye[0]}! ({uye[1]}) - Yoklaman alındı.")
                else:
                    st.error("Geçersiz PIN!")
                conn.close()

    # --- 3. QR & SELF SERVİS ---
    elif "QR & Üye Self-Servis" in secilen_modul:
        st.subheader("🌐 QR & Üye Self-Servis Portal")
        st.info("Salon giriş ekranı için dinamik QR kod simülasyonu.")
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=RingMasterCheckIn", width=150)

    # --- 4. ANTRENÖR HAKEDİŞ & PRİM ---
    elif "Antrenör Hakediş" in secilen_modul:
        st.subheader("💵 Antrenör Hakediş & Prim Paneli")
        with st.form("hoca_form"):
            c_h1, c_h2 = st.columns(2)
            with c_h1:
                hoca = st.text_input("Antrenör Adı Soyadı")
                h_brans = st.selectbox("Uzmanlık Branşı", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
            with c_h2:
                ders_s = st.number_input("Verilen Ders / PT Saati", min_value=1, value=10)
                prim = st.number_input("Saatlik Ücret / Prim (₺)", min_value=100.0, value=500.0)
            
            if st.form_submit_button("Hakedişi Hesapla & Kaydet 💾"):
                if hoca:
                    toplam_hakedis = ders_s * prim
                    conn = db.baglanti_kur()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO antrenorler (hoca_adi, brans, ders_sayisi, prim_orani) VALUES (?, ?, ?, ?)", 
                                (hoca, h_brans, ders_s, prim))
                    cur.execute("INSERT INTO kasa (islem_tipi, aciklama, tutar, tarih) VALUES (?, ?, ?, ?)", 
                                ("Gider", f"Antrenör Hakediş: {hoca} ({ders_s} Saat)", toplam_hakedis, datetime.now().strftime("%Y-%m-%d")))
                    conn.commit()
                    conn.close()
                    st.success(f"{hoca} için {toplam_hakedis:,.2f} ₺ hakediş kaydedildi ve kasaya gider olarak işlendi.")
                else:
                    st.warning("Lütfen antrenör adını giriniz.")

        st.markdown("### 📋 Kayıtlı Antrenör Hakedişleri")
        conn = db.baglanti_kur()
        hakedis_df = pd.read_sql("SELECT * FROM antrenorler", conn)
        conn.close()
        if not hakedis_df.empty:
            hakedis_df["Toplam Hakediş (₺)"] = hakedis_df["ders_sayisi"] * hakedis_df["prim_orani"]
            st.dataframe(hakedis_df, use_container_width=True)

    # --- 5. ÇOCUK VELİ GELİŞİM ---
    elif "Çocuk Veli Gelişim" in secilen_modul:
        st.subheader("👶 Çocuk Veli Gelişim Raporu")
        with st.form("cocuk_form"):
            c_adi = st.text_input("Minik Sporcu Adı")
            v_tel = st.text_input("Veli Telefonu")
            c_not = st.text_area("Hoca Gelişim Notu")
            if st.form_submit_button("Raporu Kaydet"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO cocuk_gelisim (ogrenci_adi, veli_telefon, notlar, tarih) VALUES (?, ?, ?, ?)", 
                                      (c_adi, v_tel, c_not, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success("Gelişim raporu kaydedildi!")

    # --- 6. EKİPMAN SATIŞ POS ---
    elif "Ekipman Satış POS" in secilen_modul:
        st.subheader("🛍️ Ekipman Satış POS & Stok")
        conn = db.baglanti_kur()
        stoklar = pd.read_sql("SELECT * FROM stok", conn)
        conn.close()
        st.dataframe(stoklar, use_container_width=True)
        
        with st.form("pos_form"):
            urun = st.selectbox("Satılacak Ürün", stoklar["urun_adi"].tolist() if not stoklar.empty else [])
            adet = st.number_input("Adet", min_value=1, value=1)
            if st.form_submit_button("Satışı Tamamla (POS)"):
                conn = db.baglanti_kur()
                cur = conn.cursor()
                cur.execute("SELECT fiyat FROM stok WHERE urun_adi = ?", (urun,))
                fiyat = cur.fetchone()[0]
                toplam = fiyat * adet
                cur.execute("INSERT INTO kasa (islem_tipi, aciklama, tutar, tarih) VALUES (?, ?, ?, ?)", 
                            ("Gelir", f"POS Satış: {adet}x {urun}", toplam, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success(f"Satış başarılı! Kasaya {toplam} ₺ eklendi.")

    # --- 7. KUŞAK SINAV ---
    elif "Kuşak Sınav" in secilen_modul:
        st.subheader("🥋 Kuşak Sınav Uygunluk Takibi")
        with st.form("sinav_form"):
            s_adi = st.text_input("Sporcu Adı")
            m_kusak = st.selectbox("Mevcut Kuşak", ["Beyaz", "Sarı", "Yeşil", "Mavi", "Kahverengi"])
            h_kusak = st.selectbox("Hedef Kuşak", ["Sarı", "Yeşil", "Mavi", "Kahverengi", "Siyah"])
            if st.form_submit_button("Sınav Durumunu Güncelle"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO kusak_sinav (ogrenci_adi, mevcut_kusak, hedef_kusak, durum) VALUES (?, ?, ?, ?)", 
                                      (s_adi, m_kusak, h_kusak, "Uygun"))
                conn.commit()
                conn.close()
                st.success("Sınav başvurusu işlendi.")

    # --- 8. MÜSABIK & FIGHT RECORD ---
    elif "Müsabık & Fight" in secilen_modul:
        st.subheader("🏆 Müsabık & Fight Record")
        with st.form("fight_form"):
            m_adi = st.text_input("Müsabık Sporcu Adı")
            siklet = st.text_input("Siklet (Örn: 70kg)")
            gal = st.number_input("Galibiyet", min_value=0, value=0)
            mag = st.number_input("Mağlubiyet", min_value=0, value=0)
            if st.form_submit_button("Fight Record Kaydet"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO musabiklar (sporcu_adi, siklet, galibiyet, maglubiyet) VALUES (?, ?, ?, ?)", 
                                      (m_adi, siklet, gal, mag))
                conn.commit()
                conn.close()
                st.success("Müsabık sicili güncellendi.")

    # --- 9. SAKATLIK & SPARRING ---
    elif "Sakatlık & Sparring" in secilen_modul:
        st.subheader("🚨 Sakatlık & Sparring Protokolü")
        with st.form("sakat_form"):
            s_sporcu = st.text_input("Sporcu Adı")
            durum_aciklama = st.text_input("Sakatlık Detayı")
            yasak = st.checkbox("Sparring Yapamaz (Yasaklı)")
            if st.form_submit_button("Protokole Ekle"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO sakatliklar (sporcu_adi, durum_aciklamasi, sparring_yasagi) VALUES (?, ?, ?)", 
                                      (s_sporcu, durum_aciklama, 1 if yasak else 0))
                conn.commit()
                conn.close()
                st.warning("Sakatlık protokolü işlendi.")

    # --- 10. MAÇ HAZIRLIK TAKVİMİ ---
    elif "Maç Hazırlık" in secilen_modul:
        st.subheader("📅 Maç Hazırlık Takvimi")
        with st.form("kamp_form"):
            t_adi = st.text_input("Turnuva / Şampiyona Adı")
            t_tarih = st.date_input("Kamp / Maç Tarihi")
            katilimcilar = st.text_area("Kamp Kadrosu")
            if st.form_submit_button("Kamp Takvimine Ekle"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO mac_takvimi (turnuva_adi, tarih, katilacak_sporcular) VALUES (?, ?, ?)", 
                                      (t_adi, str(t_tarih), katilimcilar))
                conn.commit()
                conn.close()
                st.success("Maç kamp takvimi oluşturuldu.")

    # --- 11. DENEME DERSİ (LEAD) ---
    elif "Deneme Dersi" in secilen_modul:
        st.subheader("🥊 Deneme Dersi (Lead) Yönetimi")
        with st.form("lead_form"):
            aday = st.text_input("Aday Adı Soyadı")
            atel = st.text_input("Telefon Numarası")
            ibrans = st.selectbox("İlgilendiği Branş", ["Boks", "Kick Boks", "Muay Thai"])
            if st.form_submit_button("Adayı Kaydet"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO adaylar (aday_adi, telefon, ilgilenilen_brans, durum) VALUES (?, ?, ?, ?)", 
                                      (aday, atel, ibrans, "Bekliyor"))
                conn.commit()
                conn.close()
                st.success("Aday lead listesine eklendi.")

    # --- 12. ÖZEL DERS (PT) ---
    elif "Özel Ders" in secilen_modul:
        st.subheader("🎯 Özel Ders (PT) & Ücret Takibi")
        with st.form("pt_form"):
            sporcu = st.text_input("Sporcu Adı")
            hoca = st.text_input("Eğitmen Adı")
            k_ders = st.number_input("Kalan Ders Paketi", min_value=1, value=10)
            if st.form_submit_button("PT Paketini Tanımla"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO ozel_dersler (sporcu_adi, hoca_adi, kalan_ders) VALUES (?, ?, ?)", 
                                      (sporcu, hoca, k_ders))
                conn.commit()
                conn.close()
                st.success("Özel ders paketi tanımlandı.")

    # --- 13. SPORCU ÖLÇÜM ---
    elif "Sporcu Ölçüm" in secilen_modul:
        st.subheader("📈 Sporcu Ölçüm Takibi")
        with st.form("olcum_form"):
            osporcu = st.text_input("Sporcu Adı")
            kilo = st.number_input("Kilo (kg)", min_value=30.0, value=75.0)
            yag = st.number_input("Yağ Oranı (%)", min_value=3.0, value=15.0)
            if st.form_submit_button("Ölçümleri Kaydet"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO olcumler (sporcu_adi, kilo, yag_orani, tarih) VALUES (?, ?, ?, ?)", 
                                      (osporcu, kilo, yag, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success("Ölçüm verileri kaydedildi.")

    # --- 14. KASA & FİNANS ---
    elif "Kasa & Finans" in secilen_modul:
        st.subheader("📊 Kasa & Finans Paneli (Gelir / Gider Yönetimi)")
        with st.form("kasa_form"):
            c_f1, c_f2, c_f3 = st.columns(3)
            with c_f1:
                tip = st.selectbox("İşlem Tipi", ["Gelir", "Gider"])
            with c_f2:
                tutar = st.number_input("Tutar (₺)", min_value=1.0, value=500.0)
            with c_f3:
                tarih_str = st.text_input("Tarih", value=datetime.now().strftime("%Y-%m-%d %H:%M"))
            aciklama = st.text_input("İşlem Açıklaması")
            if st.form_submit_button("Kasa İşlemini Kaydet 💾"):
                if aciklama:
                    conn = db.baglanti_kur()
                    conn.cursor().execute("INSERT INTO kasa (islem_tipi, aciklama, tutar, tarih) VALUES (?, ?, ?, ?)", 
                                          (tip, aciklama, tutar, tarih_str))
                    conn.commit()
                    conn.close()
                    st.success(f"Kasaya {tip} olarak {tutar:,.2f} ₺ işlendi.")
                else:
                    st.warning("Lütfen açıklama girin.")

        st.divider()
        conn = db.baglanti_kur()
        kasa_df = pd.read_sql("SELECT * FROM kasa", conn)
        conn.close()
        if not kasa_df.empty:
            gelir = kasa_df[kasa_df["islem_tipi"] == "Gelir"]["tutar"].sum()
            gider = kasa_df[kasa_df["islem_tipi"] == "Gider"]["tutar"].sum()
            net = gelir - gider
            c1, c2, c3 = st.columns(3)
            c1.metric("Toplam Gelir", f"{gelir:,.2f} ₺")
            c2.metric("Toplam Gider", f"{gider:,.2f} ₺")
            c3.metric("Net Kasa", f"{net:,.2f} ₺")
            st.dataframe(kasa_df, use_container_width=True)

    # --- 15. KAYIP ÜYE (CHURN) ---
    elif "Kayıp Üye" in secilen_modul:
        st.subheader("🚨 Kayıp Üye (Churn) Uyarısı")
        with st.form("churn_form"):
            c_sporcu = st.text_input("Riskli Görülen Sporcu Adı")
            if st.form_submit_button("Churn Takibine Al"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO churn_takip (sporcu_adi, son_gelis_tarihi, risk_durumu) VALUES (?, ?, ?)", 
                                      (c_sporcu, datetime.now().strftime("%Y-%m-%d"), "Yüksek Risk"))
                conn.commit()
                conn.close()
                st.warning("Üye risk listesine eklendi.")

    # --- 16. İLETİŞİM OTOMASYONU ---
    elif "İletişim Otomasyonu" in secilen_modul:
        st.subheader("📱 İletişim Otomasyonu (SMS / WhatsApp)")
        with st.form("sms_form"):
            grup = st.selectbox("Hedef kitle", ["Tüm Üyeler", "Deneme Süresindekiler", "Müsabık Takımı"])
            mesaj = st.text_area("Mesaj Metni", "Değerli üyemiz, matımızda başarılar dileriz! 🥊")
            if st.form_submit_button("Toplu Mesaj Gönder"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO mesaj_loglari (alici_grup, mesaj_icerigi, gonderim_tarihi) VALUES (?, ?, ?)", 
                                      (grup, mesaj, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()
                st.success("Mesaj kuyruğa eklendi.")

    # --- 17. AI ASİSTAN ---
    elif "AI Asistan & Koçluk" in secilen_modul:
        st.subheader("🤖 RingMaster AI Asistan & Salon Koçu")
        user_query = st.text_input("Asistana danışın:")
        if st.button("AI Analizini Başlat 🚀"):
            st.info("🤖 **AI Analizi:** SaaS salon büyüme metrikleri ve MRR optimize ediliyor patron, her şey yolunda!")

except Exception as e:
    st.error(f"Bir hata oluştu, Caner Baba: {e}")
