# code/logger.py
from __future__ import annotations
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv
from file_path import get_env

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

def get_logger(name: str | None = None) -> logging.Logger:
    log_level = get_env("LOG_LEVEL", "INFO").upper()
    log_dir = get_env("LOG_DIR", "../logs")
    log_file = get_env("LOG_FILE", "swaps.log")
    max_bytes = int(get_env("LOG_MAX_BYTES", "1000000"))
    backup_count = int(get_env("LOG_BACKUP_COUNT", "5"))

    base = Path(__file__).resolve().parents[1]
    if log_dir.startswith("../"):
        log_dir_path = (base / "code" / log_dir).resolve()
    else:
        log_dir_path = (base / log_dir).resolve()
    log_dir_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name if name else "app")
    logger.setLevel(getattr(logging, log_level, logging.INFO))

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
