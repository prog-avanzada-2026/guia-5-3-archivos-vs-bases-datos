"""Consultas equivalentes sobre SQLite y plan de ejecución."""

import sqlite3

from config import DB_FILE


def conectar() -> sqlite3.Connection:
    """Abre una conexión con la base de datos del taller.

    Returns:
        sqlite3.Connection: Conexión activa al archivo SQLite.
    """
    return sqlite3.connect(DB_FILE)


def buscar_por_correo(correo_objetivo: str):
    """Busca la fila cuyo correo coincida.

    Args:
        correo_objetivo: Correo exacto que se desea localizar.

    Returns:
        tuple | None: Fila encontrada, o None si no existe.
    """
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT id, nombre, correo, ciudad, programa,
                   semestre, promedio, creditos, estado
            FROM estudiantes
            WHERE correo = ?
            """,
            (correo_objetivo,),
        )
        return cursor.fetchone()


def filtrar_ciudad_promedio(ciudad: str, promedio_minimo: float) -> int:
    """Cuenta estudiantes de una ciudad con promedio mínimo.

    Args:
        ciudad: Ciudad que deben tener los registros.
        promedio_minimo: Promedio mínimo (inclusive) para contar la fila.

    Returns:
        int: Cantidad de registros que cumplen las condiciones.
    """
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM estudiantes
            WHERE ciudad = ?
              AND promedio >= ?
            """,
            (ciudad, promedio_minimo),
        )
        return cursor.fetchone()[0]


def promedio_por_programa() -> dict[str, float]:
    """Calcula el promedio de notas agrupado por programa.

    Returns:
        dict[str, float]: Promedio por nombre de programa.
    """
    with conectar() as conn:
        cursor = conn.execute(
            """
            SELECT programa, AVG(promedio)
            FROM estudiantes
            GROUP BY programa
            """
        )
        return dict(cursor.fetchall())


def plan_busqueda_correo() -> list:
    """Obtiene el plan de ejecución de la búsqueda por correo.

    Returns:
        list: Filas devueltas por EXPLAIN QUERY PLAN.
    """
    with conectar() as conn:
        cursor = conn.execute(
            """
            EXPLAIN QUERY PLAN
            SELECT *
            FROM estudiantes
            WHERE correo = ?
            """,
            ("estudiante0000001@universidad.edu.co",),
        )
        return cursor.fetchall()
