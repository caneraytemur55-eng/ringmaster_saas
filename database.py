import sqlite3

def veritabanini_kur():
    # RingMaster veritabanı bağlantısı
    conn = sqlite3.connect("ringmaster.db")
    cursor = conn.cursor()

    # 1. SALON ÜYELERİ TABLE (Dövüşçüler)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uyeler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad_soyad TEXT NOT NULL,
        telefon TEXT UNIQUE NOT NULL,
        brans TEXT NOT NULL, -- Boks, Kickboks, Wing Chun vb.
        seviye TEXT DEFAULT 'Başlangıç' -- Başlangıç, Orta, Sparring Grubu
    )
    """)

    # 2. DERSLER VE KONTENJAN TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dersler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ders_adi TEXT NOT NULL, -- Örn: Akşam Sparring / Birebir Lapa
        hoca_adi TEXT NOT NULL,
        tarih_saat TEXT NOT NULL,
        kontenjan INTEGER NOT NULL
    )
    """)

    # 3. RANDEVULAR TABLE (Rezervasyonlar)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS randevular (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uye_id INTEGER,
        ders_id INTEGER,
        durum TEXT DEFAULT 'Onaylandı',
        FOREIGN KEY(uye_id) REFERENCES uyeler(id),
        FOREIGN KEY(ders_id) REFERENCES dersler(id)
    )
    """)

    conn.commit()
    conn.close()
    print(" RingMaster SQLite Veritabanı ve Tabloları Başarıyla Kuruldu!")

if __name__ == "__main__":
    veritabanini_kur()
    import sqlite3

DB_NAME = "ringmaster.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Üyeler Tablosu (Kuşak ve Aidat Alanları Eklendi)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uyeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            telefon TEXT NOT NULL,
            brans TEXT NOT NULL,
            kusak TEXT DEFAULT 'Beyaz Kuşak / Başlangıç',
            aidat_tarihi TEXT,
            aidat_durumu TEXT DEFAULT 'Ödendi',
            kayit_tarihi DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Randevular Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS randevular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uye_id INTEGER NOT NULL,
            tarih DATE NOT NULL,
            saat TIME NOT NULL,
            durum TEXT DEFAULT 'Planlandı',
            FOREIGN KEY (uye_id) REFERENCES uyeler (id)
        )
    ''')
    
    # Eski veritabanı güncellemeleri için kolon kontrolü
    cursor.execute("PRAGMA table_info(uyeler)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'kusak' not in columns:
        cursor.execute("ALTER TABLE uyeler ADD COLUMN kusak TEXT DEFAULT 'Beyaz Kuşak / Başlangıç'")
    if 'aidat_tarihi' not in columns:
        cursor.execute("ALTER TABLE uyeler ADD COLUMN aidat_tarihi TEXT")
    if 'aidat_durumu' not in columns:
        cursor.execute("ALTER TABLE uyeler ADD COLUMN aidat_durumu TEXT DEFAULT 'Ödendi'")

    conn.commit()
    conn.close()

def uye_ekle(ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO uyeler (ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu) VALUES (?, ?, ?, ?, ?, ?)",
        (ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu)
    )
    conn.commit()
    conn.close()

def uyeleri_getir():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, ad_soyad, telefon, brans, kusak, aidat_tarihi, aidat_durumu FROM uyeler")
    uyeler = cursor.fetchall()
    conn.close()
    return uyeler

def aidat_durum_guncelle(uye_id, yeni_durum):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE uyeler SET aidat_durumu = ? WHERE id = ?", (yeni_durum, uye_id))
    conn.commit()
    conn.close()

def kusak_guncelle(uye_id, yeni_kusak):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE uyeler SET kusak = ? WHERE id = ?", (yeni_kusak, uye_id))
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
    cursor.execute('''
        SELECT r.id, u.ad_soyad, u.telefon, r.tarih, r.saat, r.durum 
        FROM randevular r 
        JOIN uyeler u ON r.uye_id = u.id
        ORDER BY r.tarih DESC, r.saat DESC
    ''')
    randevular = cursor.fetchall()
    conn.close()
    return randevular

def randevu_sayisi():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM randevular")
    count = cursor.fetchone()[0]
    conn.close()
    return count