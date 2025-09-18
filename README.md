# Proyecto Swaps – R5 (Refactor .env + logger + file_path)

Este proyecto procesa archivos de *input* y genera resultados en *output* para el flujo R5.
El refactor alinea la configuración a un único `.env`, centraliza el *logging* y unifica la validación de rutas.

## Estructura
```
proyecto_swaps_corr_r5/
├─ code/
│  ├─ main.py
│  ├─ logger.py
│  ├─ file_path.py
│  ├─ .env.example  → copiar como .env y ajustar valores
│  └─ pkg/
│     ├─ utils.py
│     └─ __init__.py
├─ input/           (proveído por el usuario)
├─ output/          (se crea si no existe)
├─ logs/            (se crea si no existe)
├─ tests/
│  └─ test_paths.py
├─ requirements.txt
└─ pyproject.toml
```

## Requisitos
- Python 3.10+
- Dependencias: `python-dotenv`, `pandas`, `pytest` (dev)

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración (.env)
Copia `code/.env.example` a `code/.env` y ajusta según tu entorno:

```env
# ==== RUTAS ====
INPUT_DIR=../input
OUTPUT_DIR=../output
LOG_DIR=../logs

# ==== LOGGING ====
LOG_LEVEL=INFO
LOG_FILE=swaps.log
LOG_MAX_BYTES=1000000
LOG_BACKUP_COUNT=5

# ==== APP ====
APP_ENV=local
DATE_FMT=%Y-%m-%d
```

> Las rutas relativas `../` se interpretan respecto a la carpeta `code/` y se convierten a **absolutas** por `file_path.py`.

## Ejecución
Desde la **raíz** del proyecto:
```bash
python -m code.main
```
O desde `code/`:
```bash
python main.py
```

## Pruebas
```bash
pytest -q
```

## Logging
- Configurado en `code/logger.py` leyendo variables del `.env`.
- Escribe a `logs/` con rotación (`RotatingFileHandler`) y también a consola.

## Paquetización (opcional)
Con `pyproject.toml`, puedes instalar el proyecto en editable:
```bash
pip install -e .
```
Luego puedes importar `code` en otros scripts:
```python
from code.file_path import load_paths
from code.logger import get_logger
```

## Solución de problemas
- **No encuentra rutas**: verifica `code/.env` y que `input/` exista. `output/` y `logs/` se crean automáticamente.
- **Sin logs**: valida permisos de escritura en `logs/` y que `LOG_LEVEL` no esté en `ERROR`.
- **Encoding en CSV**: si hay errores, especifica `encoding='latin1'` o detecta con una librería (p.ej. `charset-normalizer`).

## Licencia
Privado / Interno.
