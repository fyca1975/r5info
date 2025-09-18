from file_path import load_paths
from logger import get_logger
import os
import logging
from pkg.procesar_swaps import procesar_swaps
from pkg.actualizar_informe import actualizar_informe
from pkg.utils import cargar_env, setup_logging

def main():
    try:
            log = get_logger(__name__)
            rutas = load_paths()
            log.info('Inicializando proceso con rutas: %s', rutas)
            rutas = cargar_env()
            setup_logging(rutas['LOG_DIR'])
            logging.info("----- INICIO DEL PROCESO DE SWAPS -----")

            # Proceso de modificación de flujos
            flujos_csv_modificado, fecha = procesar_swaps(
                rutas['INPUT_DIR'],
                rutas['OUTPUT_DIR']
            )

            # Si existe archivo de informe R5, continúa el flujo
            if flujos_csv_modificado and fecha:
                informe_actualizado = actualizar_informe(
                    rutas['INPUT_DIR'],
                    rutas['OUTPUT_DIR'],
                    flujos_csv_modificado,
                    fecha
                )
                if informe_actualizado:
                    logging.info("Proceso completado y archivos generados exitosamente.")
                else:
                    logging.warning("Archivo de informe R5 no encontrado. Proceso finalizado solo con swaps.")
            else:
                logging.error("Error al procesar el archivo de flujos de swaps.")

            logging.info("----- FIN DEL PROCESO -----")

        if __name__ == "__main__":
            main()

    except Exception:
        logging.exception('Error no controlado en main()')
        raise
