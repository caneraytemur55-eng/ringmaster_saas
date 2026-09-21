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
    # Sayfayı sekmelere bölüyoruz: Biri Müşteri Vitrini, Diğeri Senin Yönetici Panelin
    tab_vitrin, tab_yonetici = st.tabs(["🌐 Müşteri Vitrini & Paketler", "🚀 Salon Yönetim Paneli (Senin Alanın)"])

    # --- 1. SEKME: MÜŞTERİ VİTRİNİ VE FİYATLAR ---
    with tab_vitrin:
        st.title("🥊 RingMaster SaaS - Salonunuzu Zirveye Taşıyın")
        st.write("Salon yönetimini dijitalleştiren profesyonel mikro-SaaS çözümü. 15 gün ücretsiz dene!")

        # Para Birimi Seçici
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

    # --- 2. SEKME: SENİN YÖNETİCİ PANELİN ---
    with tab_yonetici:
        st.title("🚀 RingMaster Geliştirici & Salon Yönetim Paneli")
        st.success("Hoş geldin patron! Burada parola sormadan tüm sistem elinin altında.")
        
        st.info("💡 15 Modülün entegrasyonunu ve veritabanı akışını bu alandan yönetiyorsun.")
        
        # Test amaçlı modül listesi önizlemesi
        moduller = [
            "1. PIN Yoklama & Mat Kontenjanı", "2. QR & Üye Self-Servis Portal", 
            "3. Antrenör Hakediş & Prim", "4. Çocuk Veli Gelişim Raporu", 
            "5. Ekipman Satış POS & Stok", "6. Kuşak Sınav Uygunluk Takibi", 
            "7. Müsabık & Fight Record", "8. Sakatlık & Sparring Protokolü", 
            "9. Maç Hazırlık Takvimi", "10. Deneme Dersi (Lead)", 
            "11. Özel Ders (PT) & Ücret", "12. Üye Yönetimi", 
            "13. Sporcu Ölçüm Takibi", "14. Kasa & Finans Paneli", "15. Kayıp Üye (Churn) Uyarısı"
        ]
        
        selected_modul = st.selectbox("Gitmek İstediğin Modülü Seç", moduller)
        st.write(f"Şu an **{selected_modul}** modülü aktif ve çalışmaya hazırdır.")

except Exception as e:
    st.error("Uygulama çalıştırılırken bir hata oluştu, Caner Baba:")
    st.exception(e)

                
                

    
 

            
    

