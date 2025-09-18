from __future__ import annotations
from pathlib import Path
import pandas as pd
from pkg.utils import safe_read_csv, safe_to_csv
from logger import get_logger

log = get_logger(__name__)

def _buscar_informe_base(input_dir: str) -> Path | None:
    p = Path(input_dir)
    candidatos = []
    candidatos += list(p.glob("**/informe*.csv"))
    candidatos += list(p.glob("**/*r5*.csv"))
    candidatos = sorted(candidatos, key=lambda x: x.stat().st_mtime, reverse=True)
    return candidatos[0] if candidatos else None

def actualizar_informe(input_dir: str, output_dir: str, flujos_csv: str, fecha: tuple[str,str,str] | None) -> str | None:
    log.info("actualizar_informe iniciado")

    # Normaliza flujos_csv a ABSOLUTO y verifica existencia
    fpath = Path(flujos_csv)
    if not fpath.is_absolute():
        fpath = (Path(output_dir) / fpath.name).resolve()
    if not fpath.exists():
        suf = "".join(fecha) if fecha else None
        if suf:
            cand = (Path(output_dir) / f"flujos_swaps_procesados_{suf}.csv").resolve()
            if cand.exists():
                fpath = cand
            else:
                log.error("No existe flujos procesados: %s ni %s", flujos_csv, cand)
                return None
        else:
            log.error("No existe flujos procesados: %s", fpath)
            return None

    # Cargar flujos procesados
    try:
        df_flujos = safe_read_csv(fpath)
    except Exception:
        log.exception("No se pudo leer flujos procesados: %s", fpath)
        return None

    # Informe base (si hay)
    base = _buscar_informe_base(input_dir)
    if base:
        try:
            df_base = safe_read_csv(base)
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
        log.warning("No se encontró informe base; se creará a partir de flujos.")
        df_out = df_flujos.copy()

    suf = "".join(fecha) if fecha else "00000000"
    out = (Path(output_dir) / f"informe_r5_actualizado_{suf}.csv").resolve()
    safe_to_csv(df_out, out)
    log.info("Informe R5 actualizado: %s", out)
    return str(out)
