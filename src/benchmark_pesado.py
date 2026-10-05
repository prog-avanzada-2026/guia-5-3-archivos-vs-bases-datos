import argparse
import statistics
from time import perf_counter

import csv_queries
import sqlite_queries


def medir(funcion, *args, repeticiones=3):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = perf_counter()
        resultado = funcion(*args)
        tiempos.append(perf_counter() - inicio)
    return resultado, tiempos


def mediana(tiempos):
    return statistics.median(tiempos)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=20_000_000)
    parser.add_argument("--repeticiones", type=int, default=3)
    args = parser.parse_args()

    posiciones = [
        max(1, int(args.rows * 0.10)),
        max(1, int(args.rows * 0.50)),
        max(1, int(args.rows * 0.90)),
        args.rows,
    ]

    print("=== TALLER 5: ESCENARIO PESADO ===")
    print(f"Registros esperados: {args.rows:,}")
    print(f"Repeticiones por consulta: {args.repeticiones}")

    for posicion in posiciones:
        correo = f"estudiante{posicion:07d}@universidad.edu.co"

        _, t_csv = medir(
            csv_queries.buscar_por_correo,
            correo,
            repeticiones=args.repeticiones,
        )
        _, t_sql = medir(
            sqlite_queries.buscar_por_correo,
            correo,
            repeticiones=args.repeticiones,
        )

        csv_med = mediana(t_csv)
        sql_med = mediana(t_sql)
        factor = csv_med / sql_med if sql_med > 0 else float("inf")

        print(f"\nCorreo ubicado aproximadamente en {posicion:,}")
        print(f"CSV:    {csv_med:.6f} s")
        print(f"SQLite: {sql_med:.6f} s")
        print(f"Factor CSV/SQLite: {factor:.2f}x")

    print("\nPlan actual de SQLite:")
    for fila in sqlite_queries.plan_busqueda_correo():
        print(fila)


if __name__ == "__main__":
    main()
