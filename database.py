# database.py dosyasına eklenecek fonksiyon:
def uye_sil(uye_id):
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM uyeler WHERE id = ?", (uye_id,))
    conn.commit()
    conn.close()



