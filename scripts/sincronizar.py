#!/usr/bin/env python3
"""Copia al repo los materiales listados en materiales.yml.

Lee cada entrada con `fuente` y `archivo`, y copia el original desde la carpeta
LABOR. Nunca modifica los originales. Por defecto usa la carpeta LABOR de
OneDrive. Para usar otra, definí la variable de entorno LABOR_DIR.
"""

import os
import shutil
import sys
from pathlib import Path

from verificar import RAIZ, cargar_materiales, nombre_prohibido

CANDIDATAS = [
    Path("C:/Users/Juani/OneDrive/Documentos/LABOR"),
    Path("/mnt/c/Users/Juani/OneDrive/Documentos/LABOR"),
]


def carpeta_labor() -> Path:
    if os.environ.get("LABOR_DIR"):
        return Path(os.environ["LABOR_DIR"])
    for carpeta in CANDIDATAS:
        if carpeta.is_dir():
            return carpeta
    sys.exit("No encontré la carpeta LABOR. Definí LABOR_DIR.")


def main() -> None:
    labor = carpeta_labor()
    copiados = 0
    for item in cargar_materiales():
        if "archivo" not in item:
            continue
        if "fuente" not in item:
            sys.exit(f"Falta `fuente` en: {item['titulo']}")
        for ruta in (item["fuente"], item["archivo"]):
            if nombre_prohibido(ruta):
                sys.exit(f"Bloqueado, parece solución o examen: {ruta}")
        origen = labor / item["fuente"]
        if not origen.is_file():
            sys.exit(f"No existe el original: {origen}")
        destino = RAIZ / item["archivo"]
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origen, destino)
        copiados += 1
    print(f"Listo. {copiados} archivos copiados.")


if __name__ == "__main__":
    main()
