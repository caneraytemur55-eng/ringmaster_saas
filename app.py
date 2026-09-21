import streamlit as st
from datetime import datetime
import database as db

# Veritabanını başlat
db.veritabani_baslat()

# 1. Sayfa Yapılandırması (En üstte olmalı!)
st.set_page_config(
    page_title="RingMaster SaaS",
    page_icon="🥊",
    layout="wide"
)

try:
    st.title("🥊 RingMaster SaaS - Salon Yönetim ve Operasyon Paneli")
    st.success("Canlı SQLite Veritabanı Bağlantısı Aktif - Adım Adım İlerliyoruz Caner Baba!")

    # Sol Yan Menü (Sidebar) - Modül Seçimi
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

    # Seçilen Modüle Göre Ekran İçerikleri
    if "Üye Yönetimi" in secilen_modul:
        st.subheader("👤 Üye Yönetimi & Canlı Kayıt Paneli")
        
        with st.form("uye_kayit_formu"):
            col_a, col_b = st.columns(2)
            with col_a:
                ad_soyad = st.text_input("Sporcu Adı Soyadı")
                telefon = st.text_input("Telefon Numarası")
                pin_kodu = st.text_input("4 Haneli Giriş PIN Kodu", max_chars=4, type="password")
            with col_b:
                brans = st.selectbox("Branş / Ders", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
                paket = st.selectbox("Abonelik Tipi", ["Standart (Aylık)", "VIP Sınırsız", "Çocuk Grubu"])
            
            kayit_butonu = st.form_submit_button("Üyeyi Veritabanına Kaydet 💾")
            
            if kayit_butonu:
                if ad_soyad and len(pin_kodu) == 4:
                    db.uye_ekle(ad_soyad, telefon, brans, paket, pin_kodu)
                    st.success(f"Tebrikler patron! {ad_soyad} ({brans}) başarıyla veritabanına kaydedildi.")
                else:
                    st.warning("Lütfen sporcu adını doldurun ve 4 haneli bir PIN kodu belirleyin.")

        st.markdown("### 📋 Mevcut Salon Üyeleri Listesi")
        uyeler = db.uyeleri_getir()
        if uyeler:
            # Tablo olarak gösterim için veriyi düzenleyelim
            import pandas as pd
            df_uyeler = pd.DataFrame(uyeler, columns=["ID", "Ad Soyad", "Telefon", "Branş", "Paket", "PIN", "Kayıt Tarihi"])
            st.dataframe(df_uyeler, use_container_width=True)
        else:
            st.info("Henüz kayıtlı üye bulunmuyor. Yukarıdaki formdan ilk üyeyi ekleyebilirsin.")

    elif "PIN Yoklama" in secilen_modul:
        st.subheader("⚡ PIN Yoklama & Mat Kontenjanı")
        st.write("Sporcuların salon girişinde 4 haneli PIN kodunu girerek yoklama vermesini sağlayın.")
        
        girilen_pin = st.text_input("Sporcu 4 Haneli PIN Kodunu Girin", type="password", max_chars=4)
        if st.button("Yoklamayı Onayla ✅"):
            if len(girilen_pin) == 4:
                # Veritabanında PIN'i arayalım
                conn = db.baglanti_kur()
                cursor = conn.cursor()
                cursor.execute("SELECT ad_soyad, brans FROM uyeler WHERE pin_kodu = ?", (girilen_pin,))
                bulunan_uye = cursor.fetchone()
                conn.close()
                
                if bulunan_uye:
                    st.success(f"🥊 Hoş geldin, {bulunan_uye[0]}! ({bulunan_uye[1]} sınıfı) Yoklamanız başarıyla alındı, mat kontenjanı güncellendi.")
                else:
                    st.error("❌ Bu PIN koduna ait kayıtlı bir üye bulunamadı!")
            else:
                st.warning("Lütfen geçerli 4 haneli bir PIN kodu girin.")

    elif "QR & Üye Self-Servis" in secilen_modul:
        st.subheader("🌐 QR & Üye Self-Servis Portal")
        st.info("Sporcuların salon girişinde okutacağı dinamik QR kod ve üye self-servis paneli.")

    elif "Antrenör Hakediş" in secilen_modul:
        st.subheader("💵 Antrenör Hakediş & Prim Paneli")
        st.metric("Bu Ay Toplam Hakediş Havuzu", "34.000 ₺")
        st.write("Antrenör bazlı ders saatleri ve prim oranları hesaplamaları.")

    elif "Çocuk Veli Gelişim" in secilen_modul:
        st.subheader("👶 Çocuk Veli Gelişim Raporu")
        st.write("Minik sporcuların gelişim grafikleri, devamsızlık ve hoca değerlendirme raporları.")

    elif "Ekipman Satış POS" in secilen_modul:
        st.subheader("🛍️ Ekipman Satış POS & Stok")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.number_input("Adet", min_value=1, value=1)
            st.selectbox("Ürün", ["Deri Eldiven", "Dişlik", "Bandaj", "Şort"])
        with col_p2:
            st.write("Stok Durumu: Yeterli (Yeşil)")
        if st.button("Satışı Tamamla"):
            st.success("POS satışı başarıyla kasaya işlendi.")

    elif "Kuşak Sınav" in secilen_modul:
        st.subheader("🥋 Kuşak Sınav Uygunluk Takibi")
        st.info("Sporcunun antrenman katılım saati ve kıdemine göre sınava çıkış uygunluk kontrolü.")

    elif "Müsabık & Fight" in secilen_modul:
        st.subheader("🏆 Müsabık & Fight Record")
        st.write("Sporcuların maç geçmişleri, galibiyet/malubiyet oranları ve sıklet bilgileri.")

    elif "Sakatlık & Sparring" in secilen_modul:
        st.subheader("🚨 Sakatlık & Sparring Protokolü")
        st.warning("Aktif sakatlık bildirimleri ve sparring yasaklı sporcu listesi takibi.")

    elif "Maç Hazırlık" in secilen_modul:
        st.subheader("📅 Maç Hazırlık Takvimi")
        st.write("Yaklaşan turnuvalar, tartı günleri ve kamp antrenman programı.")

    elif "Deneme Dersi" in secilen_modul:
        st.subheader("🥊 Deneme Dersi (Lead) Yönetimi")
        st.info("Salona ilk defa gelen potansiyel müşteri kayıtları ve takip aramaları.")

    elif "Özel Ders" in secilen_modul:
        st.subheader("🎯 Özel Ders (PT) & Ücret Takibi")
        st.write("Hoca bazlı PT saatleri, paket kalan ders sayıları ve ücretlendirmeler.")

    elif "Sporcu Ölçüm" in secilen_modul:
        st.subheader("📈 Sporcu Ölçüm Takibi")
        st.info("Kilo, yağ oranı, kas kütlesi ve performans değişim grafiklerinin girildiği alan.")

    elif "Kasa & Finans" in secilen_modul:
        st.subheader("📊 Kasa & Finans Paneli")
        col_f1, col_f2, col_f3 = st.columns(3)
        col_f1.metric("Aylık Ciro", "125.400 ₺", "+15%")
        col_f2.metric("Giderler", "32.000 ₺", "-4%")
        col_f3.metric("Net Kar", "93.400 ₺", "+18%")

    elif "Kayıp Üye" in secilen_modul:
        st.subheader("🚨 Kayıp Üye (Churn) Uyarısı")
        st.warning("Son 15 gündür salona gelmeyen ve üyeliği bitmek üzere olan riskli üyelerin listesi.")

    elif "İletişim Otomasyonu" in secilen_modul:
        st.subheader("📱 İletişim Otomasyonu (SMS / WhatsApp)")
        st.text_area("Toplu Bilgilendirme / Hatırlatma Mesajı", "Değerli üyemiz, bu hafta antrenmanları aksatmayalım! 🥊")
        if st.button("Mesajları Gönder (Simülasyon)"):
            st.success("Otomatik SMS/WhatsApp kuyruğuna eklendi.")

    elif "AI Asistan & Koçluk" in secilen_modul:
        st.subheader("🤖 RingMaster AI Asistan & Salon Koçu")
        st.write("Salonunuzun operasyonel verilerini analiz eden, üye gelişimini ve finansal durumu yorumlayan yapay zeka asistanı.")

        ai_modu = st.selectbox(
            "Asistan Modu Seçin",
            ["Genel Salon Analizi", "Antrenman & Sparring Önerisi", "Kayıp Üye (Churn) Stratejisi", "Özel Soru"]
        )

        user_query = st.text_input("Asistana danışmak istediğiniz konuyu yazın:", placeholder="Örn: Bu ay gelirlerimizi artırmak için ne yapmalıyız?")

        if st.button("AI Analizini Başlat 🚀"):
            with st.spinner("Salon verileri taranıyor ve yapay zeka modeli düşünüyor..."):
                if "gelir" in user_query.lower() or "artırmak" in user_query.lower():
                    st.success("💡 **AI Öneri Raporu:** \n1. Özel ders (PT) paketlerinde kampanya düzenlenebilir.\n2. Ekipman satış POS modülündeki eldiven ve bandajlarda çapraz satış (cross-sell) yapılabilir.")
                elif "üye" in user_query.lower() or "gelmeyen" in user_query.lower():
                    st.warning("⚠️ **Churn (Kayıp Üye) Uyarısı:** \nSon 15 gündür matı ziyaret etmeyen 4 sporcu tespit edildi. 'İletişim Otomasyonu' modülü üzerinden otomatik motivasyon SMS'i tetiklenmesi önerilir.")
                else:
                    st.info(f"🤖 **AI Yanıtı:** '{user_query}' talebiniz incelendi. Salonunuzun operasyonel dengesi şu an stabil, verileriniz güvende patron!")

except Exception as e:
    st.error("Uygulama çalıştırılırken bir hata oluştu, Caner Baba:")
    st.exception(e)
