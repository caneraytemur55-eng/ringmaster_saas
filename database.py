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
            kayit_tarihi DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # 2. Randevular Tablosu
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

    # 3. Deneme Dersi Tablosu
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

    # 4. Özel Ders (PT) Tablosu
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
    
    # 5. Kasa / Gelir-Gider Tablosu (YENİ!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kasa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            islem_tipi TEXT NOT NULL, -- 'Gelir' veya 'Gider'
            kategori TEXT NOT NULL,   -- 'Aidat', 'PT Ödemesi', 'Kira', 'Fatura', 'Ekipman', 'Maaş', 'Diğer'
            tutar REAL NOT NULL,
            aciklama TEXT,
            tarih DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # 6. Sistem Lisans/Abonelik Tablosu
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

# KASA FONKSİYONLARI (YENİ!)
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

# DİĞER MEVCUT FONKSİYONLAR
def uye_ekle(ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO uyeler (ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi)
    )
    conn.commit()
    conn.close()

def uyeleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu, son_sinav_tarihi FROM uyeler")
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

def aidat_durum_guncelle(uye_id, yeni_durum):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE uyeler SET aidat_durumu = ? WHERE id = ?", (yeni_durum, uye_id))
    conn.commit()
    conn.close()

def kusak_guncelle(uye_id, yeni_kusak, yeni_sinav_tarihi):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE uyeler SET kusak = ?, son_sinav_tarihi = ? WHERE id = ?", (yeni_kusak, yeni_sinav_tarihi, uye_id))
    conn.commit()
    conn.close()

def randevu_ekle(uye_id, tarih, saat):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO randevular (uye_id, tarih, saat) VALUES (?, ?, ?)", (uye_id, tarih, saat))
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

def randevu_sayisi():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM randevular")
        count = cursor.fetchone()[0]
    except Exception:
        count = 0
    conn.close()
    return count
