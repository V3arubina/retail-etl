from pathlib import Path
from datetime import date
import random, string, csv, logging

DATA_DIR = Path("data")
N_SHOPS = 5
MIN_CASH, MAX_CASH = 1, 4
ROWS_PER_CASH = 300

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO
)
logger = logging.getLogger("generate")

RNG = random.Random(int(date.today().strftime("%Y%m%d")))

CATALOG = (
    [
        ("Одежда", x)
        for x in (
            "Куртка демисезонная",
            "Пуховик лёгкий",
            "Пальто классическое",
            "Плащ",
            "Джинсы прямые",
            "Брюки чинос",
            "Юбка миди",
            "Шорты",
        )
    ]
    + [
        ("Обувь", x)
        for x in ("Кроссовки", "Ботинки кожаные", "Туфли классические", "Лоферы")
    ]
    + [
        ("Аксессуары", x)
        for x in ("Ремень кожаный", "Шарф шерстяной", "Шапка", "Перчатки")
    ]
)


def random_doc_id(k: int = 10) -> str:
    return "".join(RNG.choices(string.ascii_uppercase + string.digits, k=k))


def sample_row():
    category, item = RNG.choice(CATALOG)
    amount = RNG.randint(1, 3)
    price = round(RNG.uniform(200, 5000), 2)
    max_disc = round(amount * price * 0.35, 2)
    discount = round(RNG.uniform(0, max_disc), 2) if RNG.random() < 0.5 else 0.0
    return category, item, amount, price, discount


def write_file(path: Path, n_rows: int) -> None:
    produced = 0
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["doc_id", "item", "category", "amount", "price", "discount"])
        while produced < n_rows:
            did = random_doc_id()
            for _ in range(RNG.randint(1, 4)):
                if produced >= n_rows:
                    break
                category, item, amount, price, discount = sample_row()
                w.writerow([did, item, category, amount, price, discount])
                produced += 1


def main():
    if date.today().weekday() == 6:
        logger.info("Воскресенье — генерация пропущена.")
        return

    day_dir = DATA_DIR / date.today().strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Старт генерации → {day_dir}")

    for shop in range(1, N_SHOPS + 1):
        n_cash = RNG.randint(MIN_CASH, MAX_CASH)
        for cash in range(1, n_cash + 1):
            out = day_dir / f"{shop}_{cash}.csv"
            write_file(out, ROWS_PER_CASH)
            logger.info(f"Сгенерирован {out}")

    logger.info("Генерация завершена.")


if __name__ == "__main__":
    main()
