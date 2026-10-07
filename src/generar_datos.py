"""Genera el archivo CSV de estudiantes usado en los benchmarks.

El conjunto se escribe por streaming, sin cargar todos los registros en
memoria.
"""

import argparse
import csv
import random
from time import perf_counter

from config import CSV_FILE, DATA_DIR, CITIES, PROGRAMS


def crear_registro(i: int, rng: random.Random) -> tuple:
    """Construye un registro de estudiante con valores aleatorios reproducibles.

    Args:
        i: Número consecutivo que identifica al estudiante.
        rng: Generador aleatorio con semilla fija.

    Returns:
        tuple: Los nueve campos del registro en el orden del CSV.
    """
    return (
        i,
        f"Estudiante {i:07d}",
        f"estudiante{i:07d}@universidad.edu.co",
        rng.choice(CITIES),
        rng.choice(PROGRAMS),
        rng.randint(1, 10),
        round(rng.uniform(2.0, 5.0), 2),
        rng.randint(0, 180),
        "ACTIVO" if rng.random() < 0.86 else "INACTIVO",
    )


def generar(rows: int, seed: int = 2026) -> None:
    """Escribe el CSV completo con la cantidad de registros indicada.

    Args:
        rows: Cantidad de registros a generar.
        seed: Semilla del generador aleatorio para reproducibilidad.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    inicio = perf_counter()
    with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "nombre",
                "correo",
                "ciudad",
                "programa",
                "semestre",
                "promedio",
                "creditos",
                "estado",
            ]
        )

        for i in range(1, rows + 1):
            writer.writerow(crear_registro(i, rng))

    tiempo = perf_counter() - inicio
    mb = CSV_FILE.stat().st_size / (1024 * 1024)

    print(f"Registros generados: {rows:,}")
    print(f"Archivo: {CSV_FILE}")
    print(f"Tamano: {mb:.2f} MB")
    print(f"Tiempo de generacion: {tiempo:.3f} s")


def main() -> None:
    """Lee los argumentos de la línea de comandos y genera el CSV."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=5_000_000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    if args.rows < 1:
        raise ValueError("--rows debe ser mayor que cero")

    generar(args.rows, args.seed)


if __name__ == "__main__":
    main()
