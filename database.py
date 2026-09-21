-- Abonelik Planları Tablosu
CREATE TABLE abonelik_planlari (
    id SERIAL PRIMARY KEY,
    plan_anahtar VARCHAR(50) UNIQUE NOT NULL, -- 'baslangic', 'profesyonel'
    isim_tr VARCHAR(100) NOT NULL,
    isim_en VARCHAR(100) NOT NULL
);

-- Plan Fiyatları Tablosu (Çoklu Para Birimi Desteği: TRY, USD, GBP, EUR)
CREATE TABLE plan_fiyatlari (
    id SERIAL PRIMARY KEY,
    plan_anahtar VARCHAR(50) REFERENCES abonelik_planlari(plan_anahtar),
    para_birimi VARCHAR(3) NOT NULL, -- 'TRY', 'USD', 'GBP', 'EUR'
    miktar INT NOT NULL,           -- Kuruş/Cent cinsi (Örn: 1900 = 19.00 EUR)
    gecit VARCHAR(50) NOT NULL     -- 'iyzico', 'stripe'
);

