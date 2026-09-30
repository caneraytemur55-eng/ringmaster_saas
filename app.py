import streamlit as st
import datetime
import pandas as pd

# Sayfa Yapılandırması (Geniş Ekran ve Temalı)
st.set_page_config(
    page_title="Ringmaster SaaS - Salon Yönetimi & AI Head Coach",
    page_icon="🥋",
    layout="wide"
)

def render_ultimate_ringmaster():
    # ---------------------------------------------------------
    # 1. HEADER & OVERVIEW METRICS
    # ---------------------------------------------------------
    st.title("🥋 Ringmaster SaaS Pro - Dijital Salon Yönetimi & AI Head Coach")
    st.caption("BJJ, Muay Thai, Boks ve MMA Akademileri İçin Bütünleşik Akıllı Yönetim Platformu")
    st.markdown("---")

    # Üst Bilgi Kartları (Executive Metrics)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Toplam Aktif Üye", value="142 Sporcu", delta="+8 Bu Ay")
    with col2:
        st.metric(label="Kuşak / Stripe Adayı", value="6 Sporcu", delta="Terfi Hazır")
    with col3:
        st.metric(label="Riskli Üye (Churn)", value="3 Kişi", delta="-12% Katılım", delta_color="inverse")
    with col4:
        st.metric(label="Aylık MRR (Tahmini)", value="£ 6,450", delta="+12% Sterlin")
    with col5:
        st.metric(label="Tamamlanan AI Dersleri", value="34 Ders", delta="Bu Hafta")

    st.markdown("---")

    # ---------------------------------------------------------
    # 2. SECTOR-LEADING MULTI-MODULE TABS
    # ---------------------------------------------------------
    tab_coach, tab_belts, tab_churn, tab_finance, tab_waiver, tab_schedule, tab_ai_chat = st.tabs([
        "🏋️‍♂️ AI Antrenman & Müsabaka Koçu", 
        "🥋 Kuşak, Çizgi & Terfi", 
        "📊 Terk (Churn) & Sakatlık Riski", 
        "💳 Finans, Stripe & POS Kantin", 
        "📜 Feragatname & GDPR (Waiver)",
        "📅 Ders Programı & Kontenjan",
        "💬 Bilge AI Başasistan Chat"
    ])

    # =========================================================
    # TAB 1: AI ANTRENMAN VE MÜSABAKA KOÇU
    # =========================================================
    with tab_coach:
        st.subheader("📋 Bütünleşik AI Antrenman & Taktik Jeneratörü")
        st.write("Dövüş sanatları pedagojisine uygun dinamik ısınma, driller, koşullu sparring ve soğuma programı.")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            discipline = st.selectbox("Branş Seçin", ["BJJ (Gi)", "BJJ (No-Gi)", "Muay Thai / Kickboks", "Boks", "MMA (Kafes Sporları)", "Krav Maga / Self-Defense"])
            duration = st.select_slider("Ders Süresi", options=[45, 60, 75, 90, 120], value=60)
        with col_b:
            level = st.selectbox("Grup Seviyesi", ["Beginner (Fundametals)", "Intermediate (Teknik)", "Advanced / Müsabık Grubu", "Kids (Çocuk Grubu 6-12 Yaş)"])
            intensity = st.select_slider("Antrenman Yoğunluğu", options=["Düşük (Teknik Beceriler)", "Orta (Standart)", "Yüksek (Müsabaka Kampı)"])
        with col_c:
            focus_area = st.text_input("Günün Odak Konusu / Senaryo", value="Closed Guard'dan Armbar ve Sweep Kombinasyonu")
            sparring_type = st.selectbox("Sparring Tipi", ["Koşullu Positional Sparring", "Serbest Sparring (Open Mat)", "Grappling / Takedown Drills", "Sparring Yok (Sadece Teknik)"])

        if st.button("🚀 Bilge AI Antrenman Planını Üret", type="primary"):
            with st.spinner("AI Head Coach salon verilerine ve anatomi kurallarına uygun antrenmanı planlıyor..."):
                st.success(f"✅ {discipline} - {focus_area} ({duration} Dakika) İçin Hazırlanan Profesyonel Antrenman Reçetesi")
                
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.markdown(f"""
                    ### ⏱️ Antrenman Akışı ({duration} dk)
                    * **Dinamik Isınma & Mobilite (10 dk):** Kalça mobilitesi, omurga rotasyonları, branşa özel kartilaj hazırlığı.
                    * **Teknik Gösterim & Driller (25 dk):** 
                      1. Adım: {focus_area} temel pozisyon alma ve tutuş (grip) kontrolü.
                      2. Adım: Rakip tepkisine göre B planı geçişi.
                      3. Adım: 3'er dakikalık kesintisiz partnerli drill tekrarı.
                    * **Koşullu Sparring ({int(duration*0.3)} dk):** 
                      * Format: {sparring_type}. Sadece belirlenen pozisyondan başlayan 3'er dakikalık rauntlar.
                    * **Kondisyon & Cool-down (10 dk):** Çekirdek bölge (Core) dayanıklılığı ve nefes regülasyonu.
                    """)
                with col_res2:
                    st.info("""
                    💡 **AI Head Coach Taktik İpucu:**
                    - **Sakatlık Önleme:** Başlangıç seviyesi sporcularda hip-hyper extension riskine karşı dirsek kilitlerinde erken tap (teslimiyet) kuralını hatırlatın.
                    - **Pedagojik Yaklaşım:** Tekniği göstermeden önce 'Neden bu pozisyon?' sorusunu gruba yönelterek mantığını kavramalarını sağlayın.
                    """)

    # =========================================================
    # TAB 2: KUŞAK, ÇİZGİ VE TERFİ TAKİBİ
    # =========================================================
    with tab_belts:
        st.subheader("🎖️ Otomatik Kuşak Sınavı & Çizgi (Stripe) Hakediş Sistemi")
        st.write("Sistem derse katılım sayısı, salonda geçirilen ay ve performans puanına göre terfi adaylarını otomatik sıralar.")
        
        belt_data = pd.DataFrame([
            {"Sporcu": "Ahmet Yılmaz", "Branş": "BJJ", "Mevcut Seviye": "Beyaz Kuşak (2 Çizgi)", "Toplam Ders": 38, "Salondaki Süre": "5 Ay", "Durum": "3. Çizgi Hazır 🟩"},
            {"Sporcu": "Selin Kaya", "Branş": "BJJ", "Mevcut Seviye": "Mavi Kuşak (4 Çizgi)", "Toplam Ders": 142, "Salondaki Süre": "18 Ay", "Durum": "Mor Kuşak Sınav Adayı 🟣"},
            {"Sporcu": "Can Demir", "Branş": "Muay Thai", "Mevcut Seviye": "Seviye 1 Prajiad", "Toplam Ders": 28, "Salondaki Süre": "4 Ay", "Durum": "Seviye 2 Sınav Adayı 🟨"},
            {"Sporcu": "Erman Öztürk", "Branş": "Boks", "Mevcut Seviye": "Orta Seviye", "Toplam Ders": 50, "Salondaki Süre": "6 Ay", "Durum": "İleri Grup Geçişi 🥊"},
        ])
        
        st.dataframe(belt_data, use_container_width=True)
        
        if st.button("📩 Terfisi Gelen Sporculara Otomatik Davet Gönder"):
            st.success("Tüm terfi adaylarına SMS/E-posta yoluyla sınav ve çizgi töreni bilgilendirmesi iletildi!")

    # =========================================================
    # TAB 3: SPORCU TERK (CHURN) & SAKATLIK RİSKİ
    # =========================================================
    with tab_churn:
        st.subheader("⚠️ AI Erken Uyarı: Bırakma (Churn) ve Sakatlık Riski")
        
        col_ch1, col_ch2 = st.columns(2)
        with col_ch1:
            st.error("🚨 **Devamsızlık Yapıp Bırakma Riski Taşıyanlar (Churn Risk)**")
            st.warning("• **Mertcan Yılmaz:** Son 14 gündür derse katılmadı. (Eski Katılım: 3 gün/hafta)")
            st.warning("• **Ayşe Demir:** Üyelik bitimine 5 gün kaldı, yenileme yapmadı.")
            if st.button("💬 Mertcan Yılmaz İçin Geri Kazanım Mesajı Oluştur"):
                st.code("Selam Mertcan! Minderlerde gözümüz seni arıyor. Bu haftaki teknik derslerimize özel senin için yer ayırdık, bu akşam bekliyoruz! 🥋", language="text")

        with col_ch2:
            st.warning("🩹 **Over-Training / Sakatlık Riski Taşıyanlar**")
            st.info("• **Burak Çevik:** Haftalık 7 günde 11 derse katıldı. Dinlenme günü (Rest Day) eksik.")
            st.info("• **Zeynep Tan:** Son 3 ders antrenman sonrası omuz ağrısı bildirdi.")
            if st.button("📋 Burak Çevik İçin Dinlenme/Rehab Programı Öner"):
                st.success("AI Önerisi: Burak'a bu hafta 2 gün hafif aktif esneme (Mobility) ve havuz antrenmanı tavsiye edildi.")

    # =========================================================
    # TAB 4: FİNANS, STRIPE & POS KANTİN
    # =========================================================
    with tab_finance:
        st.subheader("💳 Finansal Arayüz, Otomatik Tahsilat & Pro-Shop POS")
        
        f_col1, f_col2 = st.columns([2, 1])
        with f_col1:
            st.markdown("##### 💵 Geciken ve Başarısız Ödemeler (Stripe Auto-Debit)")
            unpaid_data = pd.DataFrame([
                {"Üye Adı": "David Smith", "Üyelik Tipi": "Aylık Sınırsız BJJ", "Tutar": "£ 75.00", "Durum": "Kart Bakiye Yetersiz", "Son Deneme": "Bugün"},
                {"Üye Adı": "Elena Rostova", "Üyelik Tipi": "10'lu Punch Pass", "Tutar": "£ 110.00", "Durum": "Ödeme Bekliyor", "Son Deneme": "Dün"},
            ])
            st.table(unpaid_data)
            if st.button("🔄 Başarısız Ödemeleri Stripe Üzerinden Yeniden Çek"):
                st.info("Stripe entegrasyonu üzerinden otomatik tahsilat tetiklendi.")

        with f_col2:
            st.markdown("##### 🛒 Pro-Shop / Kantin Hızlı Satış")
            item = st.selectbox("Ürün Seç", ["BJJ Gi (Kimono) - A2", "Rashguard (Ringmaster Edition)", "Boks Eldiveni 16oz", "Protein Shake / Su", "Muay Thai Şortu"])
            member = st.text_input("Müşteri / Üye Adı", placeholder="Örn: Ahmet Yılmaz")
            price = st.number_input("Tutar (£/₺)", value=45.0)
            if st.button("🛍️ Satışı Tamamla ve Hesaba İşle"):
                st.success(f"{item} satışı {member} hesabına Stripe/Nakit olarak işlendi!")

    # =========================================================
    # TAB 5: FERAGATNAME & GDPR (WAIVER)
    # =========================================================
    with tab_waiver:
        st.subheader("📜 Dijital Sorumluluk Feragatnamesi (Waiver) & PAR-Q Formları")
        st.write("İngiltere ve AB yasal standartlarına uygun sakatlanma sorumluluk beyanları ve sağlık formları.")
        
        with st.expander("📝 Yeni Üye Dijital Waiver Formu Önizleme"):
            st.markdown("""
            **LIABILITY WAIVER & RELEASE OF LIABILITY AGREEMENT**
            1. I acknowledge that martial arts training (BJJ, Muay Thai, Boxing, MMA) involves high-intensity physical contact and risk of injury.
            2. I certify that I am physically fit and have no medical conditions that prevent safe participation (PAR-Q passed).
            3. I grant permission for the academy to use photo/video footage for training and promotional purposes under GDPR compliance.
            """)
            st.checkbox("Yukarıdaki koşulları okudum, kabul ediyorum.")
            st.text_input("Dijital İmza (Ad Soyad)", placeholder="İmza yerine geçer")
            st.button("✅ Waiver Formunu Onayla ve Arşivle")

    # =========================================================
    # TAB 6: DERS PROGRAMI & KONTENJAN
    # =========================================================
    with tab_schedule:
        st.subheader("📅 İnteraktif Ders Takvimi & Minder Kontenjanı")
        
        schedule_data = pd.DataFrame([
            {"Saat": "07:00 - 08:00", "Ders": "Morning BJJ All Levels", "Eğitmen": "Koç Caner", "Kapasite": "18 / 20", "Yedek Liste": 0},
            {"Saat": "12:00 - 13:00", "Ders": "Lunchtime Muay Thai", "Eğitmen": "Koç Alex", "Kapasite": "20 / 20 (Dolu)", "Yedek Liste": 3},
            {"Saat": "18:00 - 19:30", "Ders": "Advanced No-Gi & Sparring", "Eğitmen": "Koç Caner", "Kapasite": "14 / 25", "Yedek Liste": 0},
            {"Saat": "19:30 - 20:30", "Ders": "Beginners Boxing", "Eğitmen": "Koç Sarah", "Kapasite": "10 / 15", "Yedek Liste": 0},
        ])
        st.table(schedule_data)

    # =========================================================
    # TAB 7: BİLGE AI BAŞASİSTAN CHAT
    # =========================================================
    with tab_ai_chat:
        st.subheader("💬 Ringmaster AI - Bilge Head Coach & Başasistan")
        st.caption("Salon finansı, dövüş teknikleri, üye ilişkileri veya KOSGEB/UK pazar stratejileri hakkında sorularınızı yanıtlar.")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Selam Koç! Ben Ringmaster Bilge AI. Minderdeki teknik sorunlardan salondaki Sterlin/TL finans akışına kadar her alanda yanındayım. Bugün neyi çözüyoruz?"}
            ]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Örn: BJJ başlangıç sınıfı için 4 haftalık müfredat hazırla veya Churn oranını nasıl düşürürüm?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # Dinamik AI Yanıt Mantığı (Simüle Edilmiş Gelişmiş Yanıt)
            response = f"**[Ringmaster Bilge AI]:** '{prompt}' sorunuz analiz edildi. Spor pedagojisi ve salon işletim ilkelerine göre tavsiyelerim veritabanınıza işlendi."
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

# ---------------------------------------------------------
# UYGULAMAYI ÇALIŞTIRMA (MAIN CALL)
# ---------------------------------------------------------
if __name__ == "__main__":
    render_ultimate_ringmaster()
else:
    # Streamlit Cloud doğrudan import ettiğinde de çalışması için:
    render_ultimate_ringmaster()
