# code/pkg/procesar_swaps.py
from __future__ import annotations
import logging
from pathlib import Path
import re
import pandas as pd
from pkg.utils import safe_read_csv, safe_to_csv
from logger import get_logger

log = get_logger(__name__)

def extraer_fecha(nombre: str):
    """Devuelve (yyyy, mm, dd) a partir del nombre de archivo esperado."""
    base = Path(nombre).name
    if "flujos_swap_gbo" in base:
        # ...flujos_swap_gbo_YYYYMMDD.csv
        fecha = base.split("_")[-1].split(".")[0]
        return fecha[:4], fecha[4:6], fecha[6:8]
    if "COL_ESTIM_FLOWS" in base:
        # ...COL_ESTIM_FLOWS_DDMMYYYY.dat
        fecha = base.split("_")[-1].split(".")[0]
        return fecha[4:8], fecha[2:4], fecha[0:2]
    # genérico: busca 8 dígitos consecutivos
    m = re.search(r"(\d{8})", base)
    if m:
        fecha = m.group(1)
        return fecha[:4], fecha[4:6], fecha[6:8]
    return None

def _encontrar_archivo_input(input_dir: str) -> Path | None:
    p = Path(input_dir)
    # prioridad csv gbo, luego dat estim, luego primer csv
    candidatos = list(p.glob("**/flujos_swap_gbo_*.csv")) + list(p.glob("**/COL_ESTIM_FLOWS_*.dat")) + list(p.glob("**/*.csv"))
    return candidatos[0] if candidatos else None

def procesar_swaps(input_dir: str, output_dir: str) -> tuple[str | None, tuple[str,str,str] | None]:
    """Lee el archivo principal de swaps, hace normalizaciones simples y guarda un CSV procesado.
    Retorna (ruta_csv_generado, (yyyy, mm, dd)).
    """
    log.info("procesar_swaps iniciado")
    src = _encontrar_archivo_input(input_dir)
    if not src:
        log.error("No se encontró archivo de input en %s", input_dir)
        return None, None

    fecha = extraer_fecha(src.name)
    suf = f"{fecha[0]}{fecha[1]}{fecha[2]}" if fecha else "00000000"
    dst = Path(output_dir) / f"flujos_swaps_procesados_{suf}.csv"

    try:
        if src.suffix.lower() == ".dat":
            df = safe_read_csv(src, sep=r"[,;|\t]", engine="python")
        else:
            df = safe_read_csv(src)

        # Limpiezas leves
        df.columns = [str(c).strip() for c in df.columns]
        # Ejemplo de normalización: agrega columnas de fecha si no existen
        if fecha and not set(["anio","mes","dia"]).issubset(df.columns):
            df["anio"], df["mes"], df["dia"] = fecha

        safe_to_csv(df, dst)
        log.info("Archivo procesado guardado en %s", dst)
        return str(Path(dst).resolve()), fecha
    except Exception:
        log.exception("Fallo procesando archivo %s", src)
        return None, fecha
