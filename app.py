import streamlit as st

# 1. Sayfa Yapılandırması (En üstte olmalı!)
st.set_page_config(
    page_title="RingMaster SaaS",
    page_icon="🥊",
    layout="wide"
)

# Fiyatlandırma Konfigürasyonun
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
    tab_vitrin, tab_yonetici = st.tabs(["🌐 Müşteri Vitrini & Paketler", "🚀 Salon Yönetim Paneli (Veri Girişleri & İşlemler)"])

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
            st.write("✅ Tüm 15 Gelişmiş Modül")
            st.write("✅ Öncelikli Destek & Sınırsız Üye")
            
            if st.button("Profesyonel Paketi Seç", key="btn_pro"):
                if selected_currency == "TRY":
                    st.info("Iyzico 3D Secure ödeme sayfasına yönlendiriliyorsunuz (TRY)...")
                else:
                    st.info(f"Stripe güvenli ödeme sayfasına yönlendiriliyorsunuz ({selected_currency})...")

    # --- 2. SEKME: SENİN YÖNETİCİ PANELİN VE İŞLEM MODÜLLERİN ---
    with tab_yonetici:
        st.title("🚀 Salon Operasyon ve Yönetim Paneli")
        st.success("Hoş geldin patron! Tüm veri girişleri ve yönetim modülleri burada aktif.")

        # İçeride hızlı geçiş yapabileceğin alt işlem başlıkları (Radio veya Selectbox)
        yonetim_islem = st.radio(
            "İşlem Seçin:",
            ["👥 Üye Ekle & Yönetimi", "📋 PIN Yoklama & Mat Kontenjanı", "💰 Antrenör Hakediş & Kasa", "📦 Ekipman Satış POS & Stok"],
            horizontal=True
        )

        st.divider()

        if "Üye Ekle" in yonetim_islem:
            st.subheader("Yeni Sporcu / Üye Kaydı")
            with st.form("uye_kayit_formu"):
                col_a, col_b = st.columns(2)
                with col_a:
                    ad_soyad = st.text_input("Sporcu Adı Soyadı")
                    telefon = st.text_input("Telefon Numarası")
                with col_b:
                    brans = st.selectbox("Branş / Ders", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
                    paket = st.selectbox("Abonelik Tipi", ["Starter", "Pro", "VIP Sınırsız"])
                
                kaydet_btn = st.form_submit_button("Üyeyi Kaydet")
                if kaydet_btn:
                    if ad_soyad:
                        st.success(f"Başarıyla kaydedildi: {ad_soyad} ({brans}) - {paket}")
                        # Buraya gerçek veritabanı kayıt kodunu ekleyebilirsin
                    else:
                        st.warning("Lütfen sporcu adını boş bırakmayın.")

        elif "PIN Yoklama" in yonetim_islem:
            st.subheader("Hızlı PIN Yoklama Sistemi")
            girilen_pin = st.text_input("Sporcu 4 Haneli PIN Kodunu Girin", type="password")
            if st.button("Yoklama Al"):
                if len(girilen_pin) == 4:
                    st.success(f"PIN ({girilen_pin}) doğrulandı! Yoklama başarıyla alındı.")
                else:
                    st.error("Geçersiz PIN kodu.")

        elif "Antrenör" in yonetim_islem:
            st.subheader("Antrenör Hakediş ve Kasa Durumu")
            st.metric(label="Bu Ay Toplam Kasa", value="48.500 ₺", delta="+12%")
            st.write("Antrenör prim hesaplamaları ve prim oranları bu alandan yönetilmektedir.")

        elif "Ekipman" in yonetim_islem:
            st.subheader("Ekipman Satış POS ve Stok Paneli")
            st.info("Eldiven, bandaj, dişlik satışları ve stok takibi burada yer alıyor.")
            col_pos1, col_pos2 = st.columns(2)
            with col_pos1:
                st.number_input("Satılan Ürün Adedi", min_value=1, value=1)
            with col_pos2:
                st.selectbox("Ürün Seç", ["Deri Boks Eldiveni", "El Bandajı", "Dişlik"])
            if st.button("Satışı Tamamla (POS)"):
                st.success("Satış başarıyla kasaya işlendi!")

except Exception as e:
    st.error("Uygulama çalıştırılırken bir hata oluştu, Caner Baba:")
    st.exception(e)

                
                

    
 

            
    

