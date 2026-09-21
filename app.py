import streamlit as st

st.set_page_config(page_title="RingMaster SaaS", page_icon="🥊", layout="wide")

# Oturumda giriş yapıldı mı kontrolü
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Eğer giriş yapılmadıysa vitrini (fiyatları ve satışı) göster
if not st.session_state.logged_in:
    st.title("🥊 RingMaster SaaS - Salonunuzu Zirveye Taşıyın")
    st.write("15 günlük ücretsiz deneme ile hemen başla.")
    
    # Fiyatlandırma ve paketler burada görünür...
    selected_currency = st.selectbox("Para Birimi", ["TRY", "EUR", "USD", "GBP"])
    
    st.divider()
    
    # Salon Sahibi / Yönetici Giriş Butonu (Seni içeri alacak kapı)
    with st.expander("🔑 Salon Sahibi / Yönetici Girişi (Test İçin)"):
        admin_pass = st.text_input("Yönetici Şifresi", type="password")
        if st.button("Panele Giriş Yap"):
            if admin_pass == "1234":  # Kendi belirleyeceğin geçici şifre
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Hatalı şifre!")

# Eğer giriş yapıldıysa pırıl pırıl 15 modüllü SaaS panelini aç!
else:
    st.sidebar.title("🥊 RingMaster Paneli")
    if st.sidebar.button("Çıkış Yap / Vitrine Dön"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.title("🚀 Salon Yönetim Paneli (15 Modül Aktif)")
    st.success("Hoş geldin patron, içeridesin!")
    
    # BURAYA Kendi hazırladığın 15 modülün kodlarını (PIN yoklama, üye yönetimi vb.) koyacağız
    st.write("Burada bütün salon modüllerin liste halinde çalışacak.")

                
                

    
 

            
    

