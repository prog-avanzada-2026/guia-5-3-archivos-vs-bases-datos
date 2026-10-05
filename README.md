# Guía 5-3 — Archivos vs. bases de datos

Proyecto experimental para comparar consultas sobre un archivo CSV y sobre SQLite.

## Objetivo

Ejecutar las mismas preguntas sobre el mismo conjunto de datos y medir:

1. CSV con recorrido secuencial.
2. SQLite sin índices adicionales.
3. SQLite con índices.

La intención no es demostrar que una tecnología "siempre gana", sino observar qué cambia cuando el volumen de datos crece y qué trabajo realiza un motor de base de datos.

## Requisitos

- Python 3.11 o superior.
- No requiere paquetes externos.

## Ejecución rápida

```bash
python src/generar_datos.py --rows 5000000
python src/preparar_sqlite.py
python src/benchmark.py
python src/preparar_sqlite.py --indexes
python src/benchmark.py
```

Para el Taller 5, use el escenario pesado de 20 millones de registros:

```bash
python src/generar_datos.py --rows 20000000
python src/preparar_sqlite.py
python src/benchmark.py
python src/preparar_sqlite.py --indexes
python src/benchmark.py
```

Los archivos grandes se generan localmente y no se almacenan en Git.


## Taller 5 — Escenario pesado

El taller utiliza 20 000 000 de registros. El conjunto se genera por streaming:
no se cargan todos los datos en memoria.

```bash
python src/generar_datos.py --rows 20000000
python src/preparar_sqlite.py
python src/benchmark.py
```

Después se crean índices y se repite:

```bash
python src/preparar_sqlite.py --indexes
python src/benchmark.py
```

El estudiante debe agregar una consulta propia, medirla antes y después de
proponer un índice y documentar el plan de ejecución con `EXPLAIN QUERY PLAN`.

Advertencia: el tamaño final depende del sistema, pero 20 millones de registros
pueden ocupar varios GB entre CSV y SQLite. Verifique espacio libre antes de
ejecutar el taller.
