import argparse
import csv
import sqlite3
from time import perf_counter

from config import CSV_FILE, DB_FILE, DATA_DIR


SCHEMA = """
CREATE TABLE estudiantes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    programa TEXT NOT NULL,
    semestre INTEGER NOT NULL,
    promedio REAL NOT NULL,
    creditos INTEGER NOT NULL,
    estado TEXT NOT NULL
);
"""


def importar_csv(conn: sqlite3.Connection, batch_size: int = 10_000) -> int:
    total = 0
    lote = []

    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lote.append((
                int(row["id"]), row["nombre"], row["correo"], row["ciudad"],
                row["programa"], int(row["semestre"]), float(row["promedio"]),
                int(row["creditos"]), row["estado"],
            ))

            if len(lote) >= batch_size:
                conn.executemany(
                    "INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    lote,
                )
                total += len(lote)
                lote.clear()

        if lote:
            conn.executemany(
                "INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                lote,
            )
            total += len(lote)

    conn.commit()
    return total


def crear_indices(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_estudiantes_correo ON estudiantes(correo)"
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_estudiantes_ciudad_promedio
        ON estudiantes(ciudad, promedio)
        """
    )
    conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--indexes", action="store_true")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if args.indexes:
        if not DB_FILE.exists():
            raise FileNotFoundError("Primero cree la base de datos.")
        inicio = perf_counter()
        with sqlite3.connect(DB_FILE) as conn:
            crear_indices(conn)
        print(f"Indices creados en {perf_counter() - inicio:.3f} s")
        return

    if not CSV_FILE.exists():
        raise FileNotFoundError("Primero genere el CSV.")

    if DB_FILE.exists():
        DB_FILE.unlink()

    inicio = perf_counter()
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(SCHEMA)
        total = importar_csv(conn)

    tiempo = perf_counter() - inicio
    mb = DB_FILE.stat().st_size / (1024 * 1024)

    print(f"Registros importados: {total:,}")
    print(f"Base: {DB_FILE}")
    print(f"Tamano: {mb:.2f} MB")
    print(f"Tiempo de importacion: {tiempo:.3f} s")
    print("Base creada SIN indices adicionales.")


if __name__ == "__main__":
    main()
