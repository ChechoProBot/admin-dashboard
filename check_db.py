import sqlite3
import os

# Verificar si existe la base de datos
db_path = 'data/appadmi.db'
if os.path.exists(db_path):
    print('✅ Base de datos encontrada en:', db_path)

    # Conectar y verificar tablas
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Obtener todas las tablas
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()

    print(f'📊 Tablas encontradas: {len(tables)}')
    for table in tables:
        print(f'  - {table[0]}')

        # Contar registros en cada tabla
        cur.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cur.fetchone()[0]
        print(f'    Registros: {count}')

        if count > 0:
            # Mostrar algunos registros de ejemplo
            cur.execute(f'SELECT * FROM {table[0]} LIMIT 3')
            rows = cur.fetchall()
            print(f'    Ejemplos: {rows[:2] if len(rows) > 0 else "Sin datos"}')
        print()

    conn.close()
else:
    print('❌ Base de datos no encontrada')
