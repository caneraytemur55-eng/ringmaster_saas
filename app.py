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
            "EUR": {"amount": 1800,  "symbol": "€", "currency": "EUR"}  # € 18.00
        }
    },
    "pro": {
        "name": "Profesyonel / Pro",
        "prices": {
            "TRY": {"amount": 129900, "symbol": "₺", "currency": "TRY"},
            "USD": {"amount": 4900,   "symbol": "$", "currency": "USD"},
            "GBP": {"amount": 3900,   "symbol": "£", "currency": "GBP"},
            "EUR": {"amount": 4500,   "symbol": "€", "currency": "EUR"}  # € 45.00
        }
    }
}

try:
    st.title("🥊 RingMaster SaaS - Abonelik ve Fiyatlandırma")
    st.write("Salonun yönetimini zirveye taşıyan profesyonel mikro-SaaS çözümü.")

    # Kullanıcı için Para Birimi / Bölge Seçici
    selected_currency = st.selectbox(
        "Para Birimi / Bölge Seçin",
        options=["TRY", "EUR", "USD", "GBP"],
        format_func=lambda x: {
            "TRY": "Türkiye (₺ - Iyzico)", 
            "EUR": "Avrupa (€ - Stripe)", 
            "USD": "Amerika ($ - Stripe)", 
            "GBP": "İngiltere (£ - Stripe)"
        }[x]
    )

    st.divider()

    # Planları Yan Yana Sütunlar Halinde Gösterelim
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

except Exception as e:
    st.error("Uygulama çalıştırılırken bir hata oluştu, Caner Baba:")
    st.exception(e)

                
                

    
 

            
    

