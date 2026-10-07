"""Consultas sobre el CSV mediante recorrido secuencial."""

import csv
from collections import defaultdict

from config import CSV_FILE


def buscar_por_correo(correo_objetivo: str):
    """Busca la primera fila cuyo correo coincida.

    Args:
        correo_objetivo: Correo exacto que se desea localizar.

    Returns:
        dict | None: Fila encontrada como diccionario, o None si no existe.
    """
    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["correo"] == correo_objetivo:
                return row
    return None


def filtrar_ciudad_promedio(ciudad: str, promedio_minimo: float) -> int:
    """Cuenta estudiantes de una ciudad con promedio mínimo.

    Args:
        ciudad: Ciudad que deben tener los registros.
        promedio_minimo: Promedio mínimo (inclusive) para contar la fila.

    Returns:
        int: Cantidad de registros que cumplen las condiciones.
    """
    encontrados = 0
    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ciudad"] == ciudad and float(row["promedio"]) >= promedio_minimo:
                encontrados += 1
    return encontrados


def promedio_por_programa() -> dict[str, float]:
    """Calcula el promedio de notas agrupado por programa.

    Returns:
        dict[str, float]: Promedio por nombre de programa.
    """
    acumulados = defaultdict(float)
    cantidades = defaultdict(int)

    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            programa = row["programa"]
            acumulados[programa] += float(row["promedio"])
            cantidades[programa] += 1

    return {
        programa: acumulados[programa] / cantidades[programa] for programa in acumulados
    }
