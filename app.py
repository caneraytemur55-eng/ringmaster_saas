import streamlit as st

# 1. Sayfa Yapılandırması (En üstte olmalı!)
st.set_page_config(
    page_title="RingMaster SaaS",
    page_icon="🥊",
    layout="wide"
)

# Fiyatlandırma Konfigürasyonun (TRY, EUR, USD, GBP)
PRICING_CONFIG = {
    "starter": {
        "name": "Başlangıç / Starter",
        "prices": {
            "TRY": {"amount": 49900, "symbol": "₺", "currency": "TRY"},
            "USD": {"amount": 1900,  "symbol": "$", "currency": "USD"},
            "GBP": {"amount": 1500,  "symbol": "£", "currency": "GBP"},
            "EUR": {"amount": 1800,  "symbol": "€", "currency": "EUR"}
        }
    },
    "pro": {
        "name": "Profesyonel / Pro",
        "prices": {
            "TRY": {"amount": 129900, "symbol": "₺", "currency": "TRY"},
            "USD": {"amount": 4900,   "symbol": "$", "currency": "USD"},
            "GBP": {"amount": 3900,   "symbol": "£", "currency": "GBP"},
            "EUR": {"amount": 4500,   "symbol": "€", "currency": "EUR"}
        }
    }
}

try:
    # Sayfayı iki ana sekmeye bölüyoruz
    tab_vitrin, tab_yonetici = st.tabs(["🌐 Müşteri Vitrini & Paketler", "🚀 Salon Yönetim Paneli (Tam 16 Modül)"])

    # --- 1. SEKME: MÜŞTERİ VİTRİNİ VE FİYATLAR ---
    with tab_vitrin:
        st.title("🥊 RingMaster SaaS - Salonunuzu Zirveye Taşıyın")
        st.write("Salon yönetimini dijitalleştiren profesyonel mikro-SaaS çözümü. 15 gün ücretsiz dene!")

        selected_currency = st.selectbox(
            "Para Birimi / Bölge Seçin",
            options=["TRY", "EUR", "USD", "GBP"],
            format_func=lambda x: {
                "TRY": "Türkiye (₺ - Iyzico)", 
                "EUR": "Avrupa (€ - Stripe)", 
                "USD": "Amerika ($ - Stripe)", 
                "GBP": "İngiltere (£ - Stripe)"
            }[x],
            key="vitrin_para_birimi"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            plan_data = PRICING_CONFIG["starter"]
            price_info = plan_data["prices"][selected_currency]
            formatted_price = f"{price_info['amount'] / 100.0:.2f} {price_info['symbol']}"
            
            st.subheader(plan_data["name"])
            st.markdown(f"### **{formatted_price}** / Ay")
            st.write("✅ 15 Gün Ücretsiz Deneme")
            st.write("✅ Temel Salon Modülleri")
            st.write("✅ QR & Üye Self-Servis")
            
            if st.button("Başlangıç Paketini Seç", key="btn_starter"):
                if selected_currency == "TRY":
                    st.info("Iyzico güvenli ödeme sayfasına yönlendiriliyorsunuz (TRY)...")
                else:
                    st.info(f"Stripe güvenli ödeme sayfasına yönlendiriliyorsunuz ({selected_currency})...")

        with col2:
            plan_data = PRICING_CONFIG["pro"]
            price_info = plan_data["prices"][selected_currency]
            formatted_price = f"{price_info['amount'] / 100.0:.2f} {price_info['symbol']}"
            
            st.subheader(plan_data["name"])
            st.markdown(f"### **{formatted_price}** / Ay")
            st.write("✅ 15 Gün Ücretsiz Deneme")
            st.write("✅ Tüm 16 Gelişmiş Modül")
            st.write("✅ Öncelikli Destek & Sınırsız Üye")
            
            if st.button("Profesyonel Paketi Seç", key="btn_pro"):
                if selected_currency == "TRY":
                    st.info("Iyzico 3D Secure ödeme sayfasına yönlendiriliyorsunuz (TRY)...")
                else:
                    st.info(f"Stripe güvenli ödeme sayfasına yönlendiriliyorsunuz ({selected_currency})...")

    # --- 2. SEKME: SENİN YÖNETİCİ PANELİN (TAM 16 MODÜL) ---
    with tab_yonetici:
        st.title("🚀 Salon Operasyon ve Yönetim Paneli")
        st.success("Hoş geldin patron! Tüm operasyonel modüller ve veri girişleri emre amade.")

        # Tam 16 modülü içeren seçim menüsü
        secilen_modul = st.selectbox(
            "🛠️ Yönetim Modülü Seçin:",
            [
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
                "👤 Üye Yönetimi", 
                "📈 Sporcu Ölçüm Takibi",
                "📊 Kasa & Finans Paneli", 
                "🚨 Kayıp Üye (Churn) Uyarısı",
                "📱 İletişim Otomasyonu (SMS/WA)"
            ]
        )

        st.divider()

        # Seçilen modüle göre ilgili alanların açılması
        if "Üye Yönetimi" in secilen_modul:
            st.subheader("👤 Üye Yönetimi & Yeni Kayıt")
            with st.form("uye_kayit_formu"):
                col_a, col_b = st.columns(2)
                with col_a:
                    ad_soyad = st.text_input("Sporcu Adı Soyadı")
                    telefon = st.text_input("Telefon Numarası")
                with col_b:
                    brans = st.selectbox("Branş / Ders", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
                    paket = st.selectbox("Abonelik Tipi", ["Starter", "Pro", "VIP Sınırsız"])
                
                if st.form_submit_button("Üyeyi Kaydet"):
                    if ad_soyad:
                        st.success(f"Başarıyla kaydedildi: {ad_soyad} ({brans}) - {paket}")
                    else:
                        st.warning("Lütfen sporcu adını boş bırakmayın.")

        elif "PIN Yoklama" in secilen_modul:
            st.subheader("⚡ PIN Yoklama & Mat Kontenjanı")
            girilen_pin = st.text_input("Sporcu 4 Haneli PIN Kodunu Girin", type="password")
            if st.button("Yoklama Al"):
                if len(girilen_pin) == 4:
                    st.success(f"PIN ({girilen_pin}) doğrulandı! Mat kontenjanı güncellendi.")
                else:
                    st.error("Geçersiz PIN kodu.")

        elif "QR & Üye Self-Servis" in secilen_modul:
            st.subheader("🌐 QR & Üye Self-Servis Portal")
            st.info("Sporcuların salon girişinde okutacağı dinamik QR kod ve üye self-servis panel yönetimi.")

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

except Exception as e:
    st.error("Uygulama çalıştırılırken bir hata oluştu, Caner Baba:")
    st.exception(e)

                
                

    
 

            
    

