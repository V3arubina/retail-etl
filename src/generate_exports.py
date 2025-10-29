from pathlib import Path
from datetime import date, datetime, UTC
import random, string
import pandas as pd

from config import DATA_DIR, LOG_DIR, N_SHOPS, MIN_CASH, MAX_CASH, ROWS_PER_CASH
from utils import setup_logger

# Инициализация генератора случайных чисел с фиксированным сидом по дате
RNG = random.Random(int(date.today().strftime("%Y%m%d")))

# Каталог товаров
CATALOG = (
    [
        ("Одежда", x)
        for x in [
            "Куртка демисезонная",
            "Пуховик лёгкий",
            "Пальто классическое",
            "Плащ",
            "Джинсы прямые",
            "Брюки чинос",
            "Юбка миди",
            "Шорты",
        ]
    ]
    + [
        ("Обувь", x)
        for x in ["Кроссовки", "Ботинки кожаные", "Туфли классические", "Лоферы"]
    ]
    + [
        ("Аксессуары", x)
        for x in ["Ремень кожаный", "Шарф шерстяной", "Шапка", "Перчатки"]
    ]
)


def random_doc_id(k: int = 10) -> str:
    return "".join(RNG.choices(string.ascii_uppercase + string.digits, k=k))


def sample_row() -> tuple[str, str, int, float, float]:
    category, item = RNG.choice(CATALOG)
    amount = RNG.randint(1, 3)
    price = round(RNG.uniform(200, 5000), 2)
    max_disc = round(amount * price * 0.35, 2)
    discount = round(RNG.uniform(0, max_disc), 2) if RNG.random() < 0.5 else 0.0
    return category, item, amount, price, discount


def build_file(n_rows: int) -> pd.DataFrame:
    data, produced = [], 0
    while produced < n_rows:
        did = random_doc_id()
        for _ in range(RNG.randint(1, 4)):  # 1–4 строк на чек
            if produced >= n_rows:
                break
            cat, item, amt, price, disc = sample_row()
            data.append(
                {
                    "doc_id": did,
                    "item": item,
                    "category": cat,
                    "amount": int(amt),
                    "price": float(round(price, 2)),
                    "discount": float(round(disc, 2)),
                }
            )
            produced += 1
    return pd.DataFrame.from_records(
        data, columns=["doc_id", "item", "category", "amount", "price", "discount"]
    )


def main() -> None:
    logger = setup_logger(LOG_DIR, "generate")

    # пропуск по воскресеньям
    if datetime.now(UTC).weekday() == 6:
        logger.info("Воскресенье — генерация пропущена.")
        return

    day_dir = DATA_DIR / date.today().strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Старт генерации за {day_dir.name} → {day_dir}")

    for shop in range(1, N_SHOPS + 1):
        for cash in range(1, RNG.randint(MIN_CASH, MAX_CASH) + 1):
            df = build_file(ROWS_PER_CASH)
            out = day_dir / f"{shop}_{cash}.csv"
            df.to_csv(out, index=False, encoding="utf-8-sig")
            logger.info(f"Сгенерирован {out} rows={len(df)}")

    logger.info("Генерация завершена.")


if __name__ == "__main__":
    main()
