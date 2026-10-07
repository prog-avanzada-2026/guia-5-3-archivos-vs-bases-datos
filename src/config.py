"""Configuración compartida de la guía 5-3.

Define las rutas de trabajo y los catálogos usados al generar el
conjunto de datos sintético.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"

CSV_FILE = DATA_DIR / "estudiantes_grande.csv"
DB_FILE = DATA_DIR / "estudiantes_grande.db"

CITIES = [
    "Bogota",
    "Medellin",
    "Cali",
    "Barranquilla",
    "Bucaramanga",
    "Pereira",
    "Manizales",
    "Cartagena",
]

PROGRAMS = [
    "Ingenieria de Sistemas",
    "Ingenieria Electronica",
    "Ingenieria Industrial",
    "Ingenieria de Telecomunicaciones",
    "Ingenieria Electrica",
]
