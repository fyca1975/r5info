# code/main.py
from __future__ import annotations
import logging
from logger import get_logger
from file_path import load_paths
from pkg.procesar_swaps import procesar_swaps
from pkg.actualizar_informe import actualizar_informe

def main():
    log = get_logger(__name__)
    rutas = load_paths()
    log.info("Iniciando proceso R5 con rutas: %s", rutas)

    try:
        flujos_csv, fecha = procesar_swaps(rutas["INPUT_DIR"], rutas["OUTPUT_DIR"])
        if not flujos_csv:
            log.error("No se generó el CSV de flujos procesados. Abortando.")
            return

        informe = actualizar_informe(rutas["INPUT_DIR"], rutas["OUTPUT_DIR"], flujos_csv, fecha)
        if informe:
            log.info("Proceso completado. Informe: %s", informe)
        else:
            log.warning("Proceso completado solo con flujos. No se generó informe R5.")

    except Exception:
        logging.exception("Error no controlado en main()")
        raise

if __name__ == "__main__":
    main()
