#!/usr/bin/env python3
"""Controla que el sitio publique solo lo listado en materiales.yml.

Sin argumentos revisa el repo. Con --sitio también revisa que cada link del
sitio ya compilado en _site apunte a un archivo que existe.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

RAIZ = Path(__file__).resolve().parent.parent
EXTENSIONES = {".pdf", ".ipynb"}
PROHIBIDO = re.compile(
    r"(?<![a-z])(sol|soluci[oó]n|soluciones|rtas|respuestas?|examen|parcial)(?![a-z])",
    re.IGNORECASE,
)


def cargar_materiales() -> list:
    with open(RAIZ / "materiales.yml", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)


def nombre_prohibido(ruta: str) -> bool:
    return PROHIBIDO.search(ruta) is not None


def revisar_repo() -> list:
    errores = []
    materiales = cargar_materiales()
    listados = {item["archivo"] for item in materiales if "archivo" in item}

    for item in materiales:
        for campo in ("tipo", "bloque", "numero", "titulo"):
            if campo not in item:
                errores.append(f"Falta `{campo}` en: {item}")

    for ruta in sorted(listados):
        if nombre_prohibido(ruta):
            errores.append(f"Nombre prohibido: {ruta}")
        if not (RAIZ / ruta).is_file():
            errores.append(f"Listado pero no existe: {ruta}")

    for ruta in sorted((RAIZ / "archivos").rglob("*")):
        if not ruta.is_file():
            continue
        relativa = ruta.relative_to(RAIZ).as_posix()
        if relativa not in listados:
            errores.append(f"Archivo sin listar en materiales.yml: {relativa}")
        if ruta.suffix.lower() not in EXTENSIONES:
            errores.append(f"Extensión no permitida: {relativa}")
    return errores


class Enlaces(HTMLParser):
    def __init__(self):
        super().__init__()
        self.enlaces = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.enlaces.extend(valor for clave, valor in attrs if clave == "href" and valor)


def revisar_sitio() -> list:
    errores = []
    sitio = RAIZ / "_site"
    paginas = sorted(sitio.glob("*.html"))
    if not paginas:
        return ["No hay páginas en _site. Corré quarto render."]

    esperados = {item["archivo"] for item in cargar_materiales() if "archivo" in item}
    vistos = set()
    for pagina in paginas:
        parser = Enlaces()
        parser.feed(pagina.read_text(encoding="utf-8"))
        for enlace in parser.enlaces:
            url = urlparse(enlace)
            if url.scheme or enlace.startswith("#"):
                continue
            ruta = unquote(url.path)
            if not ruta:
                continue
            if not (sitio / ruta).is_file():
                errores.append(f"Link roto en {pagina.name}: {enlace}")
            vistos.add(ruta)

    for ruta in sorted(esperados - vistos):
        errores.append(f"Sin link en el sitio: {ruta}")
    return errores


def main() -> None:
    errores = revisar_repo()
    if "--sitio" in sys.argv:
        errores += revisar_sitio()
    for error in errores:
        print(f"ERROR: {error}")
    if errores:
        sys.exit(1)
    print("Todo en orden.")


if __name__ == "__main__":
    main()
