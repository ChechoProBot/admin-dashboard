import sqlite3
from typing import Any, List, Dict, Optional
import os

# Get the absolute path to the data directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, "data")
DB_PATH = os.path.join(data_dir, "appadmi.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

def add_propietario(nombre: str, email: str, telefono: str, propiedad: str, unidad: str, coeficiente: float = 0.0) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO propietarios (nombre, email, telefono, propiedad, unidad, coeficiente) VALUES (?, ?, ?, ?, ?, ?)",
                (nombre, email, telefono, propiedad, unidad, coeficiente))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def get_propietarios() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM propietarios")
    rows = cur.fetchall()
    conn.close()
    cols = [desc[0] for desc in cur.description]
    return [dict(zip(cols, row)) for row in rows]

def add_propiedad(nombre: str, direccion: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO propiedades (nombre, direccion) VALUES (?, ?)",
                (nombre, direccion))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def get_propiedades() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM propiedades")
    rows = cur.fetchall()
    conn.close()
    cols = [desc[0] for desc in cur.description]
    return [dict(zip(cols, row)) for row in rows]

def add_unidad(propiedad: str, unidad: str, coeficiente: float = 0.0) -> int:
    # Validar que el coeficiente sea un valor numérico válido
    if coeficiente is None or (isinstance(coeficiente, float) and coeficiente != coeficiente):  # Verifica NaN
        coeficiente = 0.0
    elif not isinstance(coeficiente, (int, float)):
        coeficiente = 0.0
    else:
        coeficiente = float(coeficiente)

    # Asegurar que esté en un rango válido
    coeficiente = max(0.0, min(100.0, coeficiente))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO unidades (propiedad, unidad, coeficiente) VALUES (?, ?, ?)",
                (propiedad, unidad, coeficiente))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def get_unidades() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM unidades")
    rows = cur.fetchall()
    conn.close()
    cols = [desc[0] for desc in cur.description]

    unidades = []
    for row in rows:
        unidad_dict = dict(zip(cols, row))
        # Asegurar que coeficiente sea un valor numérico válido
        if 'coeficiente' in unidad_dict:
            coef = unidad_dict['coeficiente']
            if coef is None:
                unidad_dict['coeficiente'] = 0.0
            elif isinstance(coef, (int, float)):
                unidad_dict['coeficiente'] = float(coef)
            else:
                unidad_dict['coeficiente'] = 0.0
        unidades.append(unidad_dict)

    return unidades

def update_unidad_coeficiente(unidad_id: int, coeficiente: float) -> None:
    # Validar que el coeficiente sea un valor numérico válido
    if coeficiente is None or (isinstance(coeficiente, float) and coeficiente != coeficiente):  # Verifica NaN
        coeficiente = 0.0
    elif not isinstance(coeficiente, (int, float)):
        coeficiente = 0.0
    else:
        coeficiente = float(coeficiente)

    # Asegurar que esté en un rango válido
    coeficiente = max(0.0, min(100.0, coeficiente))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE unidades SET coeficiente = ? WHERE id = ?",
                (coeficiente, unidad_id))
    conn.commit()
    conn.close()

def get_unidad_by_id(unidad_id: int) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM unidades WHERE id = ?", (unidad_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        cols = [desc[0] for desc in cur.description]
        return dict(zip(cols, row))
    return None

def add_factura(propietario_id: int, unidad_id: int, fecha: str, recibo: int, cuota_sostenimiento: float, saldo_pendiente: float, intereses_mora: float, cuota_extra: float, otros: str, otros_valor: float, total: float) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO facturas (propietario_id, unidad_id, fecha, recibo, cuota_sostenimiento, saldo_pendiente, intereses_mora, cuota_extra, otros, otros_valor, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (propietario_id, unidad_id, fecha, recibo, cuota_sostenimiento, saldo_pendiente, intereses_mora, cuota_extra, otros, otros_valor, total))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def get_facturas() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM facturas")
    rows = cur.fetchall()
    conn.close()
    cols = [desc[0] for desc in cur.description]
    return [dict(zip(cols, row)) for row in rows]

def add_pago(factura_id: int, monto: float, fecha: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO pagos (factura_id, monto, fecha) VALUES (?, ?, ?)", (factura_id, monto, fecha))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def get_pagos() -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pagos")
    rows = cur.fetchall()
    conn.close()
    cols = [desc[0] for desc in cur.description]
    return [dict(zip(cols, row)) for row in rows]

def set_config(clave: str, valor: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("REPLACE INTO configuracion (clave, valor) VALUES (?, ?)", (clave, valor))
    conn.commit()
    conn.close()

def get_config(clave: str) -> Optional[str]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT valor FROM configuracion WHERE clave = ?", (clave,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
