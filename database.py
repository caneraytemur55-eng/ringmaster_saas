-- Abonelik Planları Tablosu
CREATE TABLE subscription_plans (
    id SERIAL PRIMARY KEY,
    plan_key VARCHAR(50) UNIQUE NOT NULL, -- 'starter', 'pro'
    name_tr VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL
);

-- Plan Fiyatları Tablosu (Çoklu Para Birimi Desteği)
CREATE TABLE plan_prices (
    id SERIAL PRIMARY KEY,
    plan_key VARCHAR(50) REFERENCES subscription_plans(plan_key),
    currency VARCHAR(3) NOT NULL, -- 'TRY', 'USD', 'GBP', 'EUR'
    amount INT NOT NULL,          -- Kuruş/Cent cinsinden (Örn: 1900 = 19.00 EUR)
    gateway VARCHAR(50) NOT NULL  -- 'iyzico', 'stripe'
);

