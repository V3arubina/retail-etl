# Retail ETL

Генерация ежедневных CSV-выгрузок чеков и загрузка их в PostgreSQL с автоматизацией по расписанию (cron).

- Генератор создаёт файлы вида `data/<shop>_<cash>.csv`.
- Схема CSV: `doc_id,item,category,amount,price,discount`.
- Загрузчик идемпотентно пишет данные в БД (перезаписывает строки чеков по `doc_id`).
- Автоматизация: **каждый день Пн–Сб** (воскресенье пропускается).
- Логи пишутся в файл и отображаются в консоли.

---

## 1) Требования

- Python **3.11+**
- PostgreSQL (например, **Render PostgreSQL**)
- (опционально) DBeaver для просмотра БД

---

## 2) Установка

````bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
- Генератор создаёт файлы вида `data/<shop>_<cash>.csv`
- Схема CSV: `doc_id,item,category,amount,price,discount`
- Загрузчик идемпотентно записывает данные в БД
- Автоматизация: **каждый день Пн–Сб** (воскресенье пропускается)

---

## 3) Конфигурация

Создайте файл `.env` в корне
Параметры для Render возьмите в **Dashboard → PostgreSQL → Connections → External**.

```dotenv
# === Render PostgreSQL (External) ===
PGHOST=dpg-...ap-southeast-1.render.com
PGPORT=5432
PGDATABASE=retail_db_uu01
PGUSER=retail_db_uu01_user
PGPASSWORD=ВАШ_ПАРОЛЬ
PGSSLMODE=require

# === Локальные пути ===
DATA_DIR=./data
LOG_DIR=./logs

---

## 4) Структура проекта

````

.
├─ src/
│ ├─ generate_exports.py # генерация CSV
│ ├─ load_to_db_postgres.py # загрузка в PostgreSQL
│ ├─ config.py # конфиг: .env, пути, параметры
│ └─ utils.py # логирование (файл + консоль, ротация)
├─ sql/
│ └─ ddl.sql # DDL PostgreSQL (таблицы/индексы)
├─ data/ # CSV (генерируются; в git игнор)
├─ logs/ # логи (в git игнор)
├─ img/ # скриншоты (cron, DBeaver, psql, логи)
├─ README.md
└─ requirements.txt

````

---

## 5) Схема БД (PostgreSQL)

`sql/ddl.sql` создаёт таблицы:

- `shop (shop_id PK)`
- `cash_register (shop_id, cash_id) PK`
- `receipt (doc_id PK, shop_id, cash_id, ingest_date)`
- `receipt_item (doc_id FK → receipt, item, category, amount, price, discount, line_total generated)`

---

## 6) Генерация CSV

```bash
./.venv/bin/python src/generate_exports.py
# создаст data/<shop>_<cash>.csv (в воскресенье пропускает)
````

---

## 7) Загрузка в PostgreSQL

```bash
./.venv/bin/python src/load_to_db_postgres.py
```

---

## 8) Автоматизация (cron, **Пн–Сб**)

```bash
crontab -l
```

---
