# Economía Laboral (UCEMA)

Sitio del curso con las slides y los trabajos prácticos. Está hecho con Quarto y se publica en GitHub Pages con GitHub Actions.

## Cómo agregar una slide o un TP

1. Sumá una entrada en `materiales.yml`, en el lugar donde querés que aparezca.

   ```yaml
   - tipo: slides          # o tp
     bloque: Nombre del bloque
     numero: Clase 15
     titulo: Título de la clase
     archivo: archivos/slides/clase-15.pdf
     fuente: Clase 15 - Nombre/Clase15.pdf
   ```

   `fuente` es la ruta del original dentro de la carpeta `LABOR`. Para una clase que todavía no tiene material, dejá la entrada sin `archivo` ni `fuente`. El sitio muestra "Próximamente". Si la clase no va a tener material, agregá `nota: Sin slides`.

2. Copiá el archivo y controlá el listado.

   ```bash
   python scripts/sincronizar.py
   python scripts/verificar.py
   ```

3. Hacé commit y push a `main`. El sitio se actualiza solo en un par de minutos.

Los scripts necesitan PyYAML (`pip install pyyaml`). Para ver el sitio en tu máquina, corré `quarto preview`.

## Qué no se publica

El repo es público y su historial también. Solo entran archivos listados en `materiales.yml`. Nunca subas soluciones, exámenes, libros, papers ni datos. `verificar.py` rechaza nombres como `sol`, `rtas` o `examen` y cualquier archivo sin listar, pero no lee el contenido de los PDFs, así que revisá cada archivo antes de agregarlo.

## Cómo activar GitHub Pages

1. En el repo, entrá a **Settings > Pages**.
2. En **Build and deployment > Source**, elegí **GitHub Actions**.
3. Hacé un push a `main`, o corré el workflow **Publicar sitio** desde la pestaña **Actions**.

La dirección del sitio aparece en esa misma página de Settings.
