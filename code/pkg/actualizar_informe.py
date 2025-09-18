import os
import pandas as pd
import logging

def actualizar_informe(input_dir, output_dir, flujos_csv, fecha):
    try:
        informe_pattern = f"Informe_R5_GBO_{fecha[2:8]}.csv"
        archivos = os.listdir(input_dir)
        informe_csv = [f for f in archivos if f == informe_pattern]
        if not informe_csv:
            logging.warning(f"No existe archivo de informe {informe_pattern}.")
            return False
        informe_csv = informe_csv[0]
        logging.info(f"Archivo de informe encontrado: {informe_csv}")

        flujo_path = os.path.join(output_dir, flujos_csv)
        informe_path = os.path.join(input_dir, informe_csv)

        if not os.path.exists(flujo_path):
            logging.error(f"No existe el archivo de flujos procesado: {flujo_path}.")
            return False
        if not os.path.exists(informe_path):
            logging.error(f"No existe el archivo de informe R5 de entrada: {informe_path}.")
            return False

        df_flujo = pd.read_csv(flujo_path, sep=';', encoding='latin1')
        df_informe = pd.read_csv(informe_path, sep=';', encoding='latin1')

        # FORZAR float ANTES DE MODIFICAR
        df_informe['cupon'] = df_informe['cupon'].astype(float)
        df_informe['cupon_1'] = df_informe['cupon_1'].astype(float)

        for i, row in df_informe.iterrows():
            codigo = str(row['codigo_operacion']).strip()
            registros = df_flujo[df_flujo['cod_emp'].astype(str).str.strip() == codigo]
            if not registros.empty:
                cupon = registros['der_vp'].fillna(0).sum() / 1_000_000
                cupon_1 = registros['obl_vp'].fillna(0).sum() / 1_000_000
                df_informe.at[i, 'cupon'] = round(cupon, 6)
                df_informe.at[i, 'cupon_1'] = round(cupon_1, 6)
            else:
                df_informe.at[i, 'cupon'] = 0
                df_informe.at[i, 'cupon_1'] = 0

        output_path = os.path.join(output_dir, informe_csv)
        df_informe.to_csv(output_path, sep=';', index=False, encoding='latin1')
        logging.info(f"Informe R5 actualizado guardado en {output_path}.")
        return True

    except Exception as e:
        logging.exception(f"Error actualizando informe R5: {e}")
        return False
