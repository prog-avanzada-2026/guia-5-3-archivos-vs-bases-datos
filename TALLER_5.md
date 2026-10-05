# Taller 5 — Consultas sobre 20 millones de registros

## Propósito

Comprobar experimentalmente cómo cambia el costo de consultar información
cuando el volumen de datos deja de ser pequeño.

## Escenario

Genere exactamente 20 000 000 de registros:

```bash
python src/generar_datos.py --rows 20000000
```

Construya SQLite sin índices adicionales:

```bash
python src/preparar_sqlite.py
```

Ejecute:

```bash
python src/benchmark_pesado.py --rows 20000000
```

Luego cree los índices existentes y repita:

```bash
python src/preparar_sqlite.py --indexes
python src/benchmark_pesado.py --rows 20000000
```

## Trabajo a desarrollar

1. Registre el tamaño del CSV y del archivo SQLite.
2. Compare la búsqueda de un correo ubicado aproximadamente al 10 %, 50 %, 90 %
   y final del conjunto.
3. Explique por qué el tiempo del CSV depende de la posición del registro.
4. Compare el plan de SQLite antes y después de crear el índice.
5. Diseñe una nueva consulta con mínimo tres condiciones.
6. Implemente la misma consulta en CSV y SQLite.
7. Mida la consulta sin un índice nuevo.
8. Proponga y cree un índice para esa consulta.
9. Repita la medición.
10. Use `EXPLAIN QUERY PLAN` y determine si el índice fue utilizado.
11. Explique si el índice realmente mejora la consulta y por qué.
12. Identifique un costo o desventaja introducido por mantener índices.

## Entrega

- Código funcional.
- Archivo `resultados_taller.md` con tabla de mediciones.
- Explicación técnica de los resultados.
- Captura o transcripción de `EXPLAIN QUERY PLAN` antes y después.
- Commit final:

```bash
git add .
git commit -m "Completa Taller 5 de rendimiento con 20 millones de registros"
```

No se deben subir a GitHub los archivos CSV ni SQLite.
