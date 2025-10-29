from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
import sys


def setup_logger(log_dir: Path, basename: str) -> logging.Logger:
    """Логгер с ротацией: пишет в файл и в консоль."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{basename}.log"

    logger = logging.getLogger(basename)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        fmt = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # файл с ротацией (7 дней)
        fh = TimedRotatingFileHandler(
            filename=str(log_path),
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
            utc=True,
        )
        fh.setFormatter(fmt)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

        # КОНСОЛЬ ---
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)

    return logger
