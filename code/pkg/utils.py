# code/pkg/utils.py
from __future__ import annotations
from pathlib import Path
import os
from dotenv import load_dotenv

# Carga central del .env
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)  # idempotente

def cargar_env() -> dict:
    # Compat/ayuda: retorna las rutas crudas del .env (normalización la hace file_path.load_paths())
    return {
        "INPUT_DIR": os.getenv("INPUT_DIR", "../input"),
        "OUTPUT_DIR": os.getenv("OUTPUT_DIR", "../output"),
        "LOG_DIR": os.getenv("LOG_DIR", "../logs"),
    }

def get_config(key: str, default=None):
    return os.getenv(key, default)

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
