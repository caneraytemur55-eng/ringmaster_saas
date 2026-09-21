import sqlite3
from datetime import datetime, timedelta

DB_NAME = "ringmaster.db"

def baglanti_kur():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def veritabani_baslat():
    conn = baglanti_kur()
    cursor = conn.cursor()
    
    # 1. Üyeler Tablosu (Deneme süresi ve abonelik alanlarıyla güncellendi)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uyeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT,
            brans TEXT,
            paket TEXT,
            pin_kodu TEXT,
            kayit_tarihi TEXT,
            deneme_bitis TEXT,
            abonelik_durumu TEXT
        )
    """)

    # Diğer tablolar aynı kalıyor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yoklamalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pin_kodu TEXT,
            ad_soyad TEXT,
            brans TEXT,
            giris_zamani TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_adi TEXT NOT NULL,
            adet INTEGER,
            fiyat REAL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM stok")
    if cursor.fetchone()[0] == 0:
        ornek_stoklar = [
            ("Deri Eldiven", 15, 1200.0),
            ("Dişlik", 30, 150.0),
            ("El Bandajı", 45, 250.0),
            ("Antrenman Şortu", 20, 650.0)
        ]
        cursor.executemany("INSERT INTO stok (urun_adi, adet, fiyat) VALUES (?, ?, ?)", ornek_stoklar)

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

    conn.commit()
    conn.close()

def uye_ekle(ad_soyad, telefon, brans, paket, pin_kodu):
    conn = baglanti_kur()
    cursor = conn.cursor()
    simdi = datetime.now()
    kayit_tarihi = simdi.strftime("%Y-%m-%d %H:%M")
    # 15 günlük deneme süresi hesaplama
    deneme_bitis = (simdi + timedelta(days=15)).strftime("%Y-%m-%d")
    abonelik_durumu = "15 Günlük Deneme Süresi"
    
    cursor.execute("""
        INSERT INTO uyeler (ad_soyad, telefon, brans, paket, pin_kodu, kayit_tarihi, deneme_bitis, abonelik_durumu) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ad_soyad, telefon, brans, paket, pin_kodu, kayit_tarihi, deneme_bitis, abonelik_durumu))
    conn.commit()
    conn.close()

def uyeleri_getir():
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ad_soyad, telefon, brans, paket, pin_kodu, kayit_tarihi, deneme_bitis, abonelik_durumu FROM uyeler")
    veriler = cursor.fetchall()
    conn.close()
    return veriler



