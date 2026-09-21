import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevulari_getir,
    deneme_ekle, denemeleri_getir,
    ozel_ders_ekle, ozel_dersleri_getir, ozel_ders_seans_dus, ozel_ders_ucret_guncelle,
    kurulum_tarihi_getir, kasa_islem_ekle, kasa_ozet_getir, kasa_islemleri_getir,
    olcum_ekle, olcumleri_getir, uykudaki_uyeleri_getir,
    pin_ile_yoklama_al, ders_sayisi_arttir, kusak_yukselt_sifirla,
    musabik_ekle_guncelle, musabik_getir, sakatlik_ekle, sakatliklari_getir, sakatlik_kapat,
    tum_yaklasan_maclari_getir, urun_ekle, urunleri_getir, urun_satisi_yap, cocuk_rapor_guncelle,
    antrenor_ekle, antrenorleri_getir
)

# Veritabanı Kurulumu
init_db()

st.set_page_config(page_title="RingMaster SaaS v4.8", page_icon="🥊", layout="wide")

st.title("🥊 RingMaster SaaS v4.8 - QR Portal & FİNAL Sürümü")

# --- 15 GÜNLÜK DENEME SÜRESİ MANTIĞI ---
kurulum_str = kurulum_tarihi_getir()
try:
    kurulum_dt = datetime.datetime.strptime(kurulum_str, "%Y-%m-%d").date()
except Exception:
    kurulum_dt = datetime.date.today()

gecen_gun = (datetime.date.today() - kurulum_dt).days
kalan_deneme_gunu = max(0, 15 - gecen_gun)

IS_PRO = st.sidebar.checkbox("PRO Lisansı Aktifleştir", value=False)

st.sidebar.markdown("---")
if IS_PRO:
    st.sidebar.success("🟢 **PRO PAKET AKTİF**\n\nSınırsız Erişim Özelliği Açık.")
else:
    if kalan_deneme_gunu > 0:
        st.sidebar.warning(f"⏳ **15 GÜNLÜK ÜCRETSİZ DENEME**\n\nKalan Süre: **{kalan_deneme_gunu} Gün**")
    else:
        st.sidebar.error("🔴 **DENEME SÜRENİZ DOLDU!**\n\nKullanıma devam etmek için PRO Lisansı aktifleştirin.")

st.sidebar.markdown("---")

tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs([
    "⚡ PIN Yoklama & Mat Kontenjanı",
    "🌐 QR & Üye Self-Servis Portal",
    "💵 Antrenor Hakediş & Prim",
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
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

BARAJ_DERS_SAYISI = 24

if not IS_PRO and kalan_deneme_gunu <= 0:
    st.error("⛔ **Deneme Süreniz Dolmuştur!** 15 günlük ücretsiz deneme periyodunuz sona ermiştir. Lütfen yönetici ile iletişime geçip PRO pakete geçiniz.")
else:

    # --- TAB 0: PIN YOKLAMA & MAT KONTENJANI ---
    with tab0:
        st.subheader("⚡ Hızlı PIN/QR Yoklama ve Mat Kontenjan Paneli")
        col_m1, col_m2 = st.columns(2)
        mat_kapasite = col_m1.number_input("🤼‍♂️ Mat / Ring Maksimum Kapasitesi (Kişi)", min_value=5, max_value=100, value=15)
        
        if "mat_mevcut" not in st.session_state:
            st.session_state.mat_mevcut = 0

        col_m1.metric("Mevcut Mat Kalabalığı", f"{st.session_state.mat_mevcut} / {mat_kapasite} Kişi")
        if st.session_state.mat_mevcut >= mat_kapasite:
            col_m1.error("🚨 MAT KONTENJANI DOLDU! Yeni sporcu girmeden sıra bekletilmeli.")
        
        if col_m1.button("🧹 Matı Temizle / Dersi Bitir"):
            st.session_state.mat_mevcut = 0
            st.rerun()

        st.markdown("---")
        st.write("📲 **Sporcu Giriş Ekranı (PIN Girişi)**")
        pin_giris = st.text_input("Sporcu PIN Kodunu Giriniz (Varsayılan: 1234)", type="password", key="pin_giris_t0")
        if st.button("✅ Derse Check-in Yap", key="btn_checkin_t0"):
            if pin_giris:
                basari, ad, yeni_ders, brans = pin_ile_yoklama_al(pin_giris)
                if basari:
                    st.session_state.mat_mevcut += 1
                    st.success(f"🎉 **{ad}** ({brans}) Başarıyla Derse Katıldı! Toplam Katıldığı Ders: **{yeni_ders}**")
                    st.rerun()
                else:
                    st.error("❌ Hatalı PIN Kodu! Kayıtlı sporcu bulunamadı.")

    # --- TAB 1: QR & ÜYE SELF-SERVİS PORTAL (YENİ MODÜL!) ---
    with tab1:
        st.subheader("🌐 Akıllı Üye Self-Servis Portal (QR Giriş Alanı)")
        st.markdown("Sporcularınız salondaki QR kodu okutarak veya PIN kodu ile kendi panellerine girip durumlarını anlık takip edebilirler.")
        
        uyeler = uyeleri_getir()
        if uyeler:
            portal_pin = st.text_input("🔐 Üye Girişi İçin PIN Kodunuzu Girin (Örn: 1234)", type="password", key="portal_pin_input")
            if st.button("🚀 Portalime Giriş Yap", key="btn_portal_giris"):
                bulunan_uye = [u for u in uyeler if u[8] == portal_pin]
                if bulunan_uye:
                    u = bulunan_uye[0]
                    u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d, u_sinav_t, u_pin, u_ders, u_grup, u_v_ad, u_v_tel, u_not = u
                    
                    st.balloons()
                    st.success(f"✨ Hoş geldin, **{u_ad}**! RingMaster Kişisel Üye Paneline Başarıyla Giriş Yaptın.")
                    
                    p_col1, p_col2, p_col3 = st.columns(3)
                    p_col1.metric("🥋 Mevcut Kuşak", u_kusak)
                    p_col2.metric("📊 Katıldığın Ders", f"{u_ders} Ders")
                    p_col3.metric("💳 Aidat Durumu", u_aidat_d)
                    
                    st.markdown("---")
                    st.markdown("### 📋 Kişisel Gelişim & Hoca Notu")
                    st.info(f"📝 {u_not}")
                    
                    kalan_sinav_ders = max(0, BARAJ_DERS_SAYISI - u_ders)
                    if u_ders >= BARAJ_DERS_SAYISI:
                        st.success(f"🏆 Tebrikler! Kuşak sınavına girmeye hak kazandın! ({u_ders}/{BARAJ_DERS_SAYISI} ders)")
                    else:
                        st.warning(f"⏳ Sonraki Kuşak Sınavı İçin Kalan Ders: **{kalan_sinav_ders} Ders**")
                else:
                    st.error("❌ Hatalı PIN Kodu! Lütfen salon yönetimine danışın.")
            
            st.markdown("---")
            st.markdown("### 📱 Salon QR Portal Bağlantı Bilgisi")
            st.info("💡 Salonunuzun duvarına asabileceğiniz QR kod bu Streamlit uygulama adresine yönlendirilir. Sporcular kameralarını okutarak doğrudan bu sayfaya erişip PIN kodlarıyla kendi panellerini açabilirler!")
        else:
            st.warning("Henüz kayıtlı üye bulunmuyor.")

    # --- TAB 2: ANTRENÖR HAKEDİŞ & PRİM ---
    with tab2:
        st.subheader("💵 Antrenör Hakediş, Prim & Aylık Ciro Raporu")
        st.markdown("Antrenörlerin maaş, ders saati ve ciro primlerini hesaplayıp çift kanalla (WhatsApp / SMS) bildirin.")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("### 👨‍🏫 Yeni Antrenör Tanımla")
            with st.form("antrenor_form", clear_on_submit=True):
                ant_ad = st.text_input("Antrenör Adı Soyadı")
                ant_tel = st.text_input("Telefon (örn: 905xxxxxxxxx)")
                ant_brans = st.selectbox("Uzmanlık / Branş", ["Baş Antrenör (Head Coach)", "Boks Antrenörü", "Kickboks & Muay Thai Eğitmeni", "Fitness & PT Eğitmeni"])
                
                ant_maas_tipi = st.selectbox("Maaş & Ödeme Modeli", ["Sabit Maaş + Prim %", "Sadece Ders Başı / Ciro Primi", "Sabit Maaş"])
                ant_sabit = st.number_input("Sabit Maaş (TL)", min_value=0.0, value=15000.0, step=1000.0)
                ant_prim = st.number_input("Ciro / Ders Prim Oranı (%)", min_value=0.0, max_value=100.0, value=35.0, step=1.0)
                
                submit_ant = st.form_submit_button("➕ Antrenörü Kaydet")
                if submit_ant and ant_ad and ant_tel:
                    antrenor_ekle(ant_ad, ant_tel, ant_brans, ant_maas_tipi, ant_sabit, ant_prim)
                    st.success(f"'{ant_ad}' başarıyla sisteme eklendi!")
                    st.rerun()

        with col_h2:
            st.markdown("### 📊 Aylık Hakediş & Ciro Simülasyonu")
            antrenorler = antrenorleri_getir()
            if antrenorler:
                sec_ant_str = st.selectbox("Hakedişi Hesaplanacak Antrenör", [f"{a[1]} ({a[3]})" for a in antrenorler])
                ant_data = [a for a in antrenorler if f"{a[1]} ({a[3]})" == sec_ant_str][0]
                
                a_id, a_ad, a_tel, a_brans, a_m_tip, a_sabit, a_prim_y = ant_data
                
                st.write(f"📋 **Model:** {a_m_tip} | Sabit: **{a_sabit:,.0f} TL** | Prim: **%{a_prim_y}**")
                
                sim_ciro = st.number_input("Bu Ay Antrenörün Ürettiği Toplam PT/Grup Cirosu (TL)", min_value=0.0, value=30000.0, step=1000.0)
                sim_ders_sayisi = st.number_input("Bu Ay Verilen Toplam Ders Saati", min_value=0, value=40)
                
                hesaplanan_prim = sim_ciro * (a_prim_y / 100.0)
                toplam_net_hakedis = (a_sabit if "Sabit" in a_m_tip else 0.0) + hesaplanan_prim
                
                st.success(f"💰 **TOPLAM NET HAKEDİŞ: {toplam_net_hakedis:,.0f} TL**\n\n*(Sabit: {a_sabit:,.0f} TL + Prim ({a_prim_y}%): {hesaplanan_prim:,.0f} TL)*")
                
                ant_mesaj = f"Hocam selam {a_ad}, RingMaster Salonu {datetime.date.today().strftime('%B %Y')} dönemi hakediş raporun: Verilen Ders: {sim_ders_sayisi} Saat | Üretilen Ciro: {sim_ciro:,.0f} TL | Toplam Net Hakediş: {toplam_net_hakedis:,.0f} TL. Emeğine sağlık! 🥊"
                
                enc_ant = urllib.parse.quote(ant_mesaj)
                wa_ant_url = f"https://wa.me/{a_tel}?text={enc_ant}"
                sms_ant_url = f"sms:{a_tel}?body={enc_ant}"
                
                col_ab1, col_ab2 = st.columns(2)
                with col_ab1:
                    st.markdown(f'<a href="{wa_ant_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Hakediş At</button></a>', unsafe_allow_html=True)
                with col_ab2:
                    st.markdown(f'<a href="{sms_ant_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS Hakediş At</button></a>', unsafe_allow_html=True)
            else:
                st.info("Kayıtlı antrenor bulunmuyor. Soldan antrenör ekleyin.")

        st.markdown("---")
        st.subheader("📋 Salon Antrenörleri Kadrosu")
        if antrenorler:
            for ant in antrenorler:
                st.write(f"👨‍🏫 **{ant[1]}** ({ant[3]}) | 📞 {ant[2]} | Model: `{ant[4]}` | Sabit: {ant[5]:,.0f} TL | Prim: %{ant[6]}")
                st.markdown("---")
        else:
            st.info("Henüz antrenör kaydı yok.")

    # --- TAB 3: ÇOCUK VELİ GELİŞİM RAPORU ---
    with tab3:
        st.subheader("👶 Çocuk Grupları Veli Bilgilendirme & Gelişim Raporu (WhatsApp & SMS)")
        uyeler = uyeleri_getir()
        cocuklar = [u for u in uyeler if u[10] == "Çocuk Grubu (Minik/Yıldız)"]
        
        if cocuklar:
            secili_cocuk_str = st.selectbox("Raporu Düzenlenecek Çocuk Sporcuyu Seç", [f"{c[1]} ({c[3]} - Veli: {c[11]})" for c in cocuklar])
            c_data = [c for c in cocuklar if f"{c[1]} ({c[3]} - Veli: {c[11]})" == secili_cocuk_str][0]
            
            c_id, c_ad, c_tel, c_brans, c_kusak, c_aidat_t, c_aidat_d, c_sinav_t, c_pin, c_ders, c_grup, c_veli_ad, c_veli_tel, c_not = c_data

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown(f"### 📋 Sporcu & Veli Künyesi")
                st.write(f"👤 **Çocuk Sporcu:** {c_ad}")
                st.write(f"🥋 **Mevcut Kuşak / Seviye:** {c_kusak}")
                st.write(f"📊 **Toplam Katıldığı Ders:** {c_ders} Ders")
                st.write(f"👥 **Veli Adı Soyadı:** {c_veli_ad if c_veli_ad else 'Belirtilmemiş'}")
                st.write(f"📞 **Veli Telefonu:** {c_veli_tel if c_veli_tel else c_tel}")

            with col_r2:
                st.markdown(f"### ✍️ Antrenör Gelişim & Performans Notu")
                yeni_gelisim_notu = st.text_area("Hoca Gelişim Raporu Notu", value=c_not, height=100, key="txt_gelisim_notu_t3")
                if st.button("💾 Gelişim Notunu Kaydet", key=f"btn_not_{c_id}"):
                    cocuk_rapor_guncelle(c_id, yeni_gelisim_notu)
                    st.success("Çocuğun gelişim raporu güncellendi!")
                    st.rerun()

            st.markdown("---")
            veli_hedef_tel = c_veli_tel if c_veli_tel else c_tel
            veli_hitap = c_veli_ad if c_veli_ad else "Sayın Veli"
            
            veli_mesaj = f"Merhaba {veli_hitap}, RingMaster Spor Kulübü'nden çocuğunuz {c_ad} ({c_brans}) için aylık Gelişim & Katılım Raporu: \n\n🥋 Kuşak/Seviye: {c_kusak}\n📊 Toplam Katıldığı Ders: {c_ders}\n📝 Hoca Notu: {yeni_gelisim_notu}\n\nÇocuğumuzun gelişimini birlikte destekliyoruz! İyi günler dileriz. 🥊"
            
            enc_veli = urllib.parse.quote(veli_mesaj)
            wa_veli_url = f"https://wa.me/{veli_hedef_tel}?text={enc_veli}"
            sms_veli_url = f"sms:{veli_hedef_tel}?body={enc_veli}"
            
            col_v_btn1, col_v_btn2 = st.columns(2)
            with col_v_btn1:
                st.markdown(f'<a href="{wa_veli_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:6px;cursor:pointer;font-weight:bold;font-size:15px;">📲 WhatsApp ile Veliye Gelişim Raporu At</button></a>', unsafe_allow_html=True)
            with col_v_btn2:
                st.markdown(f'<a href="{sms_veli_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:6px;cursor:pointer;font-weight:bold;font-size:15px;">💬 SMS ile Veliye Gelişim Raporu At</button></a>', unsafe_allow_html=True)
        else:
            st.info("Kayıtlı çocuk grubu sporcusu bulunmuyor.")

    # --- TAB 4: EKİPMAN SATIŞ POS & STOK ---
    with tab4:
        st.subheader("🛍️ Salon İçi Mini Ekipman Satış POS & Stok Paneli")
        col_pos1, col_pos2 = st.columns(2)
        
        with col_pos1:
            st.markdown("### 🛒 Hızlı POS Kasa Satışı")
            urunler = urunleri_getir()
            if urunler:
                secilen_u_str = st.selectbox("Satılacak Ürünü Seç", [f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" for u in urunler], key="sel_urun_pos_t4")
                u_id = [u[0] for u in urunler if f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" == secilen_u_str][0]
                u_stok = [u[3] for u in urunler if f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" == secilen_u_str][0]
                u_fiyat = [u[5] for u in urunler if f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" == secilen_u_str][0]

                if u_stok <= 0:
                    st.error("🚨 ÜRÜN STOKTA TÜKENDİ!")
                else:
                    satis_adet = st.number_input("Satış Adedi", min_value=1, max_value=int(u_stok), value=1, key="num_satis_adet_t4")
                    toplam_pos_tutar = satis_adet * u_fiyat
                    odeme_tipi = st.radio("Ödeme Tipi", ["Nakit 💵", "Kredi Kartı 💳", "Havale / EFT 📲"], horizontal=True, key="radio_odeme_t4")
                    
                    st.success(f"💰 **Toplam Tahsil Edilecek Tutar:** {toplam_pos_tutar:,.0f} TL")
                    if st.button("🛒 SATIŞI TAMAMLAT & KASAYA İŞLE", key="btn_satis_tamamla_t4"):
                        urun_satisi_yap(u_id, satis_adet, toplam_pos_tutar, odeme_tipi)
                        st.balloons()
                        st.success("🎉 Satış Başarıyla Gerçekleşti!")
                        st.rerun()
            else:
                st.info("Kayıtlı ürün bulunmuyor.")

        with col_pos2:
            st.markdown("### 📦 Yeni Ekipman / Ürün Ekle")
            with st.form("urun_form_t4", clear_on_submit=True):
                u_adi = st.text_input("Ürün Adı")
                u_kat = st.selectbox("Kategori", ["Eldiven & Koruyucu", "Bandaj & Dişlik", "Tekstil / Giyim", "İçecek & Takviye", "Diğer"])
                u_stok_m = st.number_input("Stok Miktarı (Adet)", min_value=1, value=10)
                c_u1, c_u2 = st.columns(2)
                u_alis = c_u1.number_input("Maliyet / Alış (TL)", min_value=0.0, value=500.0)
                u_satis = c_u2.number_input("Satış Fiyatı (TL)", min_value=0.0, value=1000.0)
                
                submit_u = st.form_submit_button("📦 Ürünü Stoklara Ekle")
                if submit_u and u_adi:
                    urun_ekle(u_adi, u_kat, u_stok_m, u_alis, u_satis)
                    st.success("Ürün eklendi!")
                    st.rerun()

    # --- TAB 5: KUŞAK SINAV UYGUNLUK TAKİBİ ---
    with tab5:
        st.subheader("🥋 Otomatik Kuşak Derece Sınavı Uygunluk Takibi")
        uyeler = uyeleri_getir()
        if uyeler:
            for u in uyeler:
                u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d, u_sinav_t, u_pin, u_ders, u_grup, u_veli_ad, u_veli_tel, u_not = u
                c_k1, c_k2, c_k3 = st.columns([3, 3, 2])
                c_k1.write(f"👤 **{u_ad}** ({u_brans}) | Mevcut: **{u_kusak}** | PIN: `{u_pin}`")
                
                kalan_ders = max(0, BARAJ_DERS_SAYISI - u_ders)
                if u_ders >= BARAJ_DERS_SAYISI:
                    c_k2.success(f"🟢 **SINAVA GİRMEYE HAK KAZANDI!** ({u_ders}/{BARAJ_DERS_SAYISI})")
                else:
                    c_k2.warning(f"⏳ **Sınava Kalan: {kalan_ders} Ders**")
                
                if c_k3.button("🥋 +1 Manuel Ders", key=f"btn_ders_{u_id}"):
                    ders_sayisi_arttir(u_id)
                    st.success("Ders işlendi!")
                    st.rerun()
                
                if u_ders >= BARAJ_DERS_SAYISI:
                    yeni_k = c_k3.selectbox("Yeni Kuşak", KUSAKLAR, key=f"sel_k_{u_id}")
                    if c_k3.button("🎓 Kuşağı Yükselt", key=f"btn_yuks_{u_id}"):
                        kusak_yukselt_sifirla(u_id, yeni_k)
                        st.balloons()
                        st.success("Kuşak yükseltildi!")
                        st.rerun()
                st.markdown("---")

    # --- TAB 6: MÜSABIK & DÖVÜŞ SİCİLİ ---
    with tab6:
        st.subheader("🏆 Müsabık Sporcu & Dövüş Sicili (Fight Record)")
        uyeler = uyeleri_getir()
        if uyeler:
            secilen_f_str = st.selectbox("Sporcu Seçiniz", [f"{u[1]} ({u[3]})" for u in uyeler], key="sel_f_rec_t6")
            f_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_f_str][0]
            m_data = musabik_getir(f_id)
            
            with st.form("musabik_form_t6"):
                f_stili = st.selectbox("Stil", ["Ortodoks (Sağak)", "Southpaw (Solak)", "Switch (Çift Yönlü)"])
                f_siklet = st.number_input("Hedef Sıklet (kg)", value=70.0)
                c1, c2, c3, c4 = st.columns(4)
                f_win = c1.number_input("Galibiyet", min_value=0, value=0)
                f_loss = c2.number_input("Mağlubiyet", min_value=0, value=0)
                f_draw = c3.number_input("Beraberlik", min_value=0, value=0)
                f_ko = c4.number_input("KO/TKO", min_value=0, value=0)
                f_mac_tarihi = st.date_input("Yaklaşan Maç Tarihi", datetime.date.today())
                f_org = st.text_input("Organizasyon", "Gala")
                
                if st.form_submit_button("💾 Kaydet"):
                    musabik_ekle_guncelle(f_id, f_stili, f_siklet, f_win, f_loss, f_draw, f_ko, f_mac_tarihi, f_org)
                    st.success("Güncellendi!")
                    st.rerun()

    # --- TAB 7: SAKATLIK & SPARRING PROTOKOLÜ ---
    with tab7:
        st.subheader("🚨 Sakatlık & Kısıtlama Protokolü")
        uyeler = uyeleri_getir()
        if uyeler:
            secilen_s_str = st.selectbox("Sporcu Seç", [f"{u[1]} ({u[3]})" for u in uyeler], key="sel_s_t7")
            s_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_s_str][0]
            
            with st.form("sak_form_t7", clear_on_submit=True):
                s_bolge = st.text_input("Sakatlık Bölgesi", "El Bileği")
                s_gun = st.number_input("Yasak Süresi (Gün)", value=14)
                s_izin = st.text_input("İzin Verilen", "Sadece Koşu")
                if st.form_submit_button("Ekle"):
                    sakatlik_ekle(s_id, s_bolge, s_gun, s_izin)
                    st.warning("Eklendi!")
                    st.rerun()

    # --- TAB 8: MAÇ HAZIRLIK TAKVİMİ ---
    with tab8:
        st.subheader("📅 Maç Hazırlık Takvimi")
        for mc in tum_yaklasan_maclari_getir():
            st.write(f"🥊 **{mc[0]}** ({mc[1]} - {mc[2]} kg) | 🏆 {mc[4]} | Tarih: {mc[3]}")
            st.markdown("---")

    # --- TAB 9: DENEME DERSİ ---
    with tab9:
        st.subheader("🥊 Deneme Dersi (Lead)")
        with st.form("d_form_t9", clear_on_submit=True):
            d_ad = st.text_input("Ad Soyad")
            d_tel = st.text_input("Telefon")
            d_brans = st.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai"])
            if st.form_submit_button("Kaydet"):
                deneme_ekle(d_ad, d_tel, d_brans, str(datetime.date.today()), "19:00", "")
                st.success("Eklendi!")

    # --- TAB 10: ÖZEL DERS (PT) ---
    with tab10:
        st.subheader("🎯 Özel Ders (PT) Paketi")
        with st.form("pt_form_t10", clear_on_submit=True):
            pt_ad = st.text_input("Sporcu Adı")
            pt_tel = st.text_input("Telefon")
            pt_seans = st.number_input("Seans", value=10)
            pt_ucret = st.number_input("Ücret", value=5000.0)
            if st.form_submit_button("Başlat"):
                ozel_ders_ekle(pt_ad, pt_tel, "PT", pt_seans, pt_ucret, "Ödendi 🟢", "")
                kasa_islem_ekle("Gelir", "PT Geliri", pt_ucret, f"{pt_ad} PT")
                st.success("Başlatıldı!")

    # --- TAB 11: ÜYE YÖNETİMİ ---
    with tab11:
        st.subheader("👤 Yeni Üye Kaydı")
        with st.form("uye_form_t11", clear_on_submit=True):
            c1, c2 = st.columns(2)
            u_ad = c1.text_input("Ad Soyad")
            u_tel = c1.text_input("Telefon")
            u_brans = c1.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Fitness"])
            u_grup = c2.selectbox("Grup", ["Yetişkin / Genel", "Çocuk Grubu (Minik/Yıldız)"])
            u_kusak = c2.selectbox("Kuşak", KUSAKLAR)
            u_pin = c2.text_input("PIN", "1234")
            if st.form_submit_button("Kaydet"):
                uye_ekle(u_ad, u_tel, u_brans, u_kusak, str(datetime.date.today()), "Ödendi", str(datetime.date.today()), u_pin, u_grup, "", "", "Yeni kayıt")
                st.success("Kaydedildi!")

    # --- TAB 12: ÖLÇÜM TAKİBİ ---
    with tab12:
        st.subheader("📈 Ölçüm Takibi")
        uyeler = uyeleri_getir()
        if uyeler:
            sec_u = st.selectbox("Sporcu", [u[1] for u in uyeler], key="sel_u_t12")
            u_id = [u[0] for u in uyeler if u[1] == sec_u][0]
            with st.form("olc_form_t12", clear_on_submit=True):
                kilo = st.number_input("Kilo", value=75.0)
                yag = st.number_input("Yağ %", value=15.0)
                if st.form_submit_button("Kaydet"):
                    olcum_ekle(u_id, kilo, yag, 80.0, 100.0, 35.0, "İyi")
                    st.success("Kaydedildi!")

    # --- TAB 13: KASA & FİNANS ---
    with tab13:
        st.subheader("📊 Kasa Paneli")
        gelir, gider, net = kasa_ozet_getir()
        c1, c2, c3 = st.columns(3)
        c1.metric("Gelir", f"{gelir:,.0f} TL")
        c2.metric("Gider", f"{gider:,.0f} TL")
        c3.metric("Net", f"{net:,.0f} TL")

    # --- TAB 14: CHURN RİSKİ ---
    with tab14:
        st.subheader("🚨 Riskli Üyeler")
        for u in uykudaki_uyeleri_getir():
            st.write(f"👤 **{u[1]}** | Aidat Bekliyor | Tel: {u[2]}")

    # --- TAB 15: İLETİŞİM OTOMASYONU ---
    with tab15:
        st.subheader("📱 İletişim Otomasyonu")
        st.info("WhatsApp ve SMS entegrasyonu aktif.")

                
                

    
 

            
    

