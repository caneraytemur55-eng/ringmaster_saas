import streamlit as st
import datetime
import urllib.parse
from database import (
    init_db, uye_ekle, uyeleri_getir, randevu_ekle, 
    randevulari_getir, randevu_sayisi, aidat_durum_guncelle, kusak_guncelle,
    deneme_ekle, denemeleri_getir,
    ozel_ders_ekle, ozel_dersleri_getir, ozel_ders_seans_dus, ozel_ders_ucret_guncelle,
    kurulum_tarihi_getir, kasa_islem_ekle, kasa_ozet_getir, kasa_islemleri_getir,
    olcum_ekle, olcumleri_getir
)

# Veritabanı Kurulumu
init_db()

st.set_page_config(page_title="RingMaster SaaS v4.0", page_icon="🥊", layout="wide")

st.title("🥊 RingMaster SaaS - Salon Yönetim Sistemi")

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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🥊 Deneme Dersi (Lead)",
    "🎯 Özel Ders (PT) & Ücret",
    "👤 Üye Yönetimi & Kuşak", 
    "📅 Randevu & Ders", 
    "📈 Sporcu Ölçüm Takibi",
    "📊 Kasa & Finans Paneli", 
    "📱 WhatsApp & SMS Otomasyonu",
    "🤖 AI RingMaster Chat Koç"
])

KUSAKLAR = [
    "Beyaz Kuşak / Başlangıç",
    "Sarı Kuşak / Orta Seviye",
    "Yeşil Kuşak",
    "Mavi Kuşak",
    "Kahverengi Kuşak",
    "Siyah Kuşak / Müsabık / İleri Seviye"
]

# Deneme süresi bittiyse ve PRO değilse erişim uyarısı
if not IS_PRO and kalan_deneme_gunu <= 0:
    st.error("⛔ **Deneme Süreniz Dolmuştur!** 15 günlük ücretsiz deneme periyodunuz sona ermiştir. Lütfen yönetici ile iletişime geçip PRO pakete geçiniz.")
else:
    # --- TAB 1: DENEME DERSİ ---
    with tab1:
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

    # --- TAB 2: ÖZEL DERS (PT) & ÜCRET TAKİBİ ---
    with tab2:
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

    # --- TAB 3: ÜYE YÖNETİMİ ---
    with tab3:
        st.subheader("Yeni Sporcu Kaydı")
        with st.form("uye_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            ad_soyad = col1.text_input("Adı Soyadı")
            telefon = col1.text_input("Telefon (örn: 905xxxxxxxxx)")
            brans = col1.selectbox("Branş", ["Boks", "Kickboks", "Muay Thai", "Karate", "Fitness"])
            kusak = col2.selectbox("Mevcut Kuşak", KUSAKLAR)
            aidat_tarihi = col2.date_input("Son Aidat Tarihi", datetime.date.today())
            aidat_durumu = col2.selectbox("Aidat Durumu", ["Ödendi", "Ödeme Bekliyor"])
            aidat_tutari = col2.number_input("Aylık Aidat Tutarı (TL)", min_value=0, value=1500)
            
            submit = st.form_submit_button("➕ Sporcuyu Kaydet")
            if submit and ad_soyad and telefon:
                uye_ekle(ad_soyad, telefon, brans, kusak, str(aidat_tarihi), aidat_durumu, str(datetime.date.today()))
                if aidat_durumu == "Ödendi":
                    kasa_islem_ekle("Gelir", "Aidat", aidat_tutari, f"{ad_soyad} Üyelik Aidatı")
                st.success(f"{ad_soyad} başarıyla eklendi!")

        st.markdown("---")
        st.subheader("📋 Kayıtlı Sporcular")
        uyeler = uyeleri_getir()
        if uyeler:
            for u in uyeler:
                st.write(f"🥊 **{u[1]}** | Branş: {u[3]} | 🥋 Kuşak: **{u[4]}** | Aidat: `{u[6]}`")
        else:
            st.info("Kayıtlı sporcu yok.")

    # --- TAB 4: RANDEVULAR ---
    with tab4:
        st.subheader("Randevu Takvimi")
        randevular = randevulari_getir()
        if randevular:
            for r in randevular:
                st.write(f"🗓️ **{r[3]} {r[4]}** - 🥊 **{r[1]}** ({r[2]})")
        else:
            st.info("Randevu bulunmuyor.")

    # --- TAB 5: SPORCU ÖLÇÜM TAKİBİ (YENİ MODÜL!) ---
    with tab5:
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

    # --- TAB 6: KASA & FİNANS PANENİ ---
    with tab6:
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

    # --- TAB 7: WHATSAPP / SMS ---
    with tab7:
        st.subheader("📱 İletişim Otomasyonu")
        pt_dersler = ozel_dersleri_getir()
        if pt_dersler:
            secilen_pt_str = st.selectbox("Özel Ders Sporcusu Seç", [f"{p[1]} ({p[3]} - Kalan Seans: {p[5]})" for p in pt_dersler])
            pt_data = [p for p in pt_dersler if f"{p[1]} ({p[3]} - Kalan Seans: {p[5]})" == secilen_pt_str][0]
            
            varsayilan_pt_msg = f"Merhaba {pt_data[1]}, RingMaster Salonu Özel Ders paketinizden kalan seans sayınız: {pt_data[5]}. Ödeme Durumu: {pt_data[7]}. Bir sonraki antrenman saatinizi planlamak için dönüş yapabilirsiniz! 🥊"
            msg_pt_text = st.text_area("Özel Ders Mesaj Metni", varsayilan_pt_msg)
            
            enc_pt_msg = urllib.parse.quote(msg_pt_text)
            wa_pt_url = f"https://wa.me/{pt_data[2]}?text={enc_pt_msg}"
            sms_pt_url = f"sms:{pt_data[2]}?body={enc_pt_msg}"
            
            col_pt_btn1, col_pt_btn2 = st.columns(2)
            with col_pt_btn1:
                st.markdown(f'<a href="{wa_pt_url}" target="_blank"><button style="background-color:#25D366;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">📲 WhatsApp PT Bildirimi At</button></a>', unsafe_allow_html=True)
            with col_pt_btn2:
                st.markdown(f'<a href="{sms_pt_url}"><button style="background-color:#007AFF;color:white;width:100%;padding:12px;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">💬 SMS PT Bildirimi At</button></a>', unsafe_allow_html=True)

    # --- TAB 8: AI RİNGMASTER CHAT KOÇ ---
    with tab8:
        st.subheader("🤖 AI RingMaster Canlı Chat Asistanı")
        st.write("7/24 Salon Yönetim, Antrenman ve İkna Koçunuz.")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Selam Şampiyon! 🥊 Ben RingMaster AI Koçun. Özel ders paketleri, ikna mesajları ve antrenman programları için emrindeyim!"}
            ]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("RingMaster AI Koç'a sorun..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            p_lower = prompt.lower()
            if "özel ders" in p_lower or "pt" in p_lower:
                response = """
### 🥊 Özel Ders (PT) Satış & İkna Stratejisi
"Özel ders satarken sporcuya seans değil **DEĞİŞİM** satın. 10 Seanslık pakette 5. derste sporcunun gelişim videosunu çekip kendisine atın ve ekleyin: 'Tekniğin 2 katına çıktı, bir 10 seanslık paketle müsabık seviyeye geçeriz!'"
                """
            elif "antrenman" in p_lower or "program" in p_lower:
                response = """
### 🥊 Özelleştirilmiş Antrenman Programı
**1. Isınma (15 Dk):** 3 Raund İp Atlama & Omuz Mobilite  
**2. Teknik (20 Dk):** 3 Raund Gölge Boksu (Direk-Kanca) + 3 Raund Torba  
**3. Kondisyon (20 Dk):** 4 Raund Lapa & 50 Şınav / Plank  
**4. Soğuma (5 Dk):** Statik esnetme.
                """
            else:
                response = f"Anlaşıldı Şampiyon! **'{prompt}'** konusuyla ilgili özel ders ve salon yönetiminde sana destek olmaya hazırım! 🥊"

            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
