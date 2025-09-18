from __future__ import annotations
from pathlib import Path
from typing import Dict
import os
from dotenv import load_dotenv
from logger import get_logger

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

log = get_logger(__name__)

def _abs_from_code_root(path_str: str) -> Path:
    base = Path(__file__).resolve().parents[1]
    if path_str.startswith("../"):
        return (base / "code" / path_str).resolve()
    return (base / path_str).resolve() if not Path(path_str).is_absolute() else Path(path_str).resolve()

def ensure_dir(path: Path, key: str, create: bool) -> Path:
    if create:
        path.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        raise FileNotFoundError(f"La ruta para {key} no existe: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"La ruta para {key} no es un directorio: {path}")
    return path

def load_paths() -> Dict[str, str]:
    input_dir = get_env("INPUT_DIR", "../input")
    output_dir = get_env("OUTPUT_DIR", "../output")
    log_dir = get_env("LOG_DIR", "../logs")

    p_input = ensure_dir(_abs_from_code_root(input_dir), "INPUT_DIR", create=False)
    p_output = ensure_dir(_abs_from_code_root(output_dir), "OUTPUT_DIR", create=True)
    p_log = ensure_dir(_abs_from_code_root(log_dir), "LOG_DIR", create=True)

    rutas = {
        "INPUT_DIR": str(p_input),
        "OUTPUT_DIR": str(p_output),
        "LOG_DIR": str(p_log),
    }
    log.info(f"Rutas normalizadas: {rutas}")
    return rutas
