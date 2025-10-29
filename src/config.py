from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

PG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": int(os.getenv("PGPORT", "5432")),
    "dbname": os.getenv("PGDATABASE", "retail"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "postgres"),
}

DATA_DIR = Path(os.getenv("DATA_DIR", ROOT / "data")).resolve()
LOG_DIR = Path(os.getenv("LOG_DIR", ROOT / "logs")).resolve()

N_SHOPS = int(os.getenv("N_SHOPS", "5"))
MIN_CASH = int(os.getenv("MIN_CASH_PER_SHOP", "2"))
MAX_CASH = int(os.getenv("MAX_CASH_PER_SHOP", "5"))
ROWS_PER_CASH = int(os.getenv("ROWS_PER_CASH", "300"))

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
