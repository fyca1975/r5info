# code/logger.py
from __future__ import annotations
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde /code/.env (si existe)
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)  # idempotente

def get_logger(name: str | None = None) -> logging.Logger:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_dir = os.getenv("LOG_DIR", "../logs")
    log_file = os.getenv("LOG_FILE", "swaps.log")
    max_bytes = int(os.getenv("LOG_MAX_BYTES", "1000000"))
    backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    project_root = Path(__file__).resolve().parents[1]
    if log_dir.startswith("../"):
        log_dir_path = (project_root / "code" / log_dir).resolve()
    else:
        log_dir_path = (project_root / log_dir).resolve()
    log_dir_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name or "app")
    logger.setLevel(getattr(logging, level, logging.INFO))

    # Evitar duplicación de handlers si ya fue configurado
    if logger.handlers:
        return logger

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh = RotatingFileHandler(log_dir_path / log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    fh.setFormatter(fmt)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
