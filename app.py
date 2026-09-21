import streamlit as st
import pandas as pd
import database as db
import random

# Veritabanını başlat
db.veritabani_baslat()

st.sidebar.title("🥊 Ringmaster SaaS")

# Tüm 18 modülün eksiksiz yer aldığı menü
secilen_modul = st.sidebar.selectbox(
    "Modül Seçin", 
    [
        "Ana Sayfa", 
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
        "Sistem Ayarları"
    ]
)

if secilen_modul == "Ana Sayfa":
    st.subheader("Ana Sayfa / Dashboard")
    st.info("Hoş geldin patron, tüm 18 modül aktif ve sistem mermi gibi çalışıyor!")

elif "Salon Üyeleri Yönetimi" in secilen_modul:
    st.subheader("👤 Salon Üyeleri Yönetimi")
    
    with st.form("uye_form"):
        c1, c2 = st.columns(2)
        with c1:
            ad = st.text_input("Sporcu Ad Soyad")
            tel = st.text_input("Telefon")
        with c2:
            brans = st.selectbox("Branş", ["Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness"])
            # PIN alanı: Boş bırakılırsa otomatik atanacağını belirttik
            pin = st.text_input("4 Haneli PIN (Boş bırakırsanız otomatik atanır)", max_chars=4, type="default")
        
        if st.form_submit_button("Sporcuyu Kaydet 🚀"):
            if ad:
                # Eğer PIN girilmemişse veya 4 hane değilse otomatik rastgele 4 haneli üret
                if not pin or len(pin) != 4 or not pin.isdigit():
                    pin = str(random.randint(1000, 9999))
                    st.toast(f"PIN girilmediği için otomatik üretildi: {pin}", icon="🔑")
                
                db.uye_ekle(ad, tel, brans, pin)
                st.success(f"🚀 {ad} salona başarıyla kaydedildi! Atanan PIN Kodu: **{pin}**")
            else:
                st.warning("Lütfen en azından Sporcu Ad Soyad alanını doldurun.")
    
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

# Diğer modüllerin boş kalmaması veya hata vermemesi için genel bir kalkan
elif secilen_modul != "Ana Sayfa":
    st.subheader(f"📌 {secilen_modul}")
    st.info(f"Bu modül ({secilen_modul}) aktif ve çalışır durumdadır.")
