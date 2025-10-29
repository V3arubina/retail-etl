 -- Магазины
CREATE TABLE IF NOT EXISTS shop (
    shop_id INT PRIMARY KEY
);

-- Кассы
CREATE TABLE IF NOT EXISTS cash_register (
    shop_id INT NOT NULL,
    cash_id INT NOT NULL,
    PRIMARY KEY (shop_id, cash_id),
    FOREIGN KEY (shop_id) REFERENCES shop (shop_id)
);

-- Чеки
CREATE TABLE IF NOT EXISTS receipt (
    doc_id      TEXT PRIMARY KEY,
    shop_id     INT  NOT NULL,
    cash_id     INT  NOT NULL,
    ingest_date DATE NOT NULL,
    FOREIGN KEY (shop_id) REFERENCES shop (shop_id),
    FOREIGN KEY (shop_id, cash_id) REFERENCES cash_register (shop_id, cash_id)
);

-- Позиции чеков 
CREATE TABLE IF NOT EXISTS receipt_item (
    id       BIGSERIAL PRIMARY KEY,
    doc_id   TEXT NOT NULL,
    item     TEXT NOT NULL,
    category TEXT NOT NULL,
    amount   NUMERIC(12,3) NOT NULL CHECK (amount  >= 0),
    price    NUMERIC(12,2) NOT NULL CHECK (price   >= 0),
    discount NUMERIC(12,2) NOT NULL CHECK (discount >= 0),
    FOREIGN KEY (doc_id) REFERENCES receipt (doc_id)
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_receipt_ingest_date
    ON receipt (ingest_date);

CREATE INDEX IF NOT EXISTS idx_receipt_item_category
    ON receipt_item (category);

-- Ускоряет DELETE по doc_id
CREATE INDEX IF NOT EXISTS idx_receipt_item_doc
    ON receipt_item (doc_id);
