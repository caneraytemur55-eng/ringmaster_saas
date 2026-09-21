import streamlit as st
import pandas as pd
import database as db

# --- 1. MENÜ TANIMLAMASI (ÖNCE BU OLMALI) ---
st.sidebar.title("🥊 Ringmaster SaaS")
secilen_modul = st.sidebar.selectbox(
    "Modül Seçin", 
    ["Ana Sayfa", "Salon Üyeleri Yönetimi", "Yoklama Sistemi", "Stok Takibi", "Kasa / Finans"] # (Diğer modüllerin de burada olmalı)
)

# --- 2. MODÜL YÖNLENDİRMELERİ (BURADAN SONRA GELMELİ) ---
if secilen_modul == "Ana Sayfa":
    st.subheader("Ana Sayfa / Dashboard")
    st.info("Hoş geldin patron, sistem aktif!")

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
        
        # --- ÖĞRENCİ SİLME BÖLÜMÜ ---
        st.markdown("### 🗑️ Sporcu Kaydı Sil")
        with st.form("uye_sil_form"):
            silinecek_id = st.selectbox("Silinecek Sporcuyu Seç (ID - Ad Soyad)", df_uyeler.apply(lambda x: f"{x['ID']} - {x['Ad Soyad']}", axis=1).tolist())
            if st.form_submit_button("Seçilen Sporcu Kaydını Sil ❌"):
                secilen_id = int(silinecek_id.split(" - ")[0])
                db.uye_sil(secilen_id)
                st.success(f"ID'si {secilen_id} olan sporcu kaydı silindi, patron! Sayfayı yenileyebilirsin.")
                st.rerun()
    else:
        st.info("Henüz kayıtlı üye bulunmuyor.")
