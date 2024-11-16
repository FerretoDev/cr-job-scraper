import csv
import json
import re
from datetime import datetime
from typing import Optional

import requests
import tabulate
import typer
import urllib3
from bs4 import BeautifulSoup

# Inicializar Typer
app = typer.Typer()

# Deshabilitar advertencias de HTTPS no verificado (solo para pruebas)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL base para scraping
BASE_URL = "https://www.ane.cr/Puesto"


def fetch_jobs(page: int = 1) -> list:
    """Función para obtener ofertas de trabajo de una página específica."""
    url = f"{BASE_URL}?Pagina={page}"
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    job_listings = soup.find_all("div", class_="job-listing")
    jobs = []
    for job in job_listings:
        company = job.find("h4", class_="job-listing-company").text.strip()
        title = job.find("h3", class_="job-listing-title").text.strip()
        descriptions = job.find_all("h4", class_="job-listing-description")
        job_description = (
            descriptions[0].text.strip()
            if len(descriptions) > 0
            else "Descripción no disponible"
        )
        job_vacancies = (
            descriptions[1].text.strip()
            if len(descriptions) > 1
            else "Vacantes no especificadas"
        )
        published_date = (
            job.find("small", class_="job-listing-description").text.strip()
            if job.find("small", class_="job-listing-description")
            else "Fecha no disponible"
        )
        location_list = job.find("ul")
        locations = (
            ", ".join([li.text.strip() for li in location_list.find_all("li")])
            if location_list
            else "Ubicación no especificada"
        )
        jobs.append(
            {
                "company": company,
                "title": title,
                "description": job_description,
                "vacancies": job_vacancies,
                "published_date": published_date,
                "locations": locations,
            }
        )
    return jobs


def format_date(date_str: str):
    """Función para convertir la fecha a formato datetime"""
    try:
        return datetime.strptime(date_str, "%A, %d de %B de %Y")
    except ValueError:
        return None


@app.command()
def scrape(
    pages: int = typer.Option(1, help="Número de páginas a scrapear."),
    output: str = typer.Option("ofertas_trabajo.json", help="Archivo JSON de salida."),
):
    """
    Scrapea ofertas de trabajo desde www.ane.cr y guarda los datos en un archivo JSON.
    """
    all_jobs = []
    for page in range(1, pages + 1):
        typer.echo(f"Scrapeando página {page}...")
        try:
            jobs = fetch_jobs(page)
            if not jobs:
                typer.echo(f"No se encontraron más ofertas en la página {page}.")
                break
            all_jobs.extend(jobs)
        except Exception as e:
            typer.echo(f"Error en la página {page}: {e}")
            break

    # Guardar resultados en un archivo JSON
    with open(output, "w", encoding="utf-8") as json_file:
        json.dump(all_jobs, json_file, ensure_ascii=False, indent=4)

    typer.echo(f"Se han guardado {len(all_jobs)} ofertas de trabajo en '{output}'.")


@app.command()
def search(
    file: str = typer.Argument(..., help="Archivo JSON con las ofertas de trabajo."),
    position: Optional[str] = typer.Option(None, help="Filtrar por posición/título."),
    location: Optional[str] = typer.Option(None, help="Filtrar por ubicación."),
    published_date: Optional[str] = typer.Option(
        None, help="Filtrar por fecha de publicación (formato libre)."
    ),
    min_vacancies: Optional[int] = typer.Option(
        None, help="Filtrar por número mínimo de vacantes."
    ),
    max_vacancies: Optional[int] = typer.Option(
        None, help="Filtrar por número máximo de vacantes."
    ),
    save: Optional[str] = typer.Option(
        None, help="Archivo JSON donde guardar los resultados."
    ),
    output_format: Optional[str] = typer.Option(
        "json", help="Formato de salida: json o csv."
    ),
):
    """
    Busca ofertas de trabajo en un archivo JSON creado previamente.
    Permite filtrar por posición, ubicación, fecha de publicación y número de vacantes.
    """
    try:
        # Leer el archivo JSON
        with open(file, "r", encoding="utf-8") as json_file:
            jobs = json.load(json_file)

        if not jobs:
            typer.echo("El archivo JSON no contiene ofertas de trabajo.")
            raise typer.Exit()

        # Aplicar filtros
        filtered_jobs = jobs
        if position:
            filtered_jobs = [
                job
                for job in filtered_jobs
                if re.search(position, job["title"], re.IGNORECASE)
            ]
        if location:
            filtered_jobs = [
                job
                for job in filtered_jobs
                if re.search(location, job["locations"], re.IGNORECASE)
            ]
        if published_date:
            filtered_jobs = [
                job
                for job in filtered_jobs
                if published_date.lower() in job["published_date"].lower()
            ]
        if min_vacancies:
            filtered_jobs = [
                job
                for job in filtered_jobs
                if int(job["vacancies"].split()[0]) >= min_vacancies
            ]
        if max_vacancies:
            filtered_jobs = [
                job
                for job in filtered_jobs
                if int(job["vacancies"].split()[0]) <= max_vacancies
            ]

        # Mostrar resultados
        if filtered_jobs:
            typer.echo(
                f"Se encontraron {len(filtered_jobs)} ofertas que coinciden con los filtros:"
            )
            # Usamos tabulate para hacer que la salida sea más amigable
            table = [
                [
                    job["title"],
                    job["company"],
                    job["locations"],
                    job["vacancies"],
                    job["published_date"],
                ]
                for job in filtered_jobs
            ]
            headers = [
                "Título",
                "Empresa",
                "Ubicación",
                "Vacantes",
                "Fecha de Publicación",
            ]
            print(tabulate.tabulate(table, headers, tablefmt="pretty"))
        else:
            typer.echo("No se encontraron ofertas que coincidan con los filtros.")

        # Guardar resultados en un archivo si se especifica
        if save:
            if output_format == "json":
                with open(save, "w", encoding="utf-8") as save_file:
                    json.dump(filtered_jobs, save_file, ensure_ascii=False, indent=4)
            elif output_format == "csv":
                with open(save, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [
                            "Título",
                            "Empresa",
                            "Ubicación",
                            "Vacantes",
                            "Fecha de Publicación",
                        ]
                    )
                    for job in filtered_jobs:
                        writer.writerow(
                            [
                                job["title"],
                                job["company"],
                                job["locations"],
                                job["vacancies"],
                                job["published_date"],
                            ]
                        )

            typer.echo(f"Resultados guardados en '{save}'.")

    except FileNotFoundError:
        typer.echo(f"El archivo '{file}' no existe.")
    except json.JSONDecodeError:
        typer.echo(
            "Error al leer el archivo JSON. Asegúrate de que tenga un formato válido."
        )
    except Exception as e:
        typer.echo(f"Error inesperado: {e}")


if __name__ == "__main__":
    app()
