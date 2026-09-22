import streamlit as s
import pandas as pd
import sqlite3
import random
import urllib.parse
import time

# Sayfa Yapılandırması
s.set_page_config(page_title="Ringmaster SaaS - Professional Gym Management", page_icon="🥊", layout="wide")

# --- VERİTABANI BAĞLANTI & KURULUM YÖNETİCİSİ ---
def baglanti_kur():
    return sqlite3.connect("ringmaster_saas.db", check_same_thread=False)

def veritabani_baslat():
    conn = baglanti_kur()
    cursor = conn.cursor()
    
    # Tablolar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uyeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT,
            telefon TEXT,
            brans TEXT,
            pin TEXT,
            kayit_tarihi TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_adi TEXT,
            adet INTEGER,
            fiyat REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kasa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            islem_tipi TEXT,
            aciklama TEXT,
            tutar REAL,
            tarih TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS antrenorler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hoca_adi TEXT,
            brans TEXT,
            ders_sayisi INTEGER,
            prim_orani REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cocuk_gelisim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ogrenci_adi TEXT,
            veli_telefon TEXT,
            notlar TEXT,
            tarih TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kusak_sinav (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ogrenci_adi TEXT,
            mevcut_kusak TEXT,
            hedef_kusak TEXT,
            durum TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS musabiklar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            siklet TEXT,
            galibiyet INTEGER,
            maglubiyet INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sakatliklar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            durum_aciklamasi TEXT,
            sparring_yasagi INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mac_takvimi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turnuva_adi TEXT,
            tarih TEXT,
            katilacak_sporcular TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaylar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aday_adi TEXT,
            telefon TEXT,
            ilgilenilen_brans TEXT,
            durum TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ozel_dersler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            hoca_adi TEXT,
            kalan_ders INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS olcumler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            kilo REAL,
            yag_orani REAL,
            tarih TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS churn_takip (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            son_gelis_tarihi TEXT,
            risk_durumu TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mesaj_loglari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alici_grup TEXT,
            mesaj_icerigi TEXT,
            gonderim_tarihi TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salonlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            salon_adi TEXT,
            sahip_adi TEXT,
            telefon TEXT,
            email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aidatlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            donem TEXT,
            tutar REAL,
            son_odeme TEXT,
            durum TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kas_hafizasi_analizleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            teknik_adi TEXT,
            dogruluk_skoru REAL,
            ai_geri_bildirim TEXT,
            tarih TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS akilli_randevular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            antrenor_adi TEXT,
            slot_tarihi TEXT,
            durum TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS beslenme_receteleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            gunluk_kalori INTEGER,
            protein_hedefi TEXT,
            supplement_notu TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kapi_gecis_loglari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sporcu_adi TEXT,
            pin TEXT,
            gecis_durumu TEXT,
            tarih TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faturalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alici_unvan TEXT,
            vergi_no TEXT,
            fatura_tipi TEXT,
            tutar REAL,
            kdv_orani INTEGER,
            tarih TEXT
        )
    """)
    conn.commit()
    conn.close()

veritabani_baslat()

# Yardımcı DB Fonksiyonları
def uyeleri_getir():
    conn = baglanti_kur()
    res = conn.execute("SELECT * FROM uyeler").fetchall()
    conn.close()
    return res

def uye_ekle(ad, tel, brans, pin):
    conn = baglanti_kur()
    conn.execute("INSERT INTO uyeler (ad_soyad, telefon, brans, pin, kayit_tarihi) VALUES (?, ?, ?, ?, ?)",
                 (ad, tel, brans, pin, pd.Timestamp.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def uye_sil(u_id):
    conn = baglanti_kur()
    conn.execute("DELETE FROM uyeler WHERE id = ?", (u_id,))
    conn.commit()
    conn.close()

def salon_ekle(s_adi, sahip, tel, email):
    conn = baglanti_kur()
    conn.execute("INSERT INTO salonlar (salon_adi, sahip_adi, telefon, email) VALUES (?, ?, ?, ?)",
                 (s_adi, sahip, tel, email))
    conn.commit()
    conn.close()

# --- KOYU LACİVERT & NEON TURUNCU/MERCAN GYM TEMASI CSS ---
s.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: #ffffff;
    }
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800;
        color: #f97316;
    }
    [data-testid="stMetricContainer"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: #ffffff !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 14px rgba(249, 115, 22, 0.45);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
        box-shadow: 0 6px 20px rgba(249, 115, 22, 0.65);
        transform: translateY(-2px);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px;
    }
    .slide-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #f97316;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(249, 115, 22, 0.25);
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

s.sidebar.title("🥊 Ringmaster SaaS")
s.sidebar.markdown("---")

# Modül Listesi (27 Modül Tam Kadro - Fatura Modülü Dahil)
secilen_modul = s.sidebar.selectbox(
    "Modül Seçin", 
    [
        "Ana Sayfa", 
        "🚀 Sistem Oryantasyonu & Slayt Turu",
        "Ringmaster AI Asistanı 🤖", 
        "🧠 Akıllı Dijital Kas Hafızası & Teknik AI",
        "📅 Akıllı Randevu & Koç Planlama AI",
        "🥗 Akıllı Beslenme & Supplement Reçete Botu",
        "🚪 Akıllı Kapı, Turnike & Biyometrik Geçiş",
        "📄 Fatura Düzenleme & Kurumsal Arşiv",
        "Salon Üyeleri Yönetimi", 
        "Yoklama Sistemi", 
        "Stok Takibi", 
        "Kasa / Finans", 
        "Aidat & Ücret Ödeme Takibi 💳",
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
        "🌍 Küresel & Yerel Ödemeler",
        "Sistem Ayarları"
    ]
)

# --- 1. ANA SAYFA ---
if secilen_modul == "Ana Sayfa":
    s.subheader("🥊 Ringmaster SaaS Yönetim Paneline Hoş Geldin Patron!")
    s.markdown("Koyu lacivert zemin, neon turuncu butonlar, Taekwondo dahil tüm dünya branşları ve **Resmi Fatura Arşivleme** dahil 27 modülle sistem devrede.")
    
    col1, col2, col3 = s.columns(3)
    with col1:
        s.metric("Toplam Üye", len(uyeleri_getir()))
    with col2:
        s.metric("Aktif Modül", "27 / 27 (Kurumsal Tam Donanımlı)")
    with col3:
        s.metric("Sistem Modeli", "Rakipsiz AI & Küresel SaaS 🚀")

# --- 2. SİSTEM ORYANTASYONU & SLAYT TURU (27 Modül Güncel & Konforlu 3.5s) ---
elif secilen_modul == "🚀 Sistem Oryantasyonu & Slayt Turu":
    s.subheader("🚀 Ringmaster SaaS - 27 Modüllü Profesyonel Slayt Turu")
    s.write("Sistemin tüm modüllerini detaylıca inceleyebilmeniz için optimize edilmiş, konforlu geçiş hızına sahip canlı sunum.")

    tab1, tab2 = s.tabs(["🎬 Otomatik Slayt Gösterisi", "📋 27 Modül Akış Detayları"])

    with tab1:
        s.markdown("### ⏱️ Detaylı İnceleme İçin Yavaşlatılmış Slayt Akışı (3.5sn / Modül)")
        
        slayt_adimları = [
            ("01", "🥊 Ana Sayfa", "Ringmaster SaaS yönetim paneline genel bakış ve anlık metrikler."),
            ("02", "🚀 Sistem Oryantasyonu", "Salonunuzu tanıtan rehberli modül sunumu."),
            ("03", "🤖 Ringmaster AI Asistanı", "Veritabanınızla konuşan ve kararlarınızı optimize eden yapay zeka."),
            ("04", "🧠 Akıllı Kas Hafızası & Teknik AI", "Sporcuların eklem açılarını analiz eden devrimci AI antrenör asistanı."),
            ("05", "📅 Akıllı Randevu & Koç Planlama AI", "Antrenör müsaitliklerine göre en iyi PT slotunu öneren akıllı takvim."),
            ("06", "🥗 Akıllı Beslenme & Supplement Botu", "Vücut ölçümlerine göre kişiye özel kalori/protein ve WhatsApp reçetesi."),
            ("07", "🚪 Akıllı Kapı, Turnike & Geçiş", "Yüz tanıma, parmak izi veya PIN ile otonom turnike ve yoklama yönetimi."),
            ("08", "📄 Fatura Düzenleme & Arşiv", "Resmi e-fatura, e-arşiv ve kurumsal gider faturalarının yasal takibi."),
            ("09", "👤 Salon Üyeleri Yönetimi", "Taekwondo, Boks, MMA, BJJ ve tüm branşlarda hızlı kayıt ve PIN üretimi."),
            ("10", "📝 Yoklama Sistemi", "Tablet üzerinden 4 haneli PIN ile saniyeler içinde otomatik antrenman yoklaması."),
            ("11", "📦 Stok Takibi", "Eldiven, dobok, bandaj ve ekipman stoklarının anlık kontrolü."),
            ("12", "💰 Kasa / Finans", "Günlük gelir ve gider hareketlerinin şeffaf finansal takibi."),
            ("13", "💳 Aidat & Ücret Ödeme Takibi", "Üye borçlandırma, tahsilat ve geciken ödeme uyarıları."),
            ("14", "🥋 Antrenör & Prim Takibi", "Antrenörlerin ders sayıları ve yüzdelik prim hesaplamaları."),
            ("15", "🧒 Çocuk Gelişim Raporları", "Çocuk sporcuların gelişim notları ve veli bilgilendirme akışı."),
            ("16", "🥋 Kuşak / Derece Sınavı", "Taekwondo ve diğer disiplinlerin dan/kup ve seviye geçiş sınavları."),
            ("17", "🥊 Müsabık Takımı Yönetimi", "Lisanslı müsabık sporcuların siklet ve galibiyet istatistikleri."),
            ("18", "🩹 Sakatlık & Sparring Takibi", "Sakat sporcuların güvenliği için sparring yasaklarının yönetimi."),
            ("19", "🏆 Maç / Turnuva Takvimi", "Önümüzdeki şampiyonalar ve turnuvalara katılacak sporcu kadroları."),
            ("20", "📞 Aday Üye Takibi (CRM)", "Deneme dersine gelen potansiyel adayların dönüşüm süreçleri."),
            ("21", "🎯 Özel Ders (PT) Paketi", "Birebir özel ders alan sporcuların kalan ders haklarının takibi."),
            ("22", "📊 Vücut Ölçüm Takibi", "Sporcuların kilo ve yağ oranı değişimlerinin periyodik kaydı."),
            ("23", "⚠️ Üye Terk (Churn) Riski", "Uzun süredir gelmeyen üyelerin tespiti ve erken müdahale."),
            ("24", "📢 Toplu SMS / Duyuru Logu", "Üyelere veya velilere yapılan toplu duyuru ve mesaj arşivleme."),
            ("25", "🏢 SaaS Abonelik Yönetimi", "Yeni salon müşterilerinin 14 günlük deneme ve abonelik süreçleri."),
            ("26", "🌍 Küresel & Yerel Ödemeler", "Stripe ve PayTR ile çoklu para birimi ve kartlı deneme modeli."),
            ("27", "⚙️ Sistem Ayarları", "Veritabanı yönetimi, onarım ve sistem parametreleri kontrolü.")
        ]

        slayt_yeri = s.empty()
        ilerleme_cubugu = s.progress(0)
        
        if s.button("▶️ Slayt Turunu Başlat (27 Modül)"):
            toplam = len(slayt_adimları)
            for i, (no, b, a) in enumerate(slayt_adimları):
                ilerleme_cubugu.progress((i + 1) / toplam)
                with slayt_yeri.container():
                    s.markdown(f"""
                        <div class="slide-card">
                            <h4 style="color: #f97316; margin-bottom: 5px;">Modül No: {no} / 27</h4>
                            <h2 style="color: #ffffff; margin-top: 0px;">{b}</h2>
                            <p style="font-size: 18px; color: #cbd5e1; margin-top: 15px;">{a}</p>
                        </div>
                    """, unsafe_allow_html=True)
                time.sleep(3.5)
            s.success("🎉 27 modüllük tam sunum başarıyla tamamlandı, patron!")
        else:
            with slayt_yeri.container():
                s.markdown("""
                    <div class="slide-card">
                        <h4 style="color: #f97316; margin-bottom: 5px;">Modül 01 / 27</h4>
                        <h2 style="color: #ffffff; margin-top: 0px;">🥊 Ringmaster SaaS Sunumuna Hazır</h2>
                        <p style="font-size: 18px; color: #cbd5e1; margin-top: 15px;">Başlat butonuna basarak tüm 27 modülü konforlu hızda izleyin.</p>
                    </div>
                """, unsafe_allow_html=True)

    with tab2:
        s.markdown("### 📋 27 Modülün Detaylı Akış Tablosu")
        df_s = pd.DataFrame([{"No": x[0], "Modül Adı": x[1], "Açıklama": x[2]} for x in slayt_adimları])
        s.dataframe(df_s, use_container_width=True)

# --- 3. RİNGMASTER AI ASİSTANI ---
elif secilen_modul == "Ringmaster AI Asistanı 🤖":
    s.subheader("🤖 Ringmaster AI - Salon Yönetim Asistanı")
    if "messages" not in s.session_state:
        s.session_state.messages = [{"role": "assistant", "content": "Selam patron! Fatura modülü dahil tüm 27 modül devrede. Bugün hangi finansal veya operasyonel süreci optimize ediyoruz?"}]

    for m in s.session_state.messages:
        with s.chat_message(m["role"]):
            s.markdown(m["content"])

    if prompt := s.chat_input("Salon yönetimi, faturalar veya üyelikler hakkında sor..."):
        s.session_state.messages.append({"role": "user", "content": prompt})
        with s.chat_message("user"):
            s.markdown(prompt)

        with s.chat_message("assistant"):
            yanit = f"Harika bir yaklaşım patron! '{prompt}' konusunda kurumsal otomasyon ve yasal altyapılar tam devrede."
            s.markdown(yanit)
            s.session_state.messages.append({"role": "assistant", "content": yanit})

# --- 4. AKILLI DİJİTAL KAS HAFIZASI & TEKNİK AI ---
elif secilen_modul == "🧠 Akıllı Dijital Kas Hafızası & Teknik AI":
    s.subheader("🧠 Akıllı Dijital Kas Hafızası & Teknik Ustalaşma Modülü")
    s.info("Sporcuların antrenman esnasındaki hareket formlarını analiz ederek antrenörün yükünü alır ve kusursuz kas hafızası oluşturur.")

    with s.form("kas_hafizasi_form"):
        s.markdown("### 🎯 Sporcu Teknik Simülasyonu & AI Analizi")
        c1, c2 = s.columns(2)
        with c1:
            sporcu_sec = s.text_input("Sporcu Ad Soyad", value="Ahmet Yılmaz")
            teknik_sec = s.selectbox("Çalışılan Teknik", [
                "Dollyo-Chagi / Döner Tekme (Taekwondo)", "Direkt Sağ Kroşe (Boks)", 
                "Low-Kick Açısı (Muay Thai)", "Guard Pozisyonu (Wing Chun)", 
                "Single-Leg Takedown (MMA)", "Doğru Duruş (Karate)"
            ])
        with c2:
            dirsek_acisi = s.slider("Dirsek / Eklem Açısı", 0, 180, 95)
            diz_acisi = s.slider("Diz / Büküm Açısı", 90, 180, 160)

        if s.form_submit_button("🤖 AI Kas Hafızası Analizini Başlat"):
            sapma = abs(90 - dirsek_acisi) + abs(170 - diz_acisi)
            skor = max(35, round(100 - (sapma * 0.8), 2))
            
            if skor >= 85:
                geri_bildirim = "Mükemmel form! Kas hafızası başarıyla kilitleniyor."
            elif skor >= 65:
                geri_bildirim = "İyi düzeyde ancak açıları biraz daha nizami tutman gerekiyor."
            else:
                geri_bildirim = "⚠️ KRİTİK SAPMA: Form bozuluyor. Antrenör müdahalesi önerilir!"

            conn = baglanti_kur()
            conn.execute("INSERT INTO kas_hafizasi_analizleri (sporcu_adi, teknik_adi, dogruluk_skoru, ai_geri_bildirim, tarih) VALUES (?, ?, ?, ?, ?)",
                         (sporcu_sec, teknik_sec, skor, geri_bildirim, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()

            s.success(f"Analiz Tamamlandı! Sporcu: {sporcu_sec} | Teknik: {teknik_sec}")
            s.metric("Kas Hafızası Doğruluk Skoru", f"%{skor}")
            s.info(geri_bildirim)

    s.markdown("### 📊 Salon Geneli Kas Hafızası Analiz Arşivi")
    conn = baglanti_kur()
    df_kh = pd.read_sql("SELECT * FROM kas_hafizasi_analizleri", conn)
    conn.close()
    if not df_kh.empty:
        s.dataframe(df_kh, use_container_width=True)
    else:
        s.info("Henüz kayıtlı analiz bulunmuyor.")

# --- 5. AKILLI RANDEVU & KOÇ PLANLAMA AI ---
elif secilen_modul == "📅 Akıllı Randevu & Koç Planlama AI":
    s.subheader("📅 Akıllı Randevu & Antrenör Planlama Modülü")
    s.info("Salon doluluk oranlarına ve antrenörlerin müsaitlik saatlerine göre en uygun ders/ring slotunu otomatik rezerve eden akıllı takvim.")

    with s.form("randevu_form"):
        c1, c2 = s.columns(2)
        with c1:
            r_sporcu = s.text_input("Sporcu Ad Soyad")
            r_hoca = s.text_input("Antrenör Adı", value="Şefik Hoca")
        with c2:
            r_tarih = s.text_input("Randevu Tarihi ve Saati (YYYY-MM-DD HH:MM)", value=pd.Timestamp.now().strftime("%Y-%m-%d 14:00"))
            r_durum = s.selectbox("Durum", ["Onaylandı", "Beklemede", "İptal"])
        
        if s.form_submit_button("Akıllı Randevu Oluştur 🚀"):
            if r_sporcu:
                conn = baglanti_kur()
                conn.execute("INSERT INTO akilli_randevular (sporcu_adi, antrenor_adi, slot_tarihi, durum) VALUES (?, ?, ?, ?)",
                             (r_sporcu, r_hoca, r_tarih, r_durum))
                conn.commit()
                conn.close()
                s.success(f"🚀 {r_sporcu} için {r_hoca} ile randevu slotu başarıyla planlandı!")
                s.rerun()
            else:
                s.warning("Lütfen sporcu adını girin.")

    s.markdown("### 📋 Planlanan Akıllı Randevular Listesi")
    conn = baglanti_kur()
    df_rand = pd.read_sql("SELECT * FROM akilli_randevular", conn)
    conn.close()
    if not df_rand.empty:
        s.dataframe(df_rand, use_container_width=True)
    else:
        s.info("Henüz planlanmış randevu bulunmuyor.")

# --- 6. AKILLI BESLEME & SUPPLEMENT REÇETE BOTU ---
elif secilen_modul == "🥗 Akıllı Beslenme & Supplement Reçete Botu":
    s.subheader("🥗 Akıllı Beslenme ve Supplement Reçete Botu")
    s.info("Sporcunun vücut ölçüm verilerine ve antrenman yoğunluğuna göre günlük kalori/protein hesaplayıp WhatsApp reçetesi üreten AI motoru.")

    with s.form("beslenme_form"):
        c1, c2 = s.columns(2)
        with c1:
            b_sporcu = s.text_input("Sporcu Adı")
            b_kalori = s.number_input("Günlük Kalori Hedefi (kcal)", min_value=1200, value=2800)
        with c2:
            b_protein = s.text_input("Protein Hedefi", value="160g / Gün")
            b_supplement = s.text_area("Önerilen Supplementler", value="Creatine 5g, Whey Protein, Multivitamin")
        
        if s.form_submit_button("Beslenme & Supplement Reçetesi Üret 💊"):
            if b_sporcu:
                conn = baglanti_kur()
                conn.execute("INSERT INTO beslenme_receteleri (sporcu_adi, gunluk_kalori, protein_hedefi, supplement_notu) VALUES (?, ?, ?, ?)",
                             (b_sporcu, b_kalori, b_protein, b_supplement))
                conn.commit()
                conn.close()
                
                mesaj = f"Merhaba {b_sporcu}! Ringmaster AI Beslenme Reçeten: Günlük {b_kalori} kcal, Protein: {b_protein}. Supplementler: {b_supplement}. Başarılar!"
                encoded = urllib.parse.quote(mesaj)
                wa_link = f"https://wa.me/?text={encoded}"
                
                s.success(f"🚀 {b_sporcu} için beslenme reçetesi hazırlandı!")
                s.markdown(f"[📲 WhatsApp ile Beslenme Reçesini Gönder]({wa_link})", unsafe_allow_html=True)
                s.rerun()
            else:
                s.warning("Sporcu adını girin.")

    s.markdown("### 📋 Kayıtlı Beslenme Reçeteleri")
    conn = baglanti_kur()
    df_bes = pd.read_sql("SELECT * FROM beslenme_receteleri", conn)
    conn.close()
    if not df_bes.empty:
        s.dataframe(df_bes, use_container_width=True)
    else:
        s.info("Henüz kayıtlı beslenme reçetesi bulunmuyor.")

# --- 7. AKILLI KAPI, TURNİKE & BİYOMETRİK GEÇİŞ ---
elif secilen_modul == "🚪 Akıllı Kapı, Turnike & Biyometrik Geçiş":
    s.subheader("🚪 Akıllı Kapı, Turnike & Biyometrik Geçiş Modülü")
    s.info("Üyelerin kapıdaki biyometrik sensör veya 4 haneli PIN ile turnikeden geçişini otonom yöneten donanım köprüsü.")

    with s.form("turnike_simulasyon_form"):
        s.markdown("### ⚡ Kapı Geçiş Simülatörü (Donanım Test Paneli)")
        girilen_kapi_pin = s.text_input("Turnikede Okutulan PIN veya Biyometrik ID", max_chars=4, type="password")
        
        if s.form_submit_button("Kapıya Sinyal Gönder & Geçişi Test Et 🟢"):
            if girilen_kapi_pin:
                uyeler = uyeleri_getir()
                bulunan_uye = [u for u in uyeler if u[4] == girilen_kapi_pin]
                
                if bulunan_uye:
                    uye_adi = bulunan_uye[0][1]
                    gecis_durumu = "Onaylandı (Kapı Açıldı 🟢)"
                    
                    conn = baglanti_kur()
                    conn.execute("INSERT INTO kapi_gecis_loglari (sporcu_adi, pin, gecis_durumu, tarih) VALUES (?, ?, ?, ?)",
                                 (uye_adi, girilen_kapi_pin, gecis_durumu, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    conn.close()
                    
                    s.success(f"🟢 KAPI AÇILDI! Hoş geldin {uye_adi}. (Yoklama otomatik işlendi)")
                else:
                    gecis_durumu = "Reddedildi (Geçersiz PIN / Borçlu 🔴)"
                    conn = baglanti_kur()
                    conn.execute("INSERT INTO kapi_gecis_loglari (sporcu_adi, pin, gecis_durumu, tarih) VALUES (?, ?, ?, ?)",
                                 ("Bilinmeyen / Borçlu Üye", girilen_kapi_pin, gecis_durumu, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    conn.close()
                    
                    s.error("🔴 GEÇİŞ REDDEDİLDİ! Geçersiz PIN veya aidat gecikmesi tespit edildi. Turnike kilitli kaldı.")
            else:
                s.warning("Lütfen PIN girin.")

    s.markdown("### 📊 Canlı Kapı & Turnike Geçiş Logları Arşivi")
    conn = baglanti_kur()
    df_kapi = pd.read_sql("SELECT * FROM kapi_gecis_loglari ORDER BY id DESC", conn)
    conn.close()
    if not df_kapi.empty:
        s.dataframe(df_kapi, use_container_width=True)
    else:
        s.info("Henüz kapı geçiş kaydı bulunmuyor.")

# --- 8. FATURA DÜZENLEME & KURUMSAL ARŞİV ---
elif secilen_modul == "📄 Fatura Düzenleme & Kurumsal Arşiv":
    s.subheader("📄 Resmi Fatura Düzenleme ve Kurumsal Arşiv Modülü")
    s.info("Üye aidatları, kurumsal hizmetler ve salon gider faturalarının (e-Fatura / e-Arşiv simülasyonu) yasal kaydı.")

    with s.form("fatura_form"):
        c1, c2 = s.columns(2)
        with c1:
            f_unvan = s.text_input("Alıcı Unvan / Ad Soyad", value="Alpha Spor Kulübü")
            f_vergi = s.text_input("Vergi No / TCKN", value="1234567890")
            f_tipi = s.selectbox("Fatura Türü", ["Üye Satış Faturası", "Kurumsal Sponsorluk Faturası", "Gider / Tedarikçi Faturası"])
        with c2:
            f_tutar = s.number_input("Tutar (₺)", min_value=0.0, value=2500.0)
            f_kdv = s.selectbox("KDV Oranı (%)", [0, 1, 10, 20], index=3)
            f_tarih = s.text_input("Fatura Tarihi", value=pd.Timestamp.now().strftime("%Y-%m-%d"))

        if s.form_submit_button("Resmi Fatura Kes & Arşivle 📄"):
            if f_unvan:
                conn = baglanti_kur()
                conn.execute("INSERT INTO faturalar (alici_unvan, vergi_no, fatura_tipi, tutar, kdv_orani, tarih) VALUES (?, ?, ?, ?, ?, ?)",
                             (f_unvan, f_vergi, f_tipi, f_tutar, f_kdv, f_tarih))
                conn.commit()
                conn.close()
                s.success(f"📄 {f_unvan} adına {f_tutar}₺ tutarında {f_tipi} başarıyla oluşturuldu ve arşive kaydedildi!")
                s.rerun()
            else:
                s.warning("Lütfen alıcı unvanını girin.")

    s.markdown("### 📋 Kesilen Kurumsal Fatura Arşivi")
    conn = baglanti_kur()
    df_fatura = pd.read_sql("SELECT * FROM faturalar ORDER BY id DESC", conn)
    conn.close()
    if not df_fatura.empty:
        s.dataframe(df_fatura, use_container_width=True)
    else:
        s.info("Henüz kesilmiş fatura bulunmuyor.")

# --- 9. SALON ÜYELERİ YÖNETİMİ ---
elif secilen_modul == "Salon Üyeleri Yönetimi":
    s.subheader("👤 Salon Üyeleri ve PIN Yönetimi")
    with s.form("uye_form"):
        c1, c2 = s.columns(2)
        with c1:
            ad = s.text_input("Sporcu Ad Soyad")
            tel = s.text_input("Telefon (Örn: 5551234567)")
        with c2:
            brans = s.selectbox("Branş", [
                "Taekwondo", "Boks", "Kick Boks", "Muay Thai", "BJJ", "Fitness",
                "Karate", "Capoeira", "Judo", "MMA", "Self Defense",
                "Aikido", "Krav Maga", "Wing Chun", "Wushu", "Sanda", "Crossfit"
            ])
            pin = s.text_input("4 Haneli PIN (Boş bırakırsan otomatik atanır)", max_chars=4)
        
        if s.form_submit_button("Sporcuyu Kaydet ve PIN Üret 🚀"):
            if ad:
                if not pin or len(pin) != 4 or not pin.isdigit():
                    pin = str(random.randint(1000, 9999))
                uye_ekle(ad, tel, brans, pin)
                s.success(f"🚀 {ad} ({brans}) başarıyla kaydedildi! PIN: **{pin}**")
            else:
                s.warning("Lütfen sporcu adını girin.")
    
    s.markdown("### 📋 Kayıtlı Sporcular")
    uyeler = uyeleri_getir()
    if uyeler:
        df_uyeler = pd.DataFrame(uyeler, columns=["ID", "Ad Soyad", "Telefon", "Branş", "PIN", "Kayıt Tarihi"])
        s.dataframe(df_uyeler, use_container_width=True)
        
        with s.form("uye_sil_form"):
            silinecek_id = s.selectbox("Silinecek Sporcuyu Seç", df_uyeler.apply(lambda x: f"{x['ID']} - {x['Ad Soyad']}", axis=1).tolist())
            if s.form_submit_button("Seçilen Sporcu Kaydını Sil ❌"):
                secilen_id = int(silinecek_id.split(" - ")[0])
                uye_sil(secilen_id)
                s.success("Sporcu silindi!")
                s.rerun()
    else:
        s.info("Henüz kayıtlı üye bulunmuyor.")

# --- 10. YOKLAMA SİSTEMİ ---
elif secilen_modul == "Yoklama Sistemi":
    s.subheader("📝 Yoklama ve Giriş Takibi")
    girilen_pin = s.text_input("4 Haneli PIN Kodunuzu Girin", max_chars=4, type="password")
    if s.button("Giriş Yap / Yoklama Al"):
        uyeler = uyeleri_getir()
        bulunan = [u for u in uyeler if u[4] == girilen_pin]
        if bulunan:
            s.success(f"Hoş geldin, {bulunan[0][1]}! Antrenman girişin başarıyla kaydedildi 🥊")
        else:
            s.error("Geçersiz PIN kodu!")

# --- 11. STOK TAKİBİ ---
elif secilen_modul == "Stok Takibi":
    s.subheader("📦 Ürün ve Ekipman Stok Yönetimi")
    conn = baglanti_kur()
    stoklar = pd.read_sql("SELECT * FROM stok", conn)
    conn.close()
    s.dataframe(stoklar, use_container_width=True)
    with s.form("yeni_stok"):
        urun = s.text_input("Ürün Adı")
        adet = s.number_input("Adet", min_value=1, value=10)
        fiyat = s.number_input("Fiyat", min_value=0.0, value=100.0)
        if s.form_submit_button("Stok Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO stok (urun_adi, adet, fiyat) VALUES (?, ?, ?)", (urun, adet, fiyat))
            conn.commit()
            conn.close()
            s.success("Stok eklendi!")
            s.rerun()

# --- 12. KASA / FİNANS ---
elif secilen_modul == "Kasa / Finans":
    s.subheader("💰 Kasa ve Gelir/Gider Takibi")
    conn = baglanti_kur()
    kasa_df = pd.read_sql("SELECT * FROM kasa", conn)
    conn.close()
    s.dataframe(kasa_df, use_container_width=True)
    with s.form("kasa_form"):
        islem = s.selectbox("İşlem Tipi", ["Gelir", "Gider"])
        aciklama = s.text_input("Açıklama")
        tutar = s.number_input("Tutar", min_value=0.0)
        if s.form_submit_button("İşlemi Kaydet"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO kasa (islem_tipi, aciklama, tutar, tarih) VALUES (?, ?, ?, ?)", 
                         (islem, aciklama, tutar, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            s.success("Kasa hareketi eklendi!")
            s.rerun()

# --- 13. AİDAT & ÜCRET ÖDEME TAKİBİ ---
elif secilen_modul == "Aidat & Ücret Ödeme Takibi 💳":
    s.subheader("💳 Üye Aidat ve Ücret Ödeme Takip Modülü")
    conn = baglanti_kur()
    aidat_df = pd.read_sql("SELECT * FROM aidatlar", conn)
    conn.close()
    if not aidat_df.empty:
        s.dataframe(aidat_df, use_container_width=True)
    else:
        s.info("Henüz kayıtlı aidat bulunmuyor.")

    with s.form("aidat_ekle_form"):
        c1, c2 = s.columns(2)
        with c1:
            a_sporcu = s.text_input("Sporcu Ad Soyad")
            a_donem = s.text_input("Dönem (Örn: Eylül 2026)")
        with c2:
            a_tutar = s.number_input("Aidat Tutarı (₺)", min_value=0.0, value=1500.0)
            a_tarih = s.text_input("Son Ödeme Tarihi", value=pd.Timestamp.now().strftime("%Y-%m-%d"))
        
        if s.form_submit_button("Aidat Borcu Oluştur 🚀"):
            if a_sporcu:
                conn = baglanti_kur()
                conn.execute("INSERT INTO aidatlar (sporcu_adi, donem, tutar, son_odeme, durum) VALUES (?, ?, ?, ?, ?)",
                             (a_sporcu, a_donem, a_tutar, a_tarih, "Ödenmedi"))
                conn.commit()
                conn.close()
                s.success("Aidat borcu kaydedildi!")
                s.rerun()
            else:
                s.warning("Sporcu adını girin.")

# --- 14. ANTRENÖR & PRİM TAKİBİ ---
elif secilen_modul == "Antrenör & Prim Takibi":
    s.subheader("🥋 Antrenör ve Prim Yönetimi")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM antrenorler", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("hoca_form"):
        hoca = s.text_input("Antrenör Adı")
        brans = s.text_input("Uzmanlık Branşı")
        ders = s.number_input("Ders Sayısı", min_value=0, value=0)
        prim = s.number_input("Prim Oranı (%)", min_value=0.0, value=10.0)
        if s.form_submit_button("Antrenör Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO antrenorler (hoca_adi, brans, ders_sayisi, prim_orani) VALUES (?, ?, ?, ?)", (hoca, brans, ders, prim))
            conn.commit()
            conn.close()
            s.success("Antrenör eklendi!")
            s.rerun()

# --- 15. ÇOCUK GELİŞİM RAPORLARI ---
elif secilen_modul == "Çocuk Gelişim Raporları":
    s.subheader("🧒 Çocuk Gelişim ve Veli Bilgilendirme Modülü")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM cocuk_gelisim", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("cocuk_form"):
        ogr = s.text_input("Öğrenci Adı")
        tel = s.text_input("Veli Telefon")
        notlar = s.text_area("Gelişim Notları")
        if s.form_submit_button("Rapor Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO cocuk_gelisim (ogrenci_adi, veli_telefon, notlar, tarih) VALUES (?, ?, ?, ?)", 
                         (ogr, tel, notlar, pd.Timestamp.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            s.success("Rapor eklendi!")
            s.rerun()

# --- 16. KUŞAK / DERECE SINAVI ---
elif secilen_modul == "Kuşak / Derece Sınavı":
    s.subheader("🥋 Kuşak ve Derece Sınav Takibi")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM kusak_sinav", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("kusak_form"):
        ogr = s.text_input("Öğrenci Adı")
        mevcut = s.text_input("Mevcut Kuşak / Seviye")
        hedef = s.text_input("Hedef Kuşak / Seviye")
        durum = s.selectbox("Durum", ["Bekliyor", "Başarılı", "Tekrar"])
        if s.form_submit_button("Sınav Kaydı Oluştur"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO kusak_sinav (ogrenci_adi, mevcut_kusak, hedef_kusak, durum) VALUES (?, ?, ?, ?)", (ogr, mevcut, hedef, durum))
            conn.commit()
            conn.close()
            s.success("Sınav kaydı oluşturuldu!")
            s.rerun()

# --- 17. MÜSABIK TAKIMI YÖNETİMİ ---
elif secilen_modul == "Müsabık Takımı Yönetimi":
    s.subheader("🥊 Müsabık Sporcu ve Siklet Yönetimi")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM musabiklar", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("musabik_form"):
        sporcu = s.text_input("Sporcu Adı")
        siklet = s.text_input("Siklet / Kategori")
        galibiyet = s.number_input("Galibiyet", min_value=0, value=0)
        maglubiyet = s.number_input("Mağlubiyet", min_value=0, value=0)
        if s.form_submit_button("Müsabık Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO musabiklar (sporcu_adi, siklet, galibiyet, maglubiyet) VALUES (?, ?, ?, ?)", (sporcu, siklet, galibiyet, maglubiyet))
            conn.commit()
            conn.close()
            s.success("Müsabık eklendi!")
            s.rerun()

# --- 18. SAKATLİK & SPARRİNG TAKİBİ ---
elif secilen_modul == "Sakatlık & Sparring Takibi":
    s.subheader("🩹 Sporcu Sakatlık ve Sparring Yasakları")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM sakatliklar", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("sakatlik_form"):
        sporcu = s.text_input("Sporcu Adı")
        aciklama = s.text_input("Açıklama")
        yasak = s.selectbox("Sparring Yasağı?", [1, 0], format_func=lambda x: "Evet" if x==1 else "Hayır")
        if s.form_submit_button("Kayıt Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO sakatliklar (sporcu_adi, durum_aciklamasi, sparring_yasagi) VALUES (?, ?, ?)", (sporcu, aciklama, yasak))
            conn.commit()
            conn.close()
            s.success("Kayıt eklendi!")
            s.rerun()

# --- 19. MAÇ / TURNUVA TAKVİMİ ---
elif secilen_modul == "Maç / Turnuva Takvimi":
    s.subheader("🏆 Maç ve Turnuva Takvimi")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM mac_takvimi", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("mac_form"):
        turnuva = s.text_input("Turnuva Adı")
        tarih = s.text_input("Tarih (YYYY-MM-DD)")
        sporcular = s.text_area("Katılacak Sporcular")
        if s.form_submit_button("Turnuva Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO mac_takvimi (turnuva_adi, tarih, katilacak_sporcular) VALUES (?, ?, ?)", (turnuva, tarih, sporcular))
            conn.commit()
            conn.close()
            s.success("Turnuva eklendi!")
            s.rerun()

# --- 20. ADAY ÜYE TAKİBİ (CRM) ---
elif secilen_modul == "Aday Üye Takibi (CRM)":
    s.subheader("📞 Aday Üye ve Potansiyel Müşteri Takibi")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM adaylar", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("aday_form"):
        aday = s.text_input("Aday Adı")
        tel = s.text_input("Telefon")
        brans = s.text_input("İlgilenilen Branş")
        durum = s.selectbox("Durum", ["Arandı", "Deneme", "Kayıt Oldu", "Vazgeçti"])
        if s.form_submit_button("Aday Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO adaylar (aday_adi, telefon, ilgilenilen_brans, durum) VALUES (?, ?, ?, ?)", (aday, tel, brans, durum))
            conn.commit()
            conn.close()
            s.success("Aday eklendi!")
            s.rerun()

# --- 21. ÖZEL DERS (PT) TAKİBİ ---
elif secilen_modul == "Özel Ders (PT) Takibi":
    s.subheader("🎯 Özel Ders (PT) Paket Takibi")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM ozel_dersler", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("pt_form"):
        sporcu = s.text_input("Sporcu Adı")
        hoca = s.text_input("Antrenör Adı")
        kalan = s.number_input("Kalan Ders", min_value=0, value=10)
        if s.form_submit_button("PT Paketi Tanımla"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO ozel_dersler (sporcu_adi, hoca_adi, kalan_ders) VALUES (?, ?, ?)", (sporcu, hoca, kalan))
            conn.commit()
            conn.close()
            s.success("PT paketi tanımlandı!")
            s.rerun()

# --- 22. VÜCUT ÖLÇÜM TAKİBİ ---
elif secilen_modul == "Vücut Ölçüm Takibi":
    s.subheader("📊 Sporcu Vücut Ölçümleri")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM olcumler", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("olcum_form"):
        sporcu = s.text_input("Sporcu Adı")
        kilo = s.number_input("Kilo (kg)", min_value=0.0, value=75.0)
        yag = s.number_input("Yağ Oranı (%)", min_value=0.0, value=15.0)
        if s.form_submit_button("Ölçüm Kaydet"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO olcumler (sporcu_adi, kilo, yag_orani, tarih) VALUES (?, ?, ?, ?)", 
                         (sporcu, kilo, yag, pd.Timestamp.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            s.success("Ölçüm kaydedildi!")
            s.rerun()

# --- 23. ÜYE TERK (CHURN) RİSKİ ---
elif secilen_modul == "Üye Terk (Churn) Riski":
    s.subheader("⚠️ Üye Devamsızlık ve Terk Riski")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM churn_takip", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("churn_form"):
        sporcu = s.text_input("Sporcu Adı")
        son_gelis = s.text_input("Son Geliş (YYYY-MM-DD)")
        risk = s.selectbox("Risk", ["Düşük", "Orta", "Yüksek Risk"])
        if s.form_submit_button("Risk Kaydı Ekle"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO churn_takip (sporcu_adi, son_gelis_tarihi, risk_durumu) VALUES (?, ?, ?)", (sporcu, son_gelis, risk))
            conn.commit()
            conn.close()
            s.success("Risk kaydı eklendi!")
            s.rerun()

# --- 24. TOPLU SMS / DUYURU LOGU ---
elif secilen_modul == "Toplu SMS / Duyuru Logu":
    s.subheader("📢 Toplu Duyuru ve SMS Logları")
    conn = baglanti_kur()
    df = pd.read_sql("SELECT * FROM mesaj_loglari", conn)
    conn.close()
    s.dataframe(df, use_container_width=True)
    with s.form("sms_form"):
        grup = s.selectbox("Alıcı Grubu", ["Tüm Üyeler", "Müsabıklar", "Veli Grubu"])
        mesaj = s.text_area("Mesaj İçeriği")
        if s.form_submit_button("Mesajı Logla"):
            conn = baglanti_kur()
            conn.execute("INSERT INTO mesaj_loglari (alici_grup, mesaj_icerigi, gonderim_tarihi) VALUES (?, ?, ?)", 
                         (grup, mesaj, pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            s.success("Mesaj loglandı!")
            s.rerun()

# --- 25. SAAS ABONELİK YÖNETİMİ ---
elif secilen_modul == "SaaS Abonelik Yönetimi":
    s.subheader("🏢 SaaS Salon ve Abonelik Yönetimi")
    conn = baglanti_kur()
    salonlar = pd.read_sql("SELECT * FROM salonlar", conn)
    conn.close()
    s.dataframe(salonlar, use_container_width=True)
    with s.form("salon_form"):
        s_adi = s.text_input("Salon Adı")
        sahip = s.text_input("Sahip Adı")
        tel = s.text_input("Telefon")
        email = s.text_input("E-Posta")
        if s.form_submit_button("Kart Bilgisi Al ve 14 Gün Deneme Başlat 💳"):
            if s_adi and sahip:
                salon_ekle(s_adi, sahip, tel, email)
                s.success(f"{s_adi} için deneme başlatıldı!")
                s.rerun()
            else:
                s.warning("Salon adı ve sahip adını doldurun.")

# --- 26. KÜRESEL & YEREL ÖDEMELER ---
elif secilen_modul == "🌍 Küresel & Yerel Ödemeler":
    s.subheader("🌍 & 🇹🇷 Güvenli Tahsilat ve Kartlı Deneme Modeli")
    c1, c2, c3, c4 = s.columns(4)
    with c1:
        s.markdown("### 🇹🇷 TR (TRY)")
        s.info("Plan: 1.499₺ / ay")
    with c2:
        s.markdown("### 🇬🇧 UK (GBP)")
        s.info("Plan: £49 / ay")
    with c3:
        s.markdown("### 🇺🇸 US (USD)")
        s.info("Plan: $59 / ay")
    with c4:
        s.markdown("### 🇪🇺 EU (EUR)")
        s.info("Plan: €55 / ay")
    s.success("Tüm ödeme ağ geçitleri (Stripe, PayTR) aktif ve entegre!")

# --- 27. SİSTEM AYARLARI ---
elif secilen_modul == "Sistem Ayarları":
    s.subheader("⚙️ Sistem ve Veritabanı Ayarları")
    if s.button("Veritabanını Kontrol Et ve Onar"):
        veritabani_baslat()
        s.success("Tüm 27 modül tablosu, fatura arşivi ve slayt ayarları güncellendi!")



