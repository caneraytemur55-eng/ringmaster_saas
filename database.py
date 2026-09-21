import sqlite3
from datetime import datetime

DB_NAME = "ringmaster.db"

def baglanti_kur():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def veritabani_baslat():
    conn = baglanti_kur()
    cursor = conn.cursor()
    
    # 1. Üyeler Tablosu (PIN kodu ve üyelik bilgileriyle)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uyeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT,
            brans TEXT,
            paket TEXT,
            pin_kodu TEXT,
            kayit_tarihi TEXT
        )
    """)

    # 2. Yoklama Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yoklamalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pin_kodu TEXT,
            ad_soyad TEXT,
            giris_zamani TEXT
        )
    """)

    # 3. Stok / POS Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_adi TEXT NOT NULL,
            adet INTEGER,
            fiyat REAL
        )
    """)

    # Başlangıç stokları yoksa ekleyelim
    cursor.execute("SELECT COUNT(*) FROM stok")
    if cursor.fetchone()[0] == 0:
        ornek_stoklar = [
            ("Deri Eldiven", 15, 1200.0),
            ("Dişlik", 30, 150.0),
            ("El Bandajı", 45, 250.0),
            ("Antrenman Şortu", 20, 650.0)
        ]
        cursor.executemany("INSERT INTO stok (urun_adi, adet, fiyat) VALUES (?, ?, ?)", ornek_stoklar)

    # 4. Kasa & Finans Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kasa (
            id INTEGER PRIMARY KEY AUTOINCREMENT\,,
            islem_tipi TEXT,
            aciklama TEXT,
            tutar REAL,
            tarih TEXT
        )
    """)

    conn.commit()
    conn.close()

# Üye ekleme fonksiyonu
def uye_ekle(ad_soyad, telefon, brans, paket, pin_kodu):
    conn = baglanti_kur()
    cursor = conn.cursor()
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO uyeler (ad_soyad, telefon, brans, paket, pin_kodu, kayit_tarihi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ad_soyad, telefon, brans, paket, pin_kodu, tarih))
    conn.commit()
    conn.close()

# Tüm üyeleri getirme
def uyeleri_getir():
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ad_soyad, telefon, brans, paket, pin_kodu, kayit_tarihi FROM uyeler")
    veriler = cursor.fetchall()
    conn.close()
    return veriler



