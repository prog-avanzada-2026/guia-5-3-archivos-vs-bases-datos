"""Compara las consultas CSV y SQLite y guarda los resultados en JSON."""

import json
import statistics
from time import perf_counter

import csv_queries
import sqlite_queries
from config import CSV_FILE, DB_FILE, RESULTS_DIR


REPETICIONES = 3


def medir(funcion, *args):
    """Ejecuta una consulta varias veces y devuelve sus tiempos.

    Args:
        funcion: Consulta que se desea medir.
        *args: Argumentos de la consulta.

    Returns:
        tuple: Resultado de la última ejecución y lista de tiempos.
    """
    tiempos = []
    resultado = None
    for _ in range(REPETICIONES):
        inicio = perf_counter()
        resultado = funcion(*args)
        tiempos.append(perf_counter() - inicio)
    return resultado, tiempos


def comparar(nombre, csv_func, sqlite_func, *args):
    """Mide una consulta en CSV y SQLite y reporta la comparación.

    Args:
        nombre: Nombre de la consulta que aparece en el reporte.
        csv_func: Versión de la consulta sobre CSV.
        sqlite_func: Versión de la consulta sobre SQLite.
        *args: Argumentos comunes a ambas consultas.

    Returns:
        dict: Medianas de tiempo y factor CSV/SQLite.
    """
    _, csv_tiempos = medir(csv_func, *args)
    _, sql_tiempos = medir(sqlite_func, *args)

    csv_med = statistics.median(csv_tiempos)
    sql_med = statistics.median(sql_tiempos)
    factor = csv_med / sql_med if sql_med > 0 else float("inf")

    print(f"\n=== {nombre} ===")
    print(f"CSV mediana:    {csv_med:.6f} s")
    print(f"SQLite mediana: {sql_med:.6f} s")
    print(f"CSV / SQLite:   {factor:.2f}x")

    return {
        "consulta": nombre,
        "csv_mediana_s": csv_med,
        "sqlite_mediana_s": sql_med,
        "factor_csv_sobre_sqlite": factor,
    }


def main():
    """Ejecuta las tres consultas del taller y guarda benchmark.json."""
    if not CSV_FILE.exists() or not DB_FILE.exists():
        raise FileNotFoundError(
            "Debe generar el CSV y preparar SQLite antes del benchmark."
        )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    resultados = [
        comparar(
            "Busqueda exacta por correo",
            csv_queries.buscar_por_correo,
            sqlite_queries.buscar_por_correo,
            "estudiante0499999@universidad.edu.co",
        ),
        comparar(
            "Filtro ciudad + promedio",
            csv_queries.filtrar_ciudad_promedio,
            sqlite_queries.filtrar_ciudad_promedio,
            "Bogota",
            4.5,
        ),
        comparar(
            "Promedio agrupado por programa",
            csv_queries.promedio_por_programa,
            sqlite_queries.promedio_por_programa,
        ),
    ]

    print("\n=== PLAN DE CONSULTA SQLITE ===")
    for fila in sqlite_queries.plan_busqueda_correo():
        print(fila)

    salida = RESULTS_DIR / "benchmark.json"
    salida.write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nResultados guardados en: {salida}")


if __name__ == "__main__":
    main()
