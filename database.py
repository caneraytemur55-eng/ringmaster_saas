import sqlite3
import datetime

DB_NAME = "ringmaster.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Üyeler Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uyeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT NOT NULL,
            brans TEXT NOT NULL,
            kusak TEXT DEFAULT 'Beyaz Kuşak / Başlangıç',
            aidat_tarihi TEXT,
            aidat_durumu TEXT DEFAULT 'Ödendi',
            son_sinav_tarihi TEXT,
            pin_kod TEXT DEFAULT '1234',
            katilinan_ders INTEGER DEFAULT 0,
            grup_tipi TEXT DEFAULT 'Yetişkin / Genel',
            veli_adi TEXT DEFAULT '',
            veli_telefonu TEXT DEFAULT '',
            gelisim_notu TEXT DEFAULT 'Gelişimi düzenli takip ediliyor.',
            kayit_tarihi DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # 2. Antrenörler Tablosu (YENİ!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS antrenorler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT NOT NULL,
            brans TEXT NOT NULL,
            maas_tipi TEXT DEFAULT 'Sabit + Prim',
            sabit_maas REAL DEFAULT 0.0,
            prim_yuzdesi REAL DEFAULT 40.0,
            kayit_tarihi DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # 3. Randevular Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS randevular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uye_id INTEGER NOT NULL,
            tarih DATE NOT NULL DEFAULT CURRENT_DATE,
            saat TIME NOT NULL DEFAULT '18:00',
            durum TEXT DEFAULT 'Planlandı',
            FOREIGN KEY (uye_id) REFERENCES uyeler (id)
        )
    ''')

    # 4. Deneme Dersi Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deneme_dersleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT NOT NULL,
            brans TEXT NOT NULL,
            tarih DATE NOT NULL,
            saat TIME NOT NULL,
            durum TEXT DEFAULT 'Bekliyor',
            notlar TEXT
        )
    ''')

    # 5. Özel Ders (PT) Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ozel_dersler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT NOT NULL,
            brans TEXT NOT NULL,
            toplam_seans INTEGER NOT NULL DEFAULT 10,
            kalan_seans INTEGER NOT NULL DEFAULT 10,
            paket_ucreti REAL NOT NULL DEFAULT 0,
            ucret_durumu TEXT DEFAULT 'Ödeme Bekliyor',
            kayit_tarihi DATE DEFAULT CURRENT_DATE,
            notlar TEXT
        )
    ''')
    
    # 6. Kasa Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kasa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            islem_tipi TEXT NOT NULL,
            kategori TEXT NOT NULL,
            tutar REAL NOT NULL,
            aciklama TEXT,
            tarih DATE DEFAULT CURRENT_DATE
        )
    ''')

    # 7. Ölçüm Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS olcumler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uye_id INTEGER NOT NULL,
            tarih DATE DEFAULT CURRENT_DATE,
            kilo REAL,
            yag_orani REAL,
            bel REAL,
            gogus REAL,
            pazu REAL,
            notlar TEXT,
            FOREIGN KEY (uye_id) REFERENCES uyeler (id)
        )
    ''')
    
    # 8. Müsabık Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS musabiklar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uye_id INTEGER NOT NULL,
            stili TEXT DEFAULT 'Ortodoks (Sağak)',
            hedef_siklet REAL DEFAULT 70.0,
            galibiyet INTEGER DEFAULT 0,
            maglubiyet INTEGER DEFAULT 0,
            beraberlik INTEGER DEFAULT 0,
            ko_tko INTEGER DEFAULT 0,
            yaklasan_mac_tarihi DATE,
            organizasyon TEXT,
            FOREIGN KEY (uye_id) REFERENCES uyeler (id)
        )
    ''')

    # 9. Sakatlık Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sakatliklar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uye_id INTEGER NOT NULL,
            sakatlik_bolgesi TEXT NOT NULL,
            sparring_yasak_gun INTEGER DEFAULT 14,
            izin_verilen_antrenman TEXT,
            baslangic_tarihi DATE DEFAULT CURRENT_DATE,
            durum TEXT DEFAULT 'Aktif Sakatlık 🔴',
            FOREIGN KEY (uye_id) REFERENCES uyeler (id)
        )
    ''')

    # 10. Ürün & Stok Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urunler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_adi TEXT NOT NULL,
            kategori TEXT DEFAULT 'Ekipman',
            stok_miktari INTEGER DEFAULT 10,
            alis_fiyati REAL DEFAULT 0.0,
            satis_fiyati REAL DEFAULT 0.0
        )
    ''')

    # 11. Sistem Ayarları
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sistem_ayarlari (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            kurulum_tarihi DATE DEFAULT CURRENT_DATE
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO sistem_ayarlari (id, kurulum_tarihi) VALUES (1, CURRENT_DATE)")
    
    conn.commit()
    conn.close()

def kurulum_tarihi_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT kurulum_tarihi FROM sistem_ayarlari WHERE id = 1")
        row = cursor.fetchone()
        tarih_str = row[0] if row else str(datetime.date.today())
    except Exception:
        tarih_str = str(datetime.date.today())
    conn.close()
    return tarih_str

# ANTRENÖR FONKSİYONLARI (YENİ!)
def antrenor_ekle(ad_soyad, telefon, brans, maas_tipi, sabit_maas, prim_yuzdesi):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO antrenorler (ad_soyad, telefon, brans, maas_tipi, sabit_maas, prim_yuzdesi)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (ad_soyad, telefon, brans, maas_tipi, sabit_maas, prim_yuzdesi))
    conn.commit()
    conn.close()

def antrenorleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, ad_soyad, telefon, brans, maas_tipi, sabit_maas, prim_yuzdesi FROM antrenorler ORDER BY id DESC")
        res = cursor.fetchall()
    except Exception:
        res = []
    conn.close()
    return res

def cocuk_rapor_guncelle(uye_id, yeni_not):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE uyeler SET gelisim_notu = ? WHERE id = ?", (yeni_not, uye_id))
    conn.commit()
    conn.close()

def urun_ekle(urun_adi, kategori, stok_miktari, alis_fiyati, satis_fiyati):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO urunler (urun_adi, kategori, stok_miktari, alis_fiyati, satis_fiyati)
        VALUES (?, ?, ?, ?, ?)
    ''', (urun_adi, kategori, stok_miktari, alis_fiyati, satis_fiyati))
    conn.commit()
    conn.close()

def urunleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, urun_adi, kategori, stok_miktari, alis_fiyati, satis_fiyati FROM urunler ORDER BY id DESC")
        urunler = cursor.fetchall()
    except Exception:
        urunler = []
    conn.close()
    return urunler

def urun_satisi_yap(urun_id, adet, toplam_tutar, odeme_tipi):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE urunler SET stok_miktari = MAX(0, stok_miktari - ?) WHERE id = ?", (adet, urun_id))
    cursor.execute("SELECT urun_adi FROM urunler WHERE id = ?", (urun_id,))
    row = cursor.fetchone()
    u_adi = row[0] if row else "Ekipman"
    cursor.execute(
        "INSERT INTO kasa (islem_tipi, kategori, tutar, aciklama) VALUES (?, ?, ?, ?)",
        ("Gelir", "Ekipman Satışı", toplam_tutar, f"POS Satış: {adet}x {u_adi} ({odeme_tipi})")
    )
    conn.commit()
    conn.close()

def musabik_ekle_guncelle(uye_id, stili, hedef_siklet, galibiyet, maglubiyet, beraberlik, ko_tko, yaklasan_mac_tarihi, organizasyon):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM musabiklar WHERE uye_id = ?", (uye_id,))
    row = cursor.fetchone()
    if row:
        cursor.execute('''
            UPDATE musabiklar SET stili=?, hedef_siklet=?, galibiyet=?, maglubiyet=?, beraberlik=?, ko_tko=?, yaklasan_mac_tarihi=?, organizasyon=?
            WHERE uye_id=?
        ''', (stili, hedef_siklet, galibiyet, maglubiyet, beraberlik, ko_tko, str(yaklasan_mac_tarihi), organizasyon, uye_id))
    else:
        cursor.execute('''
            INSERT INTO musabiklar (uye_id, stili, hedef_siklet, galibiyet, maglubiyet, beraberlik, ko_tko, yaklasan_mac_tarihi, organizasyon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (uye_id, stili, hedef_siklet, galibiyet, maglubiyet, beraberlik, ko_tko, str(yaklasan_mac_tarihi), organizasyon))
    conn.commit()
    conn.close()

def musabik_getir(uye_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, stili, hedef_siklet, galibiyet, maglubiyet, beraberlik, ko_tko, yaklasan_mac_tarihi, organizasyon FROM musabiklar WHERE uye_id = ?", (uye_id,))
        res = cursor.fetchone()
    except Exception:
        res = None
    conn.close()
    return res

def tum_yaklasan_maclari_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT u.ad_soyad, u.brans, m.hedef_siklet, m.yaklasan_mac_tarihi, m.organizasyon, u.telefon
            FROM musabiklar m
            JOIN uyeler u ON m.uye_id = u.id
            WHERE m.yaklasan_mac_tarihi IS NOT NULL AND m.yaklasan_mac_tarihi != ''
            ORDER BY m.yaklasan_mac_tarihi ASC
        ''')
        maclar = cursor.fetchall()
    except Exception:
        maclar = []
    conn.close()
    return maclar

def sakatlik_ekle(uye_id, sakatlik_bolgesi, sparring_yasak_gun, izin_verilen_antrenman):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sakatliklar (uye_id, sakatlik_bolgesi, sparring_yasak_gun, izin_verilen_antrenman)
        VALUES (?, ?, ?, ?)
    ''', (uye_id, sakatlik_bolgesi, sparring_yasak_gun, izin_verilen_antrenman))
    conn.commit()
    conn.close()

def sakatliklari_getir(uye_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, sakatlik_bolgesi, sparring_yasak_gun, izin_verilen_antrenman, baslangic_tarihi, durum FROM sakatliklar WHERE uye_id = ? ORDER BY id DESC", (uye_id,))
        rows = cursor.fetchall()
    except Exception:
        rows = []
    conn.close()
    return rows

def sakatlik_kapat(sakatlik_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE sakatliklar SET durum = 'İyileşti 🟢' WHERE id = ?", (sakatlik_id,))
    conn.commit()
    conn.close()

def pin_ile_yoklama_al(pin):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, ad_soyad, katilinan_ders, brans FROM uyeler WHERE pin_kod = ?", (pin,))
    row = cursor.fetchone()
    if row:
        u_id, ad, ders_sayisi, brans = row
        yeni_ders = ders_sayisi + 1
        cursor.execute("UPDATE uyeler SET katilinan_ders = ? WHERE id = ?", (yeni_ders, u_id))
        conn.commit()
        conn.close()
        return True, ad, yeni_ders, brans
    conn.close()
    return False, None, 0, None

def ders_sayisi_arttir(uye_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE uyeler SET katilinan_ders = katilinan_ders + 1 WHERE id = ?", (uye_id,))
    conn.commit()
    conn.close()

def kusak_yukselt_sifirla(uye_id, yeni_kusak):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE uyeler SET kusak = ?, katilinan_ders = 0, son_sinav_tarihi = ? WHERE id = ?", (yeni_kusak, str(datetime.date.today()), uye_id))
    conn.commit()
    conn.close()

def uykudaki_uyeleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, ad_soyad, telefon, brans, aidat_tarihi, aidat_durumu FROM uyeler WHERE aidat_durumu = 'Ödeme Bekliyor'")
        uykudakiler = cursor.fetchall()
    except Exception:
        uykudakiler = []
    conn.close()
    return uykudakiler

def olcum_ekle(uye_id, kilo, yag_orani, bel, gogus, pazu, notlar):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO olcumler (uye_id, kilo, yag_orani, bel, gogus, pazu, notlar) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (uye_id, kilo, yag_orani, bel, gogus, pazu, notlar)
    )
    conn.commit()
    conn.close()

def olcumleri_getir(uye_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, tarih, kilo, yag_orani, bel, gogus, pazu, notlar FROM olcumler WHERE uye_id = ? ORDER BY id DESC", (uye_id,))
        olcumler = cursor.fetchall()
    except Exception:
        olcumler = []
    conn.close()
    return olcumler

def kasa_islem_ekle(islem_tipi, kategori, tutar, aciklama):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO kasa (islem_tipi, kategori, tutar, aciklama) VALUES (?, ?, ?, ?)",
        (islem_tipi, kategori, tutar, aciklama)
    )
    conn.commit()
    conn.close()

def kasa_ozet_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(tutar) FROM kasa WHERE islem_tipi = 'Gelir'")
        toplam_gelir = cursor.fetchone()[0] or 0.0
        
        cursor.execute("SELECT SUM(tutar) FROM kasa WHERE islem_tipi = 'Gider'")
        toplam_gider = cursor.fetchone()[0] or 0.0
    except Exception:
        toplam_gelir, toplam_gider = 0.0, 0.0
    conn.close()
    return toplam_gelir, toplam_gider, toplam_gelir - toplam_gider

def kasa_islemleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, islem_tipi, kategori, tutar, aciklama, tarih FROM kasa ORDER BY id DESC")
        islemler = cursor.fetchall()
    except Exception:
        islemler = []
    conn.close()
    return islemler

def uye_ekle(ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi, pin_kod="1234", grup_tipi="Yetişkin / Genel", veli_adi="", veli_telefonu="", gelisim_notu=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO uyeler (ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi, pin_kod, grup_tipi, veli_adi, veli_telefonu, gelisim_notu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi, pin_kod, grup_tipi, veli_adi, veli_telefonu, gelisim_notu)
    )
    conn.commit()
    conn.close()

def uyeleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi, pin_kod, katilinan_ders, grup_tipi, veli_adi, veli_telefonu, gelisim_notu FROM uyeler")
        uyeler = cursor.fetchall()
    except Exception:
        uyeler = []
    conn.close()
    return uyeler

def deneme_ekle(ad_soyad, telefon, brans, tarih, saat, notlar):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO deneme_dersleri (ad_soyad, telefon, brans, tarih, saat, notlar) VALUES (?, ?, ?, ?, ?, ?)",
        (ad_soyad, telefon, brans, tarih, saat, notlar)
    )
    conn.commit()
    conn.close()

def denemeleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, ad_soyad, telefon, brans, tarih, saat, durum, notlar FROM deneme_dersleri ORDER BY id DESC")
        denemeler = cursor.fetchall()
    except Exception:
        denemeler = []
    conn.close()
    return denemeler

def ozel_ders_ekle(ad_soyad, telefon, brans, toplam_seans, paket_ucreti, ucret_durumu, notlar):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ozel_dersler (ad_soyad, telefon, brans, toplam_seans, kalan_seans, paket_ucreti, ucret_durumu, notlar) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (ad_soyad, telefon, brans, toplam_seans, toplam_seans, paket_ucreti, ucret_durumu, notlar)
    )
    conn.commit()
    conn.close()

def ozel_dersleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, ad_soyad, telefon, brans, toplam_seans, kalan_seans, paket_ucreti, ucret_durumu, kayit_tarihi, notlar FROM ozel_dersler ORDER BY id DESC")
        dersler = cursor.fetchall()
    except Exception:
        dersler = []
    conn.close()
    return dersler

def ozel_ders_seans_dus(pt_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE ozel_dersler SET kalan_seans = MAX(0, kalan_seans - 1) WHERE id = ?", (pt_id,))
    conn.commit()
    conn.close()

def ozel_ders_ucret_guncelle(pt_id, yeni_durum):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE ozel_dersler SET ucret_durumu = ? WHERE id = ?", (yeni_durum, pt_id))
    conn.commit()
    conn.close()

def randevulari_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT r.id, u.ad_soyad, u.telefon, r.tarih, r.saat, r.durum 
            FROM randevular r 
            JOIN uyeler u ON r.uye_id = u.id
            ORDER BY r.id DESC
        ''')
        randevular = cursor.fetchall()
    except Exception:
        randevular = []
    conn.close()
    return randevular

