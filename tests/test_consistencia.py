import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import csv_queries
import sqlite_queries
from config import CSV_FILE, DB_FILE


@unittest.skipUnless(
    CSV_FILE.exists() and DB_FILE.exists(),
    "Primero genere los datos y la base de datos.",
)
class TestConsistencia(unittest.TestCase):
    def test_busqueda_correo(self):
        correo = "estudiante0000100@universidad.edu.co"
        csv_row = csv_queries.buscar_por_correo(correo)
        sql_row = sqlite_queries.buscar_por_correo(correo)
        self.assertEqual(csv_row["correo"], sql_row[2])

    def test_filtro(self):
        self.assertEqual(
            csv_queries.filtrar_ciudad_promedio("Bogota", 4.5),
            sqlite_queries.filtrar_ciudad_promedio("Bogota", 4.5),
        )

    def test_agrupacion(self):
        csv_r = csv_queries.promedio_por_programa()
        sql_r = sqlite_queries.promedio_por_programa()

        self.assertEqual(set(csv_r), set(sql_r))
        for programa in csv_r:
            self.assertAlmostEqual(csv_r[programa], sql_r[programa], places=8)


if __name__ == "__main__":
    unittest.main()
