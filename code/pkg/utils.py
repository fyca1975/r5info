from __future__ import annotations

from file_path import load_paths
from pathlib import Path
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

rutas = load_paths()

# Carga central del .env (idempotente)
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"  # /code/.env
load_dotenv(ENV_PATH)

def cargar_env() -> dict:
    """Devuelve las rutas y variables base desde .env (con valores por defecto).
    Normaliza las rutas relativas ../ respecto a /code en file_path.load_paths()."""
    rutas = {
        "INPUT_DIR": rutas['INPUT_DIR'],
        "OUTPUT_DIR": rutas['OUTPUT_DIR'],
        "LOG_DIR": rutas['LOG_DIR'],
    }
    # No normalizamos aquí; lo hace file_path.load_paths()
    return rutas

def setup_logging(log_dir: str | None = None):
    """Compat: configura logging usando variables del .env.
    Si no se pasa log_dir, usa LOG_DIR del .env.
    """
    from logger import get_logger  # evita dependencia circular
    # Instancia el logger raíz para configurar handlers según .env
    root_logger = get_logger()  # aplica rotación y consola
    if log_dir:
        # Asegura que exista (por si se invoca con ruta específica)
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    return root_logger

def get_config(key: str, default=None):
    return get_env(key, default)


# === Helpers de IO CSV robustos ===
import pandas as _pd

def safe_read_csv(path, **kwargs):
    """Intenta leer CSV con utf-8 y hace fallback a latin1 si falla."""
    encs = [kwargs.pop("encoding", None), "utf-8", "latin1"]
    tried = []
    for enc in encs:
        if not enc:
            continue
        try:
            return _pd.read_csv(path, encoding=enc, **kwargs)
        except Exception as e:
            tried.append((enc, str(e)))
    # último intento sin encoding explícito
    try:
        return _pd.read_csv(path, **kwargs)
    except Exception as e:
        raise RuntimeError(f"No se pudo leer CSV {path}. Intentos: {tried}. Error final: {e}")

def safe_to_csv(df, path, **kwargs):
    """Escribe CSV garantizando carpeta y usando utf-8 por defecto."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if "encoding" not in kwargs:
        kwargs["encoding"] = "utf-8"
    df.to_csv(p, index=False, **kwargs)
