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