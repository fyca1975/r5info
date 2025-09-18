# code/pkg/actualizar_informe.py
from __future__ import annotations
import logging
from pathlib import Path
import pandas as pd
from pkg.utils import safe_read_csv, safe_to_csv
from logger import get_logger

log = get_logger(__name__)

def _buscar_informe_base(input_dir: str) -> Path | None:
    p = Path(input_dir)
    # Busca un informe CSV base (por nombre); si no hay, devuelve None
    candidatos = list(p.glob("**/*informe*.csv")) + list(p.glob("**/*r5*.csv"))
    return candidatos[0] if candidatos else None

def actualizar_informe(input_dir: str, output_dir: str, flujos_csv: str, fecha: tuple[str,str,str] | None) -> str | None:
    """Actualiza/crea informe R5 a partir de los flujos procesados.
    Si hay informe base en input, lo combina por columnas comunes y escribe salida.
    Si no hay, crea un informe de ejemplo basado en flujos.
    Devuelve la ruta del informe generado.
    """
    log.info("actualizar_informe iniciado")
    try:
        df_flujos = safe_read_csv(flujos_csv)
    except Exception:
        log.exception("No se pudo leer flujos procesados: %s", flujos_csv)
        return None

    base = _buscar_informe_base(input_dir)
    if base:
        try:
            df_base = safe_read_csv(base)
            # Combina por columnas comunes (intersección), si existen
            comunes = [c for c in df_base.columns if c in df_flujos.columns]
            if comunes:
                df_out = pd.merge(df_base, df_flujos, on=comunes, how="outer")
            else:
                df_out = pd.concat([df_base, df_flujos], ignore_index=True)
            log.info("Informe base encontrado: %s", base)
        except Exception:
            log.exception("Fallo leyendo informe base: %s", base)
            df_out = df_flujos.copy()
    else:
        log.warning("No se encontró informe base, se creará uno a partir de flujos.")
        df_out = df_flujos.copy()

    suf = f"{fecha[0]}{fecha[1]}{fecha[2]}" if fecha else "00000000"
    out = Path(output_dir) / f"informe_r5_actualizado_{suf}.csv"
    safe_to_csv(df_out, out)
    log.info("Informe R5 actualizado: %s", out)
    return str(out)
