# Scraping de Ofertas de Trabajo en ANE

Este proyecto permite hacer scraping de las ofertas de trabajo publicadas en [www.ane.cr](https://www.ane.cr/Puesto) y proporciona una CLI (Interfaz de Línea de Comandos) para filtrar y consultar las ofertas guardadas en formato JSON. También puedes exportar los resultados a archivos CSV.

## Requisitos

Antes de comenzar, asegúrate de tener las siguientes dependencias instaladas:

```bash
pip install requests beautifulsoup4 typer tabulate
```

## Funcionalidades

### Scraping de Ofertas de Trabajo

Puedes scrapear las ofertas de trabajo desde el sitio web **www.ane.cr** especificando cuántas páginas quieres scrapear y el archivo donde quieres guardar los datos.

### Búsqueda Avanzada en Ofertas

Una vez que hayas guardado las ofertas en un archivo JSON, puedes buscar entre ellas aplicando filtros como:

- Título (por ejemplo, "Ingeniero")
- Ubicación (por ejemplo, "San José")
- Fecha de publicación
- Número de vacantes (filtrado por mínimo o máximo)

### Exportación de Resultados

Los resultados de las búsquedas pueden ser exportados a formato **JSON** o **CSV** para un análisis posterior.

---

## Uso

### 1. Scraping de Ofertas de Trabajo

Para hacer scraping de las ofertas de trabajo y guardarlas en un archivo JSON, usa el siguiente comando:

```bash
python main.py scrape --pages <NUMERO_DE_PAGINAS> --output <ARCHIVO_DE_SALIDA>.json
```

#### Parámetros:

- `--pages`: Número de páginas a scrapear (por defecto es 1).
- `--output`: Nombre del archivo de salida (por defecto es `ofertas_trabajo.json`).

#### Ejemplo:

```bash
python main.py scrape --pages 5 --output ofertas_trabajo.json
```

Este comando scrappea las primeras 5 páginas de ofertas de trabajo y las guarda en el archivo `ofertas_trabajo.json`.

---

### 2. Búsqueda de Ofertas de Trabajo

Una vez que hayas scrapear las ofertas, puedes buscar en el archivo JSON utilizando filtros avanzados.

#### Comando de búsqueda:

```bash
python main.py search <ARCHIVO_JSON> --position <POSICION> --location <UBICACION> --min_vacancies <VACANTES_MIN> --max_vacancies <VACANTES_MAX> --published_date <FECHA> --save <ARCHIVO_DE_SALIDA> --output_format <FORMATO>
```

#### Parámetros:

- `<ARCHIVO_JSON>`: Ruta al archivo JSON con las ofertas de trabajo.
- `--position`: Filtrar por posición o título del trabajo (opcional).
- `--location`: Filtrar por ubicación (opcional).
- `--min-vacancies`: Filtrar por número mínimo de vacantes (opcional).
- `--max-vacancies`: Filtrar por número máximo de vacantes (opcional).
- `--published-date`: Filtrar por fecha de publicación (opcional).
- `--save`: Guardar los resultados filtrados en un nuevo archivo.
- `--output-format`: El formato de salida, puede ser `json` o `csv` (opcional, por defecto `json`).

#### Ejemplo 1: Buscar ofertas de "Ingeniero" en "San José" con al menos 2 vacantes

```bash
python main.py search ofertas_trabajo.json --position "Ingeniero" --location "San José" --min-vacancies 2
```

#### Ejemplo 2: Filtrar por "Ingeniero" y guardar los resultados en CSV

```bash
python main.py search ofertas_trabajo.json --position "Ingeniero" --output-format csv --save ingenieros.csv
```

#### Ejemplo 3: Buscar ofertas de trabajo de "Desarrollador" publicadas en noviembre de 2024

```bash
python main.py search ofertas_trabajo.json --position "Desarrollador" --published-date "noviembre" --save desarrolladores_nov_2024.json
```

---

## Ejemplo de Salida

### Visualización de los Resultados

Los resultados de las búsquedas se mostrarán en una tabla de forma legible y organizada, gracias al uso de la librería `tabulate`. Por ejemplo:

```text
+-------------------------+--------------------+-----------------+-----------+----------------------+
| Título                  | Empresa            | Ubicación       | Vacantes | Fecha de Publicación |
+-------------------------+--------------------+-----------------+-----------+----------------------+
| Ingeniero de Sistemas   | Empresa X       | San José, Alajuela | 3       | Sábado, 16 de Noviembre de 2024 |
| Analista de Datos       | ABC Corporation    | Heredia, Santa Bárbara | 2    | Jueves, 14 de Noviembre de 2024 |
+-------------------------+--------------------+-----------------+-----------+----------------------+
```

### Exportación a CSV

Si optas por exportar a CSV, los resultados se guardarán en el archivo especificado en el formato siguiente:

```csv
Título,Empresa,Ubicación,Vacantes,Fecha de Publicación
Ingeniero de Sistemas,Empresa X,"San José, Alajuela",3,"Sábado, 16 de Noviembre de 2024"
Analista de Datos,ABC Corporation,"Heredia, Santa Bárbara",2,"Jueves, 14 de Noviembre de 2024"
```

---

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un **pull request** o abre un **issue** si encuentras algún error o tienes alguna sugerencia de mejora.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
