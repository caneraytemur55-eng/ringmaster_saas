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
    tum_yaklasan_maclari_getir, urun_ekle, urunleri_getir, urun_satisi_yap
)

# Veritabanı Kurulumu
init_db()

st.set_page_config(page_title="RingMaster SaaS v4.5", page_icon="🥊", layout="wide")

st.title("🥊 RingMaster SaaS v4.5 - POS & Ekipman Stok Sürümü")

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

tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
    "⚡ PIN Yoklama & Mat Kontenjanı",
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
        pin_giris = st.text_input("Sporcu PIN Kodunu Giriniz (Varsayılan: 1234)", type="password")
        if st.button("✅ Derse Check-in Yap"):
            if pin_giris:
                basari, ad, yeni_ders, brans = pin_ile_yoklama_al(pin_giris)
                if basari:
                    st.session_state.mat_mevcut += 1
                    st.success(f"🎉 **{ad}** ({brans}) Başarıyla Derse Katıldı! Toplam Katıldığı Ders: **{yeni_ders}**")
                    st.rerun()
                else:
                    st.error("❌ Hatalı PIN Kodu! Kayıtlı sporcu bulunmavadı.")

    # --- TAB 1: EKİPMAN SATIŞ POS & STOK PANENİ (YENİ MODÜL!) ---
    with tab1:
        st.subheader("🛍️ Salon İçi Mini Ekipman Satış POS & Stok Paneli")
        col_pos1, col_pos2 = st.columns(2)
        
        # SOL SÜTUN: HIZLI POS KASA SATIŞI
        with col_pos1:
            st.markdown("### 🛒 Hızlı POS Kasa Satışı")
            urunler = urunleri_getir()
            if urunler:
                secilen_u_str = st.selectbox("Satılacak Ürünü Seç", [f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" for u in urunler])
                u_id = [u[0] for u in urunler if f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" == secilen_u_str][0]
                u_stok = [u[3] for u in urunler if f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" == secilen_u_str][0]
                u_fiyat = [u[5] for u in urunler if f"{u[1]} ({u[2]} - Stok: {u[3]} Adet - Fiyat: {u[5]:,.0f} TL)" == secilen_u_str][0]

                if u_stok <= 0:
                    st.error("🚨 ÜRÜN STOKTA TÜKENDİ! Satış yapabilmek için stok ekleyiniz.")
                else:
                    satis_adet = st.number_input("Satış Adedi", min_value=1, max_value=int(u_stok), value=1)
                    toplam_pos_tutar = satis_adet * u_fiyat
                    odeme_tipi = st.radio("Ödeme Tipi", ["Nakit 💵", "Kredi Kartı 💳", "Havale / EFT 📲"], horizontal=True)
                    
                    st.success(f"💰 **Toplam Tahsil Edilecek Tutar:** {toplam_pos_tutar:,.0f} TL")
                    if st.button("🛒 SATIŞI TAMAMLAT & KASAYA İŞLE"):
                        urun_satisi_yap(u_id, satis_adet, toplam_pos_tutar, odeme_tipi)
                        st.balloons()
                        st.success(f"🎉 Satış Başarıyla Gerçekleşti! {toplam_pos_tutar:,.0f} TL Kasaya Gelir Olarak İşlendi!")
                        st.rerun()
            else:
                st.info("Kayıtlı ürün bulunmuyor. Sağ taraftan yeni ürün ekleyiniz.")

        # SAĞ SÜTUN: STOK VE ÜRÜN EKLEME
        with col_pos2:
            st.markdown("### 📦 Yeni Ekipman / Ürün Ekle")
            with st.form("urun_form", clear_on_submit=True):
                u_adi = st.text_input("Ürün Adı (Örn: 16oz Boks Eldiveni)")
                u_kat = st.selectbox("Kategori", ["Eldiven & Koruyucu", "Bandaj & Dişlik", "Tekstil / Giyim", "İçecek & Takviye", "Diğer"])
                u_stok_m = st.number_input("Stok Miktarı (Adet)", min_value=1, value=10)
                
                c_u1, c_u2 = st.columns(2)
                u_alis = c_u1.number_input("Maliyet / Alış (TL)", min_value=0.0, value=500.0)
                u_satis = c_u2.number_input("Satış Fiyatı (TL)", min_value=0.0, value=1000.0)
                
                submit_u = st.form_submit_button("📦 Ürünü Stoklara Ekle")
                if submit_u and u_adi:
                    urun_ekle(u_adi, u_kat, u_stok_m, u_alis, u_satis)
                    st.success(f"'{u_adi}' ürünü envantere eklendi!")
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📋 Envanterdeki Ürünler ve Stok Durumu")
        urunler_tum = urunleri_getir()
        if urunler_tum:
            for ur in urunler_tum:
                u_id, u_ad, u_kat, u_stk, u_al, u_sat = ur
                stok_alert = "🚨 **KRİTİK DÜŞÜK STOK!**" if u_stk <= 3 else "🟢 **Stok Yeterli**"
                st.write(f"📦 **{u_ad}** ({u_kat}) | Stok: **{u_stk} Adet** ({stok_alert}) | Alış: {u_al:,.0f} TL -> Satış: **{u_sat:,.0f} TL**")
                st.markdown("---")

    # --- TAB 2: KUŞAK SINAV UYGUNLUK TAKİBİ ---
    with tab2:
        st.subheader("🥋 Otomatik Kuşak Derece Sınavı Uygunluk Takibi")
        st.caption(f"Bir sonraki kuşak sınavına girmek için baraj: **{BARAJ_DERS_SAYISI} Katılım Dersi**")
        
        uyeler = uyeleri_getir()
        if uyeler:
            for u in uyeler:
                u_id, u_ad, u_tel, u_brans, u_kusak, u_aidat_t, u_aidat_d, u_sinav_t, u_pin, u_ders = u
                
                c_k1, c_k2, c_k3 = st.columns([3, 3, 2])
                c_k1.write(f"👤 **{u_ad}** ({u_brans})\n\n🥋 Mevcut: **{u_kusak}** | PIN: `{u_pin}`")
                
                kalan_ders = max(0, BARAJ_DERS_SAYISI - u_ders)
                if u_ders >= BARAJ_DERS_SAYISI:
                    c_k2.success(f"🟢 **SINAVA GİRMEYE HAK KAZANDI!**\n\nToplanan: **{u_ders} / {BARAJ_DERS_SAYISI} Ders**")
                else:
                    c_k2.warning(f"⏳ **Sınava Kalan: {kalan_ders} Ders**\n\nTamamlanan: {u_ders} / {BARAJ_DERS_SAYISI}")
                
                if c_k3.button("🥋 +1 Manuel Derse Katıldı", key=f"btn_ders_{u_id}"):
                    ders_sayisi_arttir(u_id)
                    st.success(f"{u_ad} için +1 ders işlendi!")
                    st.rerun()
                
                if u_ders >= BARAJ_DERS_SAYISI:
                    yeni_k = c_k3.selectbox("Yeni Kuşak Seç", KUSAKLAR, key=f"sel_k_{u_id}")
                    if c_k3.button("🎓 Kuşağı Yükselt & Sıfırla", key=f"btn_yuks_{u_id}"):
                        kusak_yukselt_sifirla(u_id, yeni_k)
                        st.balloons()
                        st.success(f"{u_ad} resmen **{yeni_k}** seviyesine yükseltildi!")
                        st.rerun()
                        
                    msg_sinav = f"Tebrikler {u_ad}! RingMaster Salonu'nda {BARAJ_DERS_SAYISI} derslik devamlılığını tamamlayarak Kuşak Sınavı'na girmeye hak kazandın! Sınav saatini öğrenmek için dönüş yapabilirsin. 🥋"
                    enc_s = urllib.parse.quote(msg_sinav)
                    wa_sinav_url = f"https://wa.me/{u_tel}?text={enc_s}"
                    c_k3.markdown(f'<a href="{wa_sinav_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:8px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 Sınav Davetiyesi At</button></a>', unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("Kayıtlı sporcu bulunmuyor.")

    # --- TAB 3: MÜSABIK & DÖVÜŞ SİCİLİ ---
    with tab3:
        st.subheader("🏆 Müsabık Sporcu, Sıklet & Dövüş Sicili (Fight Record)")
        uyeler = uyeleri_getir()
        if uyeler:
            secilen_f_str = st.selectbox("Sporcu Seçiniz", [f"{u[1]} ({u[3]})" for u in uyeler], key="sel_f_rec")
            f_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_f_str][0]
            f_ad = [u[1] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_f_str][0]

            m_data = musabik_getir(f_id)
            stili_def = m_data[1] if m_data else 'Ortodoks (Sağak)'
            siklet_def = m_data[2] if m_data else 70.0
            g_def = m_data[3] if m_data else 0
            m_def = m_data[4] if m_data else 0
            b_def = m_data[5] if m_data else 0
            ko_def = m_data[6] if m_data else 0
            mac_t_def = datetime.datetime.strptime(m_data[7], "%Y-%m-%d").date() if (m_data and m_data[7]) else datetime.date.today()
            org_def = m_data[8] if m_data else "Türkiye Şampiyonası / Gala"

            with st.form("musabik_form"):
                f_stili = st.selectbox("Dövüş Stili / Duruş", ["Ortodoks (Sağak)", "Southpaw (Solak)", "Switch (Çift Yönlü)"], index=["Ortodoks (Sağak)", "Southpaw (Solak)", "Switch (Çift Yönlü)"].index(stili_def) if stili_def in ["Ortodoks (Sağak)", "Southpaw (Solak)", "Switch (Çift Yönlü)"] else 0)
                f_siklet = st.number_input("Hedef Maç Sıkleti (kg)", min_value=40.0, max_value=150.0, value=float(siklet_def), step=0.5)
                
                c_rec1, c_rec2, c_rec3, c_rec4 = st.columns(4)
                f_win = c_rec1.number_input("Galibiyet (W)", min_value=0, value=int(g_def))
                f_loss = c_rec2.number_input("Mağlubiyet (L)", min_value=0, value=int(m_def))
                f_draw = c_rec3.number_input("Beraberlik (D)", min_value=0, value=int(b_def))
                f_ko = c_rec4.number_input("KO / TKO", min_value=0, value=int(ko_def))
                
                f_mac_tarihi = st.date_input("Yaklaşan Maç Tarihi", mac_t_def)
                f_org = st.text_input("Organizasyon / Şampiyona Adı", org_def)
                
                submit_musabik = st.form_submit_button("💾 Dövüş Sicilini & Maç Tarihini Kaydet")
                if submit_musabik:
                    musabik_ekle_guncelle(f_id, f_stili, f_siklet, f_win, f_loss, f_draw, f_ko, f_mac_tarihi, f_org)
                    st.success("Sporcunun dövüş profili, sicili ve yaklaşan maç tarihi güncellendi!")
                    st.rerun()

            st.markdown("---")
            if m_data:
                st.success(f"🏆 **FIGHT RECORD:** `{g_def}-W / {m_def}-L / {b_def}-D ({ko_def} KO)`")
                st.write(f"🎯 **Hedef Sıklet:** {siklet_def} kg | 🥊 **Stil:** {stili_def}")
                st.write(f"🗓️ **Yaklaşan Maç:** {m_data[7]} | **Organizasyon:** {org_def}")
        else:
            st.warning("Önce 'Üye Yönetimi' sekmesinden sporcu kaydı yapmalısınız.")

    # --- TAB 4: SAKATLIK & SPARRING PROTOKOLÜ ---
    with tab4:
        st.subheader("🚨 Sakatlık & Sparring/Temas Kısıtlama Protokolü")
        uyeler = uyeleri_getir()
        if uyeler:
            secilen_s_str = st.selectbox("Sakatlık Kaydı Girilecek Sporcu", [f"{u[1]} ({u[3]})" for u in uyeler], key="sel_s_prot")
            s_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_s_str][0]
            s_ad = [u[1] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_s_str][0]

            with st.form("sakatlik_form", clear_on_submit=True):
                s_bolge = st.text_input("Sakatlık Bölgesi / Tanı", "Örn: Burun Kırığı / Sağ El Bileği Burkulması")
                s_gun = st.number_input("Sparring & Temas Yasağı Süresi (Gün)", min_value=1, max_value=180, value=14)
                s_izin = st.text_input("İzin Verilen Antrenman Türü", "Örn: Sadece Koşu, İp Atlama ve Gölge Boksu Yapabilir")
                
                submit_sak = st.form_submit_button("🚨 Sakatlık & Kısıtlama Ekle")
                if submit_sak:
                    sakatlik_ekle(s_id, s_bolge, s_gun, s_izin)
                    st.warning("Sakatlık ve Sparring kısıtlaması sisteme işlendi!")
                    st.rerun()

            st.markdown("---")
            st.subheader(f"🩹 {s_ad} - Aktif & Geçmiş Sakatlıklar")
            sak_listesi = sakatliklari_getir(s_id)
            if sak_listesi:
                for sak in sak_listesi:
                    sak_id, sak_b, sak_g, sak_iz, sak_t, sak_durum = sak
                    if sak_durum == "Aktif Sakatlık 🔴":
                        st.error(f"🔴 **{sak_durum}** | **{sak_b}**\n\n⛔ **{sak_g} Gün Sparring Yapamaz!**\n\n🟢 İzin Verilen: {sak_iz} (Tarih: {sak_t})")
                        if st.button("🟢 İyileşti Olarak İşaretle", key=f"btn_sak_{sak_id}"):
                            sakatlik_kapat(sak_id)
                            st.success("Sporcu iyileşti olarak güncellendi!")
                            st.rerun()
                    else:
                        st.success(f"🟢 **{sak_durum}** | {sak_b} (Süre: {sak_g} Gün)")
                    st.markdown("---")
            else:
                st.info("Bu sporcunun aktif bir sakatlık veya sparring kısıtlaması bulunmuyor.")
        else:
            st.warning("Önce 'Üye Yönetimi' sekmesinden sporcu kaydı yapmalısınız.")

    # --- TAB 5: MAÇ HAZIRLIK TAKVİMİ & GERİ SAYIM ---
    with tab5:
        st.subheader("📅 Salon Genel Maç Hazırlık Takvimi & Geri Sayım")
        st.caption("Salondaki tüm müsabık sporcuların yaklaşan maçları ve canlı geri sayım kronometresi.")
        
        maclar_listesi = tum_yaklasan_maclari_getir()
        if maclar_listesi:
            for mc in maclar_listesi:
                mc_ad, mc_brans, mc_siklet, mc_tarih_str, mc_org, mc_tel = mc
                try:
                    mc_dt = datetime.datetime.strptime(mc_tarih_str, "%Y-%m-%d").date()
                    kalan_mac_gunu = (mc_dt - datetime.date.today()).days
                except Exception:
                    kalan_mac_gunu = 0

                c_m1, c_m2, c_m3 = st.columns([3, 3, 2])
                c_m1.write(f"🥊 **{mc_ad}** ({mc_brans} - {mc_siklet} kg)\n\n🏆 Organizasyon: **{mc_org}**")
                
                if kalan_mac_gunu > 7:
                    c_m2.info(f"🗓️ Maç Tarihi: **{mc_tarih_str}**\n\n⏳ Kalan Süre: **{kalan_mac_gunu} Gün**")
                elif kalan_mac_gunu >= 0:
                    c_m2.warning(f"🚨 **MAÇA SON {kalan_mac_gunu} GÜN!** (Kilo düşme & Lapa Dönemi)")
                else:
                    c_m2.success(f"✅ Maç Tamamlandı / Tarih Geçti ({mc_tarih_str})")
                    
                msg_mac = f"Selam {mc_ad}! RingMaster Salonu'nda {mc_org} organizasyonundaki maçına son {kalan_mac_gunu} gün kaldı! Sıkletini korumayı ve lapa antrenmanlarını aksatmamayı unutma! 🥊"
                enc_mc = urllib.parse.quote(msg_mac)
                wa_mc_url = f"https://wa.me/{mc_tel}?text={enc_mc}"
                c_m3.markdown(f'<a href="{wa_mc_url}" target="_blank"><button style="background-color:#007AFF;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 Maç Motivasyon Bildirimi At</button></a>', unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("Henüz eklenmiş yaklaşan bir maç bulunmuyor.")

    # --- TAB 6: DENEME DERSİ ---
    with tab6:
        st.subheader("🥊 Potansiyel Sporcu Deneme Dersi Kaydı")
        with st.form("deneme_form", clear_on_submit=True):
            col_d1, col_d2 = st.columns(2)
            d_ad = col_d1.text_input("Aday Sporcu Adı Soyadı")
            d_tel = col_d1.text_input("Telefon (örn: 905xxxxxxxxx)")
            d_brans = col_d1.selectbox("İlgilendiği Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness"])
            d_tarih = col_d2.date_input("Deneme Dersi Tarihi", datetime.date.today())
            d_saat = col_d2.time_input("Deneme Dersi Saati", datetime.time(19, 0))
            d_not = col_d2.text_input("Not", "")
            
            submit_d = st.form_submit_button("➕ Deneme Dersi Kaydet")
            if submit_d and d_ad and d_tel:
                deneme_ekle(d_ad, d_tel, d_brans, str(d_tarih), str(d_saat), d_not)
                st.success(f"{d_ad} kaydoldu!")

        st.markdown("---")
        st.subheader("📌 Deneme Dersleri Listesi")
        denemeler = denemeleri_getir()
        if denemeler:
            for den in denemeler:
                st.write(f"👤 **{den[1]}** ({den[3]}) - 📞 {den[2]} | 🗓️ {den[4]} {den[5]} | Durum: `{den[6]}`")
        else:
            st.info("Planlanmış deneme dersi yok.")

    # --- TAB 7: ÖZEL DERS (PT) & ÜCRET TAKİBİ ---
    with tab7:
        st.subheader("🥊 Birebir Özel Ders (PT) Paketi Tanımla")
        with st.form("pt_form", clear_on_submit=True):
            col_p1, col_p2 = st.columns(2)
            pt_ad = col_p1.text_input("Özel Ders Sporcu Adı Soyadı")
            pt_tel = col_p1.text_input("Telefon (örn: 905xxxxxxxxx)")
            pt_brans = col_p1.selectbox("Branş / Konsept", ["Boks Özel Ders", "Kickboks PT", "Muay Thai PT", "Kilo Verme / Fitness PT"])
            
            pt_seans = col_p2.number_input("Paket Toplam Seans Sayısı", min_value=1, max_value=100, value=10)
            pt_ucret = col_p2.number_input("Paket Ücreti (₺ / $)", min_value=0, value=5000)
            pt_ucret_durumu = col_p2.selectbox("Paket Ücret Ödeme Durumu", ["Ödendi 🟢", "Ödeme Bekliyor 🔴", "Kısmi Ödeme Yapıldı 🟡"])
            pt_not = col_p2.text_input("Not (Örn: Haftada 2 gün gelecek)", "")
            
            submit_pt = st.form_submit_button("➕ Özel Ders Paketini Başlat")
            if submit_pt and pt_ad and pt_tel:
                ozel_ders_ekle(pt_ad, pt_tel, pt_brans, pt_seans, pt_ucret, pt_ucret_durumu, pt_not)
                if "Ödendi" in pt_ucret_durumu:
                    kasa_islem_ekle("Gelir", "PT Ödemesi", pt_ucret, f"{pt_ad} PT Paket Ücreti")
                st.success(f"🎉 {pt_ad} için {pt_seans} seanslık özel ders paketi açıldı!")

        st.markdown("---")
        st.subheader("📊 Aktif Özel Ders (PT) & Ücret Takip Tablosu")
        pt_dersler = ozel_dersleri_getir()
        if pt_dersler:
            for pt in pt_dersler:
                pt_id, pt_ad, pt_tel, pt_brans, pt_toplam, pt_kalan, pt_ucret, pt_durum, pt_tarih, pt_not = pt
                
                c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
                c1.write(f"👤 **{pt_ad}** ({pt_brans})\n\n📞 {pt_tel}")
                
                durum_emoji = "🔴 **PAKET BİTTİ!**" if pt_kalan == 0 else f"🟢 **{pt_kalan} / {pt_toplam} Seans Kaldı**"
                c2.write(f"🥊 Seans Takibi:\n\n{durum_emoji}")
                c3.write(f"💰 Ücret: **{pt_ucret:,.0f} TL**\n\nDurum: **{pt_durum}**")
                
                if c4.button("🥊 1 Ders Düş (-1)", key=f"btn_seans_{pt_id}"):
                    ozel_ders_seans_dus(pt_id)
                    st.success("1 Seans düşüldü!")
                    st.rerun()
                    
                yeni_pt_ucret_d = c4.selectbox("Ödeme Durumu", ["Ödendi 🟢", "Ödeme Bekliyor 🔴", "Kısmi Ödeme Yapıldı 🟡"], index=["Ödendi 🟢", "Ödeme Bekliyor 🔴", "Kısmi Ödeme Yapıldı 🟡"].index(pt_durum) if pt_durum in ["Ödendi 🟢", "Ödeme Bekliyor 🔴", "Kısmi Ödeme Yapıldı 🟡"] else 1, key=f"select_pt_{pt_id}")
                if yeni_pt_ucret_d != pt_durum:
                    ozel_ders_ucret_guncelle(pt_id, yeni_pt_ucret_d)
                    if "Ödendi" in yeni_pt_ucret_d:
                        kasa_islem_ekle("Gelir", "PT Ödemesi", pt_ucret, f"{pt_ad} PT Ödemesi Alındı")
                    st.success("Ödeme durumu güncellendi!")
                    st.rerun()
                st.markdown("---")
        else:
            st.info("Kayıtlı özel ders paketi bulunmuyor.")

    # --- TAB 8: ÜYE YÖNETİMİ ---
    with tab8:
        st.subheader("Yeni Sporcu Kaydı")
        with st.form("uye_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            ad_soyad = col1.text_input("Adı Soyadı")
            telefon = col1.text_input("Telefon (örn: 905xxxxxxxxx)")
            brans = col1.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness"])
            kusak = col2.selectbox("Mevcut Kuşak", KUSAKLAR)
            pin_kod = col2.text_input("Yoklama PIN Kodu (Örn: 1234)", "1234")
            aidat_tarihi = col2.date_input("Son Aidat Tarihi", datetime.date.today())
            aidat_durumu = col2.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
            aidat_tutari = col2.number_input("Aylık Aidat Tutarı (TL)", min_value=0, value=1500)
            
            submit = st.form_submit_button("➕ Sporcuyu Kaydet")
            if submit and ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu, str(datetime.date.today()), pin_kod)
                if aidat_durumu == "Ödendi":
                    kasa_islem_ekle("Gelir", "Aidat", aidat_tutari, f"{ad_soyad} Üyelik Aidatı")
                st.success(f"{ad_soyad} başarıyla eklendi!")

        st.markdown("---")
        st.subheader("📋 Kayıtlı Sporcular")
        uyeler = uyeleri_getir()
        if uyeler:
            for u in uyeler:
                st.write(f"🥊 **{u[1]}** | Branş: {u[3]} | 🥋 Kuşak: **{u[4]}** | PIN: `{u[8]}` | Aidat: `{u[6]}`")
        else:
            st.info("Kayıtlı sporcu yok.")

    # --- TAB 9: SPORCU ÖLÇÜM TAKİBİ ---
    with tab9:
        st.subheader("📈 Sporcu Fiziksel Gelişim & Ölçüm Kaydı")
        uyeler = uyeleri_getir()
        if uyeler:
            secilen_uye_str = st.selectbox("Ölçüm Yapılacak Sporcuyu Seç", [f"{u[1]} ({u[3]})" for u in uyeler])
            uye_id = [u[0] for u in uyeler if f"{u[1]} ({u[3]})" == secilen_uye_str][0]
            
            with st.form("olcum_form", clear_on_submit=True):
                col_o1, col_o2, col_o3 = st.columns(3)
                o_kilo = col_o1.number_input("Kilo (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
                o_yag = col_o1.number_input("Yağ Oranı (%)", min_value=3.0, max_value=60.0, value=15.0, step=0.1)
                
                o_bel = col_o2.number_input("Bel Çevresi (cm)", min_value=40.0, max_value=200.0, value=80.0, step=0.5)
                o_gogus = col_o2.number_input("Göğüs Çevresi (cm)", min_value=50.0, max_value=200.0, value=100.0, step=0.5)
                
                o_pazu = col_o3.number_input("Pazu Çevresi (cm)", min_value=20.0, max_value=70.0, value=35.0, step=0.5)
                o_not = col_o3.text_input("Ölçüm Notu / Hedef", "Formda görünüş iyi, yağ oranı düşüyor.")
                
                submit_olcum = st.form_submit_button("📏 Yeni Ölçümü Kaydet")
                if submit_olcum:
                    olcum_ekle(uye_id, o_kilo, o_yag, o_bel, o_gogus, o_pazu, o_not)
                    st.success("Sporcunun yeni fiziksel ölçümü kaydedildi!")
                    st.rerun()

            st.markdown("---")
            st.subheader(f"📊 {secilen_uye_str} - Ölçüm Geçmişi")
            olcum_gecmisi = olcumleri_getir(uye_id)
            if olcum_gecmisi:
                for olc in olcum_gecmisi:
                    st.write(f"🗓️ **{olc[1]}** | ⚖️ Kilo: **{olc[2]} kg** | 🩸 Yağ: **%{olc[3]}** | 📏 Bel: **{olc[4]} cm** | 🏋️ Göğüs: **{olc[5]} cm** | 💪 Pazu: **{olc[6]} cm**")
                    if olc[7]:
                        st.caption(f"📝 Not: {olc[7]}")
                    st.markdown("---")
            else:
                st.info("Bu sporcuya ait henüz ölçüm kaydı bulunmuyor.")
        else:
            st.warning("Ölçüm yapabilmek için önce 'Üye Yönetimi' sekmesinden sporcu kaydı oluşturmalısınız.")

    # --- TAB 10: KASA & FİNANS PANENİ ---
    with tab10:
        st.subheader("📊 Salon Kasa & Finans Durumu")
        gelir, gider, net_kar = kasa_ozet_getir()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("🟢 Toplam Gelir", f"{gelir:,.0f} TL")
        m2.metric("🔴 Toplam Gider", f"{gider:,.0f} TL")
        m3.metric("💰 Net Kasa / Kar", f"{net_kar:,.0f} TL")
        
        st.markdown("---")
        st.subheader("➕ Yeni Gelir / Gider Ekle")
        with st.form("kasa_form", clear_on_submit=True):
            col_k1, col_k2 = st.columns(2)
            k_tip = col_k1.selectbox("İşlem Tipi", ["Gider", "Gelir"])
            k_kat = col_k1.selectbox("Kategori", ["Kira", "Fatura (Elektrik/Su/İnternet)", "Antrenör Maaşı", "Ekipman Alımı", "Aidat Geliri", "PT Geliri", "Diğer"])
            k_tutar = col_k2.number_input("Tutar (TL)", min_value=1.0, value=1000.0)
            k_aciklama = col_k2.text_input("Açıklama / Not", "")
            
            submit_kasa = st.form_submit_button("💾 İşlemi Kasaya İşle")
            if submit_kasa:
                kasa_islem_ekle(k_tip, k_kat, k_tutar, k_aciklama)
                st.success(f"{k_tip} işlemi kasaya eklendi!")
                st.rerun()

        st.markdown("---")
        st.subheader("📜 Son Kasa Hareketleri")
        kasa_kayitlari = kasa_islemleri_getir()
        if kasa_kayitlari:
            for k in kasa_kayitlari:
                emoji = "🟢" if k[1] == "Gelir" else "🔴"
                st.write(f"{emoji} **{k[5]}** | `{k[1]}` - **{k[2]}**: **{k[3]:,.0f} TL** | Not: {k[4]}")
        else:
            st.info("Kasada henüz işlem kaydı yok.")

    # --- TAB 11: KAYIP ÜYE (CHURN RISK) UYARI MODÜLÜ ---
    with tab11:
        st.subheader("🚨 Riskli & Uykudaki Üye Erken Uyarı Paneli")
        st.write("Aidatı geciken veya salona gelmeyi aksatan üyeleri buradan tek tıkla geri kazanın.")
        
        uykudakiler = uykudaki_uyeleri_getir()
        if uykudakiler:
            for uy in uykudakiler:
                u_id, u_ad, u_tel, u_brans, u_tarih, u_durum = uy
                
                c_r1, c_r2, c_r3 = st.columns([3, 3, 2])
                c_r1.write(f"👤 **{u_ad}** ({u_brans})\n\n📞 {u_tel}")
                c_r2.write(f"🚨 Durum: **{u_durum}**\n\n🗓️ Son Tarih: {u_tarih}")
                
                mesaj = f"Merhaba {u_ad}, RingMaster Salonu'nda antrenmanları aksattığını fark ettik! 🥊 Sağlığın ve hedeflerin için salona geri dönme vakti. Bu haftaki ders programı için dönüşünü bekliyoruz!"
                enc_m = urllib.parse.quote(mesaj)
                wa_churn_url = f"https://wa.me/{u_tel}?text={enc_m}"
                
                c_r3.markdown(f'<a href="{wa_churn_url}" target="_blank"><button style="background-color:#FF3B30;color:white;width:100%;padding:10px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">🔥 Üyeyi Geri Çağır</button></a>', unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.success("🎉 Harika! Şu an aidatı geciken veya kayıp riski taşıyan üye bulunmuyor.")

    # --- TAB 12: İLETİŞİM OTOMASYONU ---
    with tab12:
        st.subheader("📱 Akıllı İletişim Otomasyon Merkezi")
        otomasyon_tipi = st.radio("İletişim Türünü Seçiniz", ["👥 Grup Dersi Aidat Hatırlatma", "🎯 Özel Ders (PT) Kalan Seans Uyarısı"], horizontal=True)
        st.markdown("---")
        
        if "Grup Dersi" in otomasyon_tipi:
            st.markdown("### 👥 Grup Dersi Sporcuları Aidat Hatırlatıcısı")
            uyeler = uyeleri_getir()
            if uyeler:
                secilen_grup_str = st.selectbox("Aidat Hatırlatılacak Sporcuyu Seç", [f"{u[1]} ({u[3]} - Aidat: {u[6]} - Tarih: {u[5]})" for u in uyeler])
                grup_data = [u for u in uyeler if f"{u[1]} ({u[3]} - Aidat: {u[6]} - Tarih: {u[5]})" == secilen_grup_str][0]
                
                varsayilan_grup_msg = f"Merhaba {grup_data[1]}, RingMaster Salonu aylık üyelik aidat tarihiniz ({grup_data[5]}) dolmuştur/yaklaşmıştır. Aidat Durumu: {grup_data[6]}. Antrenmanlarınızın aksamaması için ödemenizi tamamlayabilirsiniz. İyi antrenmanlar! 🥊"
                msg_grup_text = st.text_area("Grup Dersi Mesaj Metni", varsayilan_grup_msg, height=100)
                
                enc_grup_msg = urllib.parse.quote(msg_grup_text)
                wa_grup_url = f"https://wa.me/{grup_data[2]}?text={enc_grup_msg}"
                sms_grup_url = f"sms:{grup_data[2]}?body={enc_grup_msg}"
                
                col_g_btn1, col_g_btn2 = st.columns(2)
                with col_g_btn1:
                    st.markdown(f'<a href="{wa_grup_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp Aidat Hatırlatması At</button></a>', unsafe_allow_html=True)
                with col_g_btn2:
                    st.markdown(f'<a href="{sms_grup_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS Aidat Hatırlatması At</button></a>', unsafe_allow_html=True)
            else:
                st.info("Kayıtlı grup dersi sporcusu bulunmuyor.")

        else:
            st.markdown("### 🎯 Özel Ders (PT) Kalan Ders Sayısı Hatırlatıcısı")
            pt_dersler = ozel_dersleri_getir()
            if pt_dersler:
                secilen_pt_str = st.selectbox("Özel Ders Sporcusu Seç", [f"{p[1]} ({p[3]} - Kalan Seans: {p[5]}/{p[4]})" for p in pt_dersler])
                pt_data = [p for p in pt_dersler if f"{p[1]} ({p[3]} - Kalan Seans: {p[5]}/{p[4]})" == secilen_pt_str][0]
                
                varsayilan_pt_msg = f"Merhaba {pt_data[1]}, RingMaster Salonu Özel Ders paketinizden kalan seans sayınız: {pt_data[5]}. Ödeme Durumu: {pt_data[7]}. Bir sonraki antrenman saatinizi planlamak veya paketinizi yenilemek için dönüş yapabilirsimiz! 🥊"
                msg_pt_text = st.text_area("Özel Ders Mesaj Metni", varsayilan_pt_msg, height=100)
                
                enc_pt_msg = urllib.parse.quote(msg_pt_text)
                wa_pt_url = f"https://wa.me/{pt_data[2]}?text={enc_pt_msg}"
                sms_pt_url = f"sms:{pt_data[2]}?body={enc_pt_msg}"
                
                col_pt_btn1, col_pt_btn2 = st.columns(2)
                with col_pt_btn1:
                    st.markdown(f'<a href="{wa_pt_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp PT Kalan Ders Uyarısı At</button></a>', unsafe_allow_html=True)
                with col_pt_btn2:
                    st.markdown(f'<a href="{sms_pt_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS PT Kalan Ders Uyarısı At</button></a>', unsafe_allow_html=True)
            else:
                st.info("Kayıtlı özel ders paketi bulunmuyor.")

    
 

            
    

