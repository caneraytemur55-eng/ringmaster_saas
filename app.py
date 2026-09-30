import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ---------------------------------------------------------
# 1. SAYFA YAPILANDIRMASI & ÖZEL CSS STİL DOKUNUŞLARI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ringmaster SaaS - Ar-Ge Kokpiti & AI Head Coach",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS (Metrik Kartları, Gölgeler ve Rozetler İçin)
st.markdown("""
    <style>
    /* Metrik Kartı Özelleştirme */
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Ar-Ge Rozet Stili */
    .badge-rd {
        background-color: #0284c7;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        display: inline-block;
    }
    .badge-ai {
        background-color: #16a34a;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        display: inline-block;
    }
    .badge-uk {
        background-color: #9333ea;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

def render_ultimate_ringmaster_rd():
    # ---------------------------------------------------------
    # 2. ÜST BİLGİ VE AR-GE ROZETLERİ
    # ---------------------------------------------------------
    st.markdown("""
        <div>
            <span class="badge-rd">🔬 KOSGEB Ar-Ge Faz-1 Prototip</span>
            <span class="badge-ai">⚡ AI Head Coach Engine v1.2 Active</span>
            <span class="badge-uk">🇬🇧 UK Market Ready</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("🥋 Ringmaster SaaS Pro - Salon Yönetimi & AI Kokpiti")
    st.caption("Dövüş Sanatları Akademileri İçin Bütünleşik Akıllı Yönetim & Karar Destek Platformu")
    st.markdown("---")

    # Executive Metrikler
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Toplam Aktif Üye", value="142 Sporcu", delta="+8 Bu Ay")
    with col2:
        st.metric(label="Kuşak/Stripe Adayı", value="6 Sporcu", delta="Terfi Hazır")
    with col3:
        st.metric(label="Riskli Üye (Churn)", value="3 Kişi", delta="-12% Katılım", delta_color="inverse")
    with col4:
        st.metric(label="Aylık MRR (Tahmini)", value="£ 6,450", delta="+12% Sterlin")
    with col5:
        st.metric(label="Tamamlanan AI Dersleri", value="34 Ders", delta="Bu Hafta")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. SEKTÖR LİDERİ MODÜLLER VE GRAFİK ANALİTİKLERİ
    # ---------------------------------------------------------
    tab_overview, tab_coach, tab_belts, tab_churn, tab_finance, tab_waiver, tab_ai_chat = st.tabs([
        "📈 Analitik & Genel Bakış",
        "🏋️‍♂️ AI Antrenman Jeneratörü", 
        "🥋 Kuşak, Çizgi & Terfi", 
        "📊 Terk (Churn) & Sakatlık Riski", 
        "💳 Finans & POS Kantin", 
        "📜 Feragatname & GDPR",
        "💬 Bilge AI Başasistan Chat"
    ])

    # =========================================================
    # TAB 0: ANALİTİK & GENEL BAKIŞ (GÖRSEL GRAFİKLER)
    # =========================================================
    with tab_overview:
        st.subheader("📊 Salon Performansı & Yapay Zeka Trend Analizleri")
        
        g_col1, g_col2 = st.columns(2)
        
        with g_col1:
            st.markdown("##### 🥋 Son 30 Günlük Derse Katılım & Yoğunluk Trendi")
            # Örnek Katılım Verisi (Line Chart)
            dates = pd.date_range(start="2026-09-01", periods=30)
            katilim_data = pd.DataFrame({
                "Tarih": dates,
                "BJJ Sınıfları": np.random.randint(15, 30, size=30),
                "Muay Thai / Boks": np.random.randint(10, 25, size=30)
            }).set_index("Tarih")
            st.line_chart(katilim_data)

        with g_col2:
            st.markdown("##### 💷 Aylık Düzenli Gelir (MRR) Büyümesi (£ Sterlin)")
            # Örnek Finansal Büyüme Verisi (Bar Chart)
            mrr_data = pd.DataFrame({
                "Ay": ["Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül"],
                "Abonelik Geliri": [3200, 4100, 4800, 5600, 6450]
            }).set_index("Ay")
            st.bar_chart(mrr_data)

    # =========================================================
    # TAB 1: AI ANTRENMAN JENERATÖRÜ
    # =========================================================
    with tab_coach:
        st.subheader("📋 Bütünleşik AI Antrenman & Taktik Jeneratörü")
        st.write("Dövüş sanatları pedagojisine uygun dinamik ısınma, driller ve koşullu sparring programı.")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            discipline = st.selectbox("Branş Seçin", ["BJJ (Gi)", "BJJ (No-Gi)", "Muay Thai / Kickboks", "Boks", "MMA"])
            duration = st.select_slider("Ders Süresi", options=[45, 60, 75, 90, 120], value=60)
        with col_b:
            level = st.selectbox("Grup Seviyesi", ["Beginner (Fundamentals)", "Intermediate (Teknik)", "Advanced / Müsabık", "Kids (6-12 Yaş)"])
            intensity = st.select_slider("Antrenman Yoğunluğu", options=["Düşük", "Orta", "Yüksek (Müsabaka Kampı)"])
        with col_c:
            focus_area = st.text_input("Günün Odak Konusu", value="Closed Guard'dan Armbar ve Sweep")
            sparring_type = st.selectbox("Sparring Tipi", ["Koşullu Positional Sparring", "Serbest Sparring", "Drills Only"])

        if st.button("🚀 Bilge AI Antrenman Planını Üret", type="primary"):
            with st.spinner("AI Head Coach ders planını hazırlıyor..."):
                st.success(f"✅ {discipline} - {focus_area} ({duration} dk) Planı Hazırlandı")
                
                res1, res2 = st.columns(2)
                with res1:
                    st.markdown(f"""
                    ### ⏱️ Antrenman Akışı
                    * **Dinamik Isınma (10 dk):** Kalça mobilitesi, omurga rotasyonu.
                    * **Teknik Driller (25 dk):** {focus_area} kombine geçişleri.
                    * **Koşullu Sparring ({int(duration*0.3)} dk):** Format: {sparring_type}.
                    * **Cool-down (10 dk):** Core güçlendirme ve esneme.
                    """)
                with res2:
                    st.info("""
                    💡 **AI Taktik İpucu:**
                    - Başlangıç seviyesinde dirsek kilitlerinde erken tap (teslimiyet) kuralını vurgulayın.
                    - Sakatlık riskini azaltmak için ısınma süresine sadık kalın.
                    """)

    # =========================================================
    # TAB 2: KUŞAK VE ÇİZGİ TAKİBİ
    # =========================================================
    with tab_belts:
        st.subheader("🎖️ Otomatik Kuşak Sınavı & Çizgi (Stripe) Analizi")
        
        belt_data = pd.DataFrame([
            {"Sporcu": "Ahmet Yılmaz", "Branş": "BJJ", "Mevcut Seviye": "Beyaz Kuşak (2 Çizgi)", "Toplam Ders": 38, "Durum": "3. Çizgi Hazır 🟩"},
            {"Sporcu": "Selin Kaya", "Branş": "BJJ", "Mevcut Seviye": "Mavi Kuşak (4 Çizgi)", "Toplam Ders": 142, "Durum": "Mor Kuşak Sınav Adayı 🟣"},
            {"Sporcu": "Can Demir", "Branş": "Muay Thai", "Mevcut Seviye": "Seviye 1 Prajiad", "Toplam Ders": 28, "Durum": "Seviye 2 Sınav Adayı 🟨"},
        ])
        st.dataframe(belt_data, use_container_width=True)

    # =========================================================
    # TAB 3: SPORCU TERK (CHURN) & SAKATLIK RİSKİ
    # =========================================================
    with tab_churn:
        st.subheader("⚠️ AI Erken Uyarı: Churn & Sakatlık Analitiği")
        
        ch1, ch2 = st.columns(2)
        with ch1:
            st.error("🚨 **Devamsızlık Yapıp Bırakma Riski (Churn)**")
            st.warning("• **Mertcan Yılmaz:** Son 14 gündür derse katılmadı.")
            if st.button("💬 Geri Kazanım Mesajı Hazırla"):
                st.code("Selam Mertcan! Minderlerde gözümüz seni arıyor. Bu haftaki teknik derslerimize seni de bekliyoruz! 🥋")
        with ch2:
            st.warning("🩹 **Over-Training / Sakatlık Riski**")
            st.info("• **Burak Çevik:** Haftada 11 derse katıldı. Dinlenme günü eksik.")

    # =========================================================
    # TAB 4: FİNANS & POS KANTİN
    # =========================================================
    with tab_finance:
        st.subheader("💳 Otomatik Tahsilat & Pro-Shop POS")
        
        f1, f2 = st.columns([2, 1])
        with f1:
            st.markdown("##### 💵 Geciken Ödemeler (Stripe Auto-Debit)")
            unpaid_data = pd.DataFrame([
                {"Üye": "David Smith", "Abonelik": "Aylık Sınırsız BJJ", "Tutar": "£ 75.00", "Durum": "Bakiye Yetersiz"},
                {"Üye": "Elena Rostova", "Abonelik": "10'lu Pass", "Tutar": "£ 110.00", "Durum": "Ödeme Bekliyor"},
            ])
            st.table(unpaid_data)
        with f2:
            st.markdown("##### 🛒 Pro-Shop Hızlı Satış")
            st.selectbox("Ürün", ["BJJ Gi - A2", "Rashguard", "Boks Eldiveni", "Protein Shake"])
            st.button("🛍️ Satışı Onayla")

    # =========================================================
    # TAB 5: FERAGATNAME & GDPR
    # =========================================================
    with tab_waiver:
        st.subheader("📜 Dijital Feragatname (Waiver) & GDPR")
        st.checkbox("Spor salonu yasal güvenlik beyanını kabul ediyorum.")
        st.text_input("Dijital İmza (Ad Soyad)")
        st.button("✅ Onayla")

    # =========================================================
    # TAB 6: BİLGE AI BAŞASİSTAN CHAT
    # =========================================================
    with tab_ai_chat:
        st.subheader("💬 Ringmaster AI - Bilge Head Coach Chat")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Selam Koç! Ben Ringmaster Bilge AI. Salon operasyonu veya antrenman planları hakkında neyi çözüyoruz?"}
            ]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Mesajınızı yazın..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            response = f"**[Ringmaster Bilge AI]:** '{prompt}' talebiniz analiz edildi ve yanıtlandı."
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

# ---------------------------------------------------------
# ÇALIŞTIRMA
# ---------------------------------------------------------
if __name__ == "__main__":
    render_ultimate_ringmaster_rd()
else:
    render_ultimate_ringmaster_rd()
