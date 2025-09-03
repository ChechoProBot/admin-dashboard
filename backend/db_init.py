import sqlite3
import os

# Get the absolute path to the data directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, "data")
DB_PATH = os.path.join(data_dir, "appadmi.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Propiedades
    cur.execute('''CREATE TABLE IF NOT EXISTS propiedades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    # Propietarios
    # Unidades
    cur.execute('''CREATE TABLE IF NOT EXISTS unidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        propiedad TEXT NOT NULL,
        unidad TEXT NOT NULL,
        coeficiente REAL DEFAULT 0.0
    )''')
    # Facturas
    cur.execute('''CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        propietario_id INTEGER,
        unidad_id INTEGER,
        fecha TEXT,
        recibo INTEGER,
        cuota_sostenimiento REAL,
        saldo_pendiente REAL,
        intereses_mora REAL,
        cuota_extra REAL,
        otros TEXT,
        otros_valor REAL,
        total REAL,
        FOREIGN KEY(propietario_id) REFERENCES propietarios(id),
        FOREIGN KEY(unidad_id) REFERENCES unidades(id)
    )''')
    # Pagos
    cur.execute('''CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factura_id INTEGER,
        monto REAL,
        fecha TEXT,
        FOREIGN KEY(factura_id) REFERENCES facturas(id)
    )''')
    # Configuración global
    cur.execute('''CREATE TABLE IF NOT EXISTS configuracion (
        clave TEXT PRIMARY KEY,
        valor TEXT
    )''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Base de datos y tablas creadas correctamente.")
