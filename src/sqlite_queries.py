import sqlite3

from config import DB_FILE


def conectar() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def buscar_por_correo(correo_objetivo: str):
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
