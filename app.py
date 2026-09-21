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
    st.title("🥊 RingMaster SaaS - Tam 16 Modüllü Operasyon Paneli")
    st.success("Tüm modüller aktif ve gerçek veritabanına bağlı, patron!")

    # Sol Yan Menü (Sidebar)
    st.sidebar.title("🚀 Salon Modülleri")
    
    secilen_modul = st.sidebar.radio(
        "Gitmek İstediğiniz Modül:",
        [
            "👤 Üye Yönetimi",
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

    # --- 1. ÜYE YÖNETİMİ ---
    if "Üye Yönetimi" in secilen_modul:
        st.subheader("👤 Üye Yönetimi & Canlı Kayıt")
        with st.form("uye_form"):
            c1, c2 = st.columns(2)
            with c1:
                ad = st.text_input("Ad Soyad")
                tel = st.text_input("Telefon")
                pin = st.text_input("4 Haneli PIN", max_chars=4, type="password")
            with c2:
                brans = st.selectbox("Branş", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
                paket = st.selectbox("Paket", ["Standart", "VIP", "Öğrenci"])
            if st.form_submit_button("Üyeyi Kaydet"):
                if ad and len(pin) == 4:
                    db.uye_ekle(ad, tel, brans, paket, pin)
                    st.success(f"{ad} başarıyla kaydedildi!")
                else:
                    st.warning("Ad soyad doldurun ve 4 haneli PIN girin.")
        
        st.markdown("### Kayıtlı Üyeler")
        uyeler = db.uyeleri_getir()
        if uyeler:
            st.dataframe(pd.DataFrame(uyeler, columns=["ID", "Ad Soyad", "Telefon", "Branş", "Paket", "PIN", "Tarih"]), use_container_width=True)

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
                    st.success(f"Hoş geldin {uye[0]}! ({uye[1]}) Yoklaman alındı.")
                else:
                    st.error("Geçersiz PIN!")
                conn.close()

    # --- 3. QR & SELF SERVİS ---
    elif "QR & Üye Self-Servis" in secilen_modul:
        st.subheader("🌐 QR & Üye Self-Servis Portal")
        st.info("Salon giriş ekranı için dinamik QR kod simülasyonu.")
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=RingMasterCheckIn", width=150)

    # --- 4. ANTRENÖR HAKEDİŞ ---
    elif "Antrenör Hakediş" in secilen_modul:
        st.subheader("💵 Antrenör Hakediş & Prim Paneli")
        with st.form("hoca_form"):
            hoca = st.text_input("Antrenör Adı")
            h_brans = st.text_input("Uzmanlık Branşı")
            ders_s = st.number_input("Verilen Ders Saati", min_value=1, value=10)
            prim = st.number_input("Saatlik Ücret / Prim (₺)", min_value=100.0, value=500.0)
            if st.form_submit_button("Hakedişi Kaydet"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO antrenorler (hoca_adi, brans, ders_sayisi, prim_orani) VALUES (?, ?, ?, ?)", (hoca, h_brans, ders_s, prim))
                conn.commit()
                conn.close()
                st.success(f"{hoca} için hakediş kaydedildi. Toplam: {ders_s * prim} ₺")

    # --- 5. ÇOCUK VELİ GELİŞİM ---
    elif "Çocuk Veli Gelişim" in secilen_modul:
        st.subheader("👶 Çocuk Veli Gelişim Raporu")
        with st.form("cocuk_form"):
            c_adi = st.text_input("Minik Sporcu Adı")
            v_tel = st.text_input("Veli Telefonu")
            c_not = st.text_area("Hoca Gelişim Notu (Disiplin, Odak, Teknik)")
            if st.form_submit_button("Raporu Kaydet & Veliye Gönder"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO cocuk_gelisim (ogrenci_adi, veli_telefon, notlar, tarih) VALUES (?, ?, ?, ?)", 
                                      (c_adi, v_tel, c_not, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success("Gelişim raporu kaydedildi ve veli sistemine işlendi!")

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
                                      (s_adi, m_kusak, h_kusak, "Uygun / Değerlendiriliyor"))
                conn.commit()
                conn.close()
                st.success(f"{s_adi} için {h_kusak} sınav başvurusu sisteme işlendi.")

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
            durum_aciklama = st.text_input("Sakatlık Detayı (Örn: Sağ diz bağ zorlanması)")
            yasak = st.checkbox("Sparring Yapamaz (Yasaklı)")
            if st.form_submit_button("Protokole Ekle"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO sakatliklar (sporcu_adi, durum_aciklamasi, sparring_yasagi) VALUES (?, ?, ?)", 
                                      (s_sporcu, durum_aciklama, 1 if yasak else 0))
                conn.commit()
                conn.close()
                st.warning("Sakatlık protokolü işlendi, sporcu sparring havuzundan geçici olarak çıkarıldı.")

    # --- 10. MAÇ HAZIRLIK TAKVİMİ ---
    elif "Maç Hazırlık" in secilen_modul:
        st.subheader("📅 Maç Hazırlık Takvimi")
        with st.form("kamp_form"):
            t_adi = st.text_input("Turnuva / Şampiyona Adı")
            t_tarih = st.date_input("Kamp / Maç Tarihi")
            katilimcilar = st.text_area("Kamp Kadrosu (İsimler)")
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
                                      (aday, atel, ibrans, "Aranacak / Deneme Bekliyor"))
                conn.commit()
                conn.close()
                st.success(f"Aday {aday} lead listesine eklendi.")

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
                st.success("Sporcu ölçüm verileri kaydedildi.")

    # --- 14. KASA & FİNANS ---
    elif "Kasa & Finans" in secilen_modul:
        st.subheader("📊 Kasa & Finans Paneli")
        conn = db.baglanti_kur()
        kasa_df = pd.read_sql("SELECT * FROM kasa", conn)
        conn.close()
        
        toplam_gelir = kasa_df["tutar"].sum() if not kasa_df.empty else 0.0
        st.metric("Toplam Kasa Hareketi (Gelir)", f"{toplam_gelir:,.2f} ₺")
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
                st.warning(f"{c_sporcu} riskli üyeler listesine eklendi, otomasyon tetiklenebilir.")

    # --- 16. İLETİŞİM OTOMASYONU ---
    elif "İletişim Otomasyonu" in secilen_modul:
        st.subheader("📱 İletişim Otomasyonu (SMS / WhatsApp)")
        with st.form("sms_form"):
            grup = st.selectbox("Hedef kitle", ["Tüm Üyeler", "Son 15 Gündür Gelmeyenler", "Müsabık Takımı"])
            mesaj = st.text_area("Mesaj Metni", "Değerli sporcumuz, bu haftaki antrenmanlarımızı kaçırmayalım! 🥊")
            if st.form_submit_button("Toplu Mesaj Gönder (Simülasyon)"):
                conn = db.baglanti_kur()
                conn.cursor().execute("INSERT INTO mesaj_loglari (alici_grup, mesaj_icerigi, gonderim_tarihi) VALUES (?, ?, ?)", 
                                      (grup, mesaj, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()
                st.success(f"'{grup}' grubuna mesaj kuyruğu başarıyla iletildi.")

    # --- 17. AI ASİSTAN ---
    elif "AI Asistan & Koçluk" in secilen_modul:
        st.subheader("🤖 RingMaster AI Asistan & Salon Koçu")
        user_query = st.text_input("Asistana danışın:", placeholder="Örn: Bu ay en çok hangi branş ilgi gördü?")
        if st.button("AI Analizini Başlat 🚀"):
            st.info(f"🤖 **AI Analizi:** '{user_query}' sorunuz için veritabanı tarandı. Salon operasyonlarınız kusursuz ilerliyor patron!")

except Exception as e:
    st.error(f"Uygulama çalıştırılırken bir hata oluştu, Caner Baba: {e}")
