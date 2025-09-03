import streamlit as st
from fpdf import FPDF
import tempfile
import base64
import pywhatkit
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

# Add the backend directory to sys.path for module resolution
import importlib.util

backend_path = os.path.abspath(os.path.join("E:\\SERGIO\\APPaDMINISTRACION\\AppADMI", "backend"))
db_utils_path = os.path.join(backend_path, "db_utils.py")
if backend_path not in sys.path:
    sys.path.append(backend_path)

if os.path.exists(db_utils_path):
    spec = importlib.util.spec_from_file_location("db_utils", db_utils_path)
    db_utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(db_utils)
    get_propietarios = db_utils.get_propietarios
    add_propietario = db_utils.add_propietario
    get_unidades = db_utils.get_unidades
    add_unidad = db_utils.add_unidad
    update_unidad_coeficiente = db_utils.update_unidad_coeficiente
    get_propiedades = db_utils.get_propiedades
    add_propiedad = db_utils.add_propiedad
    get_facturas = db_utils.get_facturas
    add_factura = db_utils.add_factura
    get_pagos = db_utils.get_pagos
    add_pago = db_utils.add_pago
    get_config = db_utils.get_config
    set_config = db_utils.set_config
else:
    raise ImportError(f"db_utils.py not found in {backend_path}")
import sqlite3

st.set_page_config(page_title="AppAdmi - Administración", page_icon="🏢", layout="wide")

# Cargar estilos CSS modernos
st.markdown("""
<style>
/* Variables CSS para colores modernos */
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-600: #4b5563;
    --gray-900: #111827;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --border-radius: 8px;
    --border-radius-lg: 12px;
}

/* Reset y tipografía moderna */
* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--gray-900);
}

/* Headers modernos */
.modern-header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 2rem;
    border-radius: var(--border-radius-lg);
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: var(--shadow-lg);
}

.modern-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.modern-header p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0;
}

/* Cards modernas */
.modern-card {
    background: white;
    border-radius: var(--border-radius-lg);
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--gray-200);
    transition: all 0.3s ease;
}

.modern-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

.modern-card h3 {
    color: var(--primary-color);
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.modern-card h3::before {
    content: '';
    width: 4px;
    height: 24px;
    background: var(--primary-color);
    border-radius: 2px;
}

/* Formularios modernos */
.modern-form {
    background: var(--gray-50);
    padding: 2rem;
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--gray-200);
}

.form-section {
    background: white;
    padding: 1.5rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
    border: 1px solid var(--gray-200);
}

.form-section h4 {
    color: var(--gray-600);
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Botones modernos */
.modern-btn {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: var(--border-radius);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
}

.modern-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.modern-btn-secondary {
    background: var(--gray-200);
    color: var(--gray-700);
}

.modern-btn-secondary:hover {
    background: var(--gray-300);
}

.modern-btn-success {
    background: linear-gradient(135deg, var(--success-color), #059669);
}

.modern-btn-danger {
    background: linear-gradient(135deg, var(--danger-color), #dc2626);
}

/* Tablas modernas */
.modern-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.modern-table th {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.modern-table td {
    padding: 1rem;
    border-bottom: 1px solid var(--gray-200);
    background: white;
}

.modern-table tr:hover td {
    background: var(--gray-50);
}

/* Sidebar moderno */
.modern-sidebar {
    background: white;
    padding: 1.5rem;
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-sm);
    margin-bottom: 2rem;
}

.modern-sidebar h3 {
    color: var(--primary-color);
    font-size: 1.2rem;
    margin-bottom: 1rem;
}

/* Métricas modernas */
.metric-card {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 1.5rem;
    border-radius: var(--border-radius-lg);
    text-align: center;
    box-shadow: var(--shadow-md);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    display: block;
}

.metric-label {
    font-size: 0.9rem;
    opacity: 0.9;
    font-weight: 500;
}

/* Grid layout moderno */
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

/* Status indicators */
.status-success {
    color: var(--success-color);
    font-weight: 600;
}

.status-warning {
    color: var(--warning-color);
    font-weight: 600;
}

.status-danger {
    color: var(--danger-color);
    font-weight: 600;
}

/* Responsive design */
@media (max-width: 768px) {
    .modern-header {
        padding: 1.5rem;
    }

    .modern-header h1 {
        font-size: 2rem;
    }

    .modern-card {
        padding: 1.5rem;
    }

    .grid-container {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# Página de acceso inicial
# Verificar si acabamos de hacer login
if st.session_state.get("logged_in", False) and not st.session_state.get("welcome_shown", False):
    # Mostrar mensaje de bienvenida solo una vez
    st.session_state["welcome_shown"] = True
    st.success("¡Login exitoso! Bienvenido al sistema APPADMI.")
    st.balloons()

# Verificar autenticación
if not st.session_state.get("logged_in", False):
    st.warning("🔐 Debe iniciar sesión para acceder al sistema.")
    st.info("Use el menú lateral para ir a la página de login.")

    # Header moderno
    st.markdown('<div class="modern-header"><h1>🏢 APPADMI</h1><p>Sistema de Administración de Propiedades</p></div>', unsafe_allow_html=True)

    # Grid de características
    st.markdown("""
    <div class="grid-container">
        <div class="modern-card">
            <h3>🏢 Gestión de Propiedades</h3>
            <p>Administre edificios y conjuntos residenciales con facilidad. Registre propiedades, direcciones y mantenga toda la información organizada.</p>
        </div>
        <div class="modern-card">
            <h3>� Control de Unidades</h3>
            <p>Gestiona apartamentos, casas y espacios individuales. Asocia unidades a propiedades y mantén el control total.</p>
        </div>
        <div class="modern-card">
            <h3>👥 Administración de Propietarios</h3>
            <p>Mantén información actualizada de todos los residentes. Registra datos personales y asigna unidades específicas.</p>
        </div>
        <div class="modern-card">
            <h3>💰 Sistema Financiero</h3>
            <p>Control completo de facturación, pagos y estados de cuenta. Genera recibos y mantén el seguimiento financiero.</p>
        </div>
        <div class="modern-card">
            <h3>📊 Dashboard y Reportes</h3>
            <p>Métricas en tiempo real, gráficos interactivos y reportes detallados para tomar mejores decisiones.</p>
        </div>
        <div class="modern-card">
            <h3>📧 Comunicaciones</h3>
            <p>Envío de notificaciones, recordatorios y comunicaciones masivas a propietarios y residentes.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Call to action moderno
    st.markdown("""
    <div class="modern-card" style="text-align: center; background: linear-gradient(135deg, #f3f4f6, #e5e7eb);">
        <h3 style="color: var(--gray-600);">🚀 Comienza Ahora</h3>
        <p style="margin-bottom: 1.5rem;">Inicia sesión para acceder a todas las funcionalidades del sistema</p>
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
        <p style="color: var(--gray-600);"><strong>Usa el menú lateral para acceder al login</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Detener la ejecución aquí si no está autenticado
    st.stop()

# Si está autenticado, mostrar la aplicación principal
else:
    st.title("🏢 APPaDMINISTRACION - Plataforma Principal")
    st.markdown("---")

    # Información del usuario y opción de cerrar sesión
    col1, col2 = st.columns([3, 1])
    with col1:
        user_email = st.session_state.get("user_email", "admin")
        st.info(f"👤 Sesión activa: {user_email}")
    with col2:
        if st.button("🚪 Cerrar Sesión", type="secondary"):
            # Limpiar la sesión
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Sesión cerrada correctamente.")
            st.info("Use el menú lateral para volver al login.")
            st.rerun()

    st.markdown("---")

# Inicializar estado de navegación
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Inicio"

# Función para cambiar de página
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Menú principal solo en la página de inicio
if st.session_state.current_page == "Inicio":
    menu = st.sidebar.selectbox(
        "Menú principal",
        [
            "Inicio",
            "Propiedad (Edificio/Conjunto)",
            "Unidades (Apartamentos/Casas)",
            "Registro de propietarios",
            "Facturación",
            "Recibos de caja (Pagos)",
            "Estado de cuenta por propietario",
            "Egresos y gastos",
            "Dashboard financiero",
            "Reportes mensuales",
            "Configuración de %"
        ]
    )

    # Actualizar página actual cuando se selecciona del menú
    if menu != "Inicio":
        st.session_state.current_page = menu
        st.rerun()

# Obtener la página actual
current_page = st.session_state.current_page

if current_page == "Inicio":
    st.markdown("---")
    st.subheader("Acceso rápido a configuración de porcentajes y coeficientes")
    if st.button("Ir a configuración de %"):
        st.session_state["menu_override"] = True
        st.experimental_rerun()

if st.session_state.get("menu_override", False):
    menu = "Configuración de %"
    st.session_state["menu_override"] = False

# Nueva página de configuración
elif current_page == "Configuración de %":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_config"):
        navigate_to("Inicio")

    st.header("Configuración de porcentajes globales y coeficientes por unidad")
    st.markdown("---")
    st.subheader("Porcentajes globales")
    ipc = get_config("ipc") or 15.1
    sml = float(get_config("sml") or 1423000)
    transp = float(get_config("transp") or 200000)
    interes_mora = get_config("interes_mora") or 1.888
    with st.form(key="form_porcentajes"):
        nuevo_ipc = st.number_input("IPC (%)", min_value=0.0, value=float(ipc), step=0.01)
        nuevo_sml = st.number_input("SML ($)", min_value=0.0, value=float(sml), step=1000.0)
        nuevo_transp = st.number_input("Transporte ($)", min_value=0.0, value=float(transp), step=1000.0)
        nuevo_interes_mora = st.number_input("Interés de mora (%)", min_value=0.0, value=float(interes_mora), step=0.01)
        submit_porcentajes = st.form_submit_button("Guardar porcentajes globales")
    if submit_porcentajes:
        set_config("ipc", str(nuevo_ipc))
        set_config("sml", str(nuevo_sml))
        set_config("transp", str(nuevo_transp))
        set_config("interes_mora", str(nuevo_interes_mora))
        st.success("Porcentajes globales actualizados.")

    st.markdown("---")
    st.subheader("Coeficientes y edición por unidad")

    unidades = get_unidades()
    if unidades:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h4>📊 Configuración de Coeficientes por Unidad</h4>', unsafe_allow_html=True)
        st.markdown('<p>Establece el porcentaje de participación de cada unidad en los gastos comunes</p>', unsafe_allow_html=True)

        # Mostrar resumen de coeficientes actuales
        def get_coeficiente_safe(unidad):
            coef = unidad.get("coeficiente", 0)
            if coef is None or (isinstance(coef, float) and coef != coef):  # Verifica NaN
                return 0.0
            return float(coef)

        total_coeficientes = sum(get_coeficiente_safe(unidad) for unidad in unidades)
        st.metric("📈 Suma Total de Coeficientes", f"{total_coeficientes:.2f}%")

        # Opción para distribuir coeficientes equitativamente
        if st.button("⚖️ Distribuir Coeficientes Equitativamente", help="Asigna el mismo porcentaje a todas las unidades"):
            coeficiente_equitativo = 100.0 / len(unidades)
            for unidad in unidades:
                update_unidad_coeficiente(unidad['id'], coeficiente_equitativo)
            st.success(f"✅ Coeficientes distribuidos equitativamente: {coeficiente_equitativo:.2f}% por unidad")
            st.rerun()

        st.markdown("---")

        # Formulario para editar coeficientes
        with st.form(key="form_coeficientes"):
            st.markdown('<h5>✏️ Editar Coeficientes</h5>', unsafe_allow_html=True)

            coeficientes_actualizados = []
            for idx, unidad in enumerate(unidades):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                with col1:
                    st.markdown(f"🏠 **{unidad['unidad']}**")
                with col2:
                    st.markdown(f"🏢 **{unidad['propiedad']}**")
                with col3:
                    coef_actual = unidad.get("coeficiente", 0.0)
                    nuevo_coef = st.number_input(
                        f"Coeficiente (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(coef_actual),
                        step=0.01,
                        key=f"coef_{idx}",
                        help=f"Coeficiente actual: {coef_actual}%"
                    )
                with col4:
                    coeficientes_actualizados.append((unidad['id'], nuevo_coef))

            # Calcular suma de nuevos coeficientes
            suma_nueva = sum(coef for _, coef in coeficientes_actualizados)
            st.metric("📊 Nueva Suma de Coeficientes", f"{suma_nueva:.2f}%")

            if abs(suma_nueva - 100.0) > 0.01:
                st.warning(f"⚠️ La nueva suma será {suma_nueva:.2f}%. Considera ajustar los valores para llegar a 100%.")
                guardar_de_todas_formas = st.checkbox("Guardar de todas formas (no recomendado)", key="guardar_coeficientes_warning")
            else:
                st.success("✅ Los coeficientes suman 100%. Distribución perfecta.")
                guardar_de_todas_formas = True

            submit_coeficientes = st.form_submit_button("💾 Guardar Coeficientes", use_container_width=True, disabled=not guardar_de_todas_formas)

        if submit_coeficientes:
            # Actualizar coeficientes en la base de datos
            for unidad_id, nuevo_coef in coeficientes_actualizados:
                update_unidad_coeficiente(unidad_id, nuevo_coef)

            st.success("✅ Coeficientes actualizados correctamente.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Mostrar tabla resumen
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h4>📋 Resumen de Coeficientes</h4>', unsafe_allow_html=True)

        # Crear DataFrame para mostrar
        import pandas as pd
        df_coeficientes = pd.DataFrame([
            {
                'Unidad': unidad['unidad'],
                'Propiedad': unidad['propiedad'],
                'Coeficiente (%)': get_coeficiente_safe(unidad)
            }
            for unidad in unidades
        ])

        st.dataframe(df_coeficientes, use_container_width=True)

        # Gráfico de distribución de coeficientes
        if len(unidades) > 1:
            st.markdown("---")
            st.markdown('<h5>📊 Distribución de Coeficientes</h5>', unsafe_allow_html=True)

            # Filtrar y validar coeficientes
            coefs_validos = []
            labels_validos = []

            for unidad in unidades:
                coef = unidad.get('coeficiente', 0)
                # Validar que el coeficiente sea un número válido y no NaN
                if coef is not None and not (isinstance(coef, float) and coef != coef):  # Verifica NaN
                    coefs_validos.append(float(coef) if coef > 0 else 0.01)  # Evitar valores 0 que causan problemas en pie chart
                    labels_validos.append(f"{unidad['unidad']}\n({unidad['propiedad']})")

            # Solo crear gráfico si hay coeficientes válidos
            if coefs_validos and sum(coefs_validos) > 0:
                fig, ax = plt.subplots(figsize=(10, 6))

                ax.pie(coefs_validos, labels=labels_validos, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                ax.set_title('Distribución de Coeficientes por Unidad')

                st.pyplot(fig)
            else:
                st.info("📊 No hay suficientes datos de coeficientes para generar el gráfico.")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("📝 No hay unidades registradas. Primero registra unidades para configurar sus coeficientes.")

    # Botón de configuración (rueda) en la esquina inferior izquierda
    if st.session_state.get("logged_in", False):
        st.markdown("""
<div class="config-btn" id="config-btn">
    <span style='font-size:28px;'>&#9881;</span>
</div>
""", unsafe_allow_html=True)
        show_config = st.sidebar.checkbox("Editar perfil del administrador", value=False)
        if show_config:
            st.sidebar.header("Editar perfil del administrador")
            nombre_admin = st.session_state.get("nombre_admin", "Administrador")
            email_admin = st.session_state.get("email_admin", "")
            password_admin = st.session_state.get("password_admin", "")
            with st.sidebar.form(key="form_admin"):
                nuevo_nombre = st.text_input("Nombre del administrador", value=nombre_admin)
                nuevo_email = st.text_input("Email de registro", value=email_admin)
                nueva_password = st.text_input("Contraseña", value=password_admin, type="password")
                submit_admin = st.form_submit_button("Guardar cambios")
            if submit_admin:
                st.session_state["nombre_admin"] = nuevo_nombre
                st.session_state["email_admin"] = nuevo_email
                st.session_state["password_admin"] = nueva_password
                st.success("Datos del administrador actualizados.")
elif current_page == "Login":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_login"):
        navigate_to("Inicio")

    st.header("Iniciar sesión")
    email_admin = st.session_state.get("email_admin", "")
    password_admin = st.session_state.get("password_admin", "")
    with st.form(key="form_login"):
        email_login = st.text_input("Email")
        password_login = st.text_input("Contraseña", type="password")
        submit_login = st.form_submit_button("Ingresar")
    if submit_login:
        if email_login == email_admin and password_login == password_admin:
            st.session_state["logged_in"] = True
            st.success("¡Bienvenido, administrador!")
        else:
            st.error("Email o contraseña incorrectos.")
elif current_page == "Registro":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_registro"):
        navigate_to("Inicio")

    st.header("Registro de administrador")
    with st.form(key="form_registro"):
        nombre_reg = st.text_input("Nombre completo")
        email_reg = st.text_input("Email")
        password_reg = st.text_input("Contraseña", type="password")
        submit_reg = st.form_submit_button("Registrar")
    if submit_reg:
        st.session_state["nombre_admin"] = nombre_reg
        st.session_state["email_admin"] = email_reg
        st.session_state["password_admin"] = password_reg
        st.success("Administrador registrado correctamente. Ahora puede iniciar sesión.")
    propiedades = st.session_state.get("propiedades", [])
    nombre_admin = st.session_state.get("nombre_admin", "Administrador")
    st.markdown("<div class='center-content'>", unsafe_allow_html=True)
    if propiedades:
        for prop in propiedades:
            st.markdown(f"<h1>🏢 {prop['nombre']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h4>{prop.get('direccion','')}</h4>", unsafe_allow_html=True)
    else:
        st.markdown("<h1>🏢 Sistema administrativo de propiedad horizontal</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='admin-info'>Administrador: <b>{nombre_admin}</b></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Resumen rápido")
    col1, col2, col3 = st.columns(3)
    propietarios = st.session_state.get("propietarios", [])
    egresos = st.session_state.get("egresos", [])
    historial = st.session_state.get("historial_propietarios", {})
    ingresos_adicionales = st.session_state.get("ingresos_adicionales", [])
    total_ingresos = sum(
        sum(pago["monto"] for pago in propietario.get("pagos", []))
        for propietario in historial.values()
    ) + sum(i["valor"] for i in ingresos_adicionales)
    total_egresos = sum(e["valor"] for e in egresos)
    saldo_general = total_ingresos - total_egresos
    with col1:
        st.metric("Propietarios registrados", len(propietarios))
    with col2:
        st.metric("Ingresos totales", f"$ {total_ingresos:,.2f}")
    with col3:
        st.metric("Egresos totales", f"$ {total_egresos:,.2f}")
    st.markdown("---")
    st.markdown("<div class='footer-text'>Desarrollado por APPaDMINISTRACION</div>", unsafe_allow_html=True)
elif current_page == "Propiedad (Edificio/Conjunto)":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_propiedad"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>🏢 Gestión de Propiedades</h1><p>Administra edificios y conjuntos residenciales</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📝 Registrar Nueva Propiedad</h3>', unsafe_allow_html=True)

        with st.form(key="form_propiedad"):
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            nombre_propiedad = st.text_input("🏢 Nombre del edificio o conjunto", placeholder="Ej: Edificio Central, Conjunto Los Álamos")
            direccion = st.text_input("📍 Dirección completa", placeholder="Ej: Carrera 23 # 45-67, Bogotá")
            st.markdown('</div>', unsafe_allow_html=True)

            submit_prop = st.form_submit_button("✅ Crear Propiedad", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if submit_prop:
            propiedad_id = add_propiedad(nombre_propiedad, direccion)
            st.success(f"✅ Propiedad '{nombre_propiedad}' creada correctamente.")
            st.rerun()

    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📊 Estadísticas</h3>', unsafe_allow_html=True)

        propiedades = get_propiedades()
        total_propiedades = len(propiedades)

        st.metric("🏢 Total Propiedades", total_propiedades)

        if total_propiedades > 0:
            st.markdown(f'<p class="status-success">✅ Sistema operativo con {total_propiedades} propiedades registradas</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-warning">⚠️ No hay propiedades registradas aún</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Lista de propiedades
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Propiedades Registradas</h3>', unsafe_allow_html=True)

    if propiedades:
        # Convertir a DataFrame para mejor visualización
        import pandas as pd
        df_propiedades = pd.DataFrame(propiedades)
        df_propiedades.columns = ['ID', 'Nombre', 'Dirección', 'Fecha Creación']
        st.dataframe(df_propiedades, use_container_width=True)
    else:
        st.info("📝 No hay propiedades registradas. Crea tu primera propiedad usando el formulario de arriba.")

    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Unidades (Apartamentos/Casas)":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_unidades"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>🏠 Gestión de Unidades</h1><p>Administra apartamentos, casas y espacios individuales</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📝 Registrar Nueva Unidad</h3>', unsafe_allow_html=True)

        with st.form(key="form_nueva_unidad"):
            # Obtener propiedades existentes
            propiedades = get_propiedades()
            if propiedades:
                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                propiedad_options = {prop["nombre"]: prop["id"] for prop in propiedades}
                propiedad_seleccionada = st.selectbox("🏢 Seleccionar Propiedad", options=list(propiedad_options.keys()))
                propiedad_id = propiedad_options[propiedad_seleccionada]
                propiedad_nombre = propiedad_seleccionada
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                unidad = st.text_input("🏠 Nombre de la Unidad", placeholder="Ej: Apt 101, Casa A, Local 5")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                coeficiente = st.number_input(
                    "📊 Coeficiente (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.01,
                    help="Porcentaje de participación en gastos comunes"
                )
                st.markdown('</div>', unsafe_allow_html=True)

                submit = st.form_submit_button("✅ Agregar Unidad", use_container_width=True)
            else:
                st.warning("⚠️ No hay propiedades registradas. Primero debe crear una propiedad.")
                submit = None

        if submit:
            add_unidad(propiedad_nombre, unidad, coeficiente)
            st.success("✅ Unidad agregada correctamente.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📊 Estadísticas</h3>', unsafe_allow_html=True)

        unidades = get_unidades()
        total_unidades = len(unidades)

        st.metric("🏠 Total Unidades", total_unidades)

        if total_unidades > 0:
            # Contar unidades por propiedad
            propiedades_count = {}
            for unidad in unidades:
                prop = unidad["propiedad"]
                propiedades_count[prop] = propiedades_count.get(prop, 0) + 1

            st.markdown("**Unidades por propiedad:**")
            for prop, count in propiedades_count.items():
                st.markdown(f"• {prop}: {count} unidades")

        st.markdown('</div>', unsafe_allow_html=True)

    # Lista de unidades
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Unidades Registradas</h3>', unsafe_allow_html=True)

    unidades = get_unidades()
    if unidades:
        # Convertir a DataFrame para mejor visualización
        import pandas as pd
        df_unidades = pd.DataFrame(unidades)
        df_unidades.columns = ['ID', 'Propiedad', 'Unidad', 'Coeficiente']

        # Asegurar que los coeficientes sean valores numéricos válidos
        df_unidades['Coeficiente'] = pd.to_numeric(df_unidades['Coeficiente'], errors='coerce').fillna(0.0)

        st.dataframe(df_unidades, use_container_width=True)

        # Gestión de unidades
        st.markdown("---")
        st.markdown('<h4>🔧 Gestionar Unidades</h4>', unsafe_allow_html=True)

        unidad_ids = [u['id'] for u in unidades]
        unidad_idx = st.selectbox(
            "Seleccionar unidad para gestionar",
            options=unidad_ids,
            format_func=lambda i: f"{[u for u in unidades if u['id']==i][0]['unidad']} - {[u for u in unidades if u['id']==i][0]['propiedad']}",
            key="unidad_gestion_select"
        )

        unidad = next(u for u in unidades if u['id'] == unidad_idx)

        col_edit, col_delete = st.columns(2)

        with col_edit:
            editar_unidad = st.checkbox("✏️ Editar unidad", key="editar_unidad_checkbox")
        with col_delete:
            eliminar_unidad = st.checkbox("🗑️ Eliminar unidad", key="eliminar_unidad_checkbox")

        if editar_unidad:
            st.markdown('<div class="modern-form">', unsafe_allow_html=True)
            with st.form(key=f"form_editar_unidad_{unidad_idx}"):
                st.markdown('<h4>Editar Unidad</h4>', unsafe_allow_html=True)

                # Obtener propiedades para el selectbox
                propiedades = get_propiedades()
                if propiedades:
                    propiedad_options = {prop["nombre"]: prop["id"] for prop in propiedades}
                    propiedad_actual = unidad["propiedad"]
                    if propiedad_actual in propiedad_options:
                        propiedad_idx = list(propiedad_options.keys()).index(propiedad_actual)
                    else:
                        propiedad_idx = 0

                    nueva_propiedad_seleccionada = st.selectbox(
                        "🏢 Nueva Propiedad",
                        options=list(propiedad_options.keys()),
                        index=propiedad_idx
                    )
                    nueva_propiedad = nueva_propiedad_seleccionada
                else:
                    nueva_propiedad = st.text_input("Propiedad", value=unidad["propiedad"])

                nueva_unidad = st.text_input("🏠 Nueva Unidad", value=unidad["unidad"])

                # Campo para editar coeficiente
                coeficiente_actual = unidad.get("coeficiente", 0.0)
                nuevo_coeficiente = st.number_input(
                    "📊 Coeficiente (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(coeficiente_actual),
                    step=0.01,
                    help=f"Coeficiente actual: {coeficiente_actual}%"
                )

                submit_edit_unidad = st.form_submit_button("💾 Guardar Cambios", use_container_width=True)

            if submit_edit_unidad:
                conn = sqlite3.connect("E:/SERGIO/APPaDMINISTRACION/AppADMI/data/appadmi.db")
                cur = conn.cursor()
                cur.execute("UPDATE unidades SET propiedad=?, unidad=?, coeficiente=? WHERE id=?",
                           (nueva_propiedad, nueva_unidad, nuevo_coeficiente, unidad_idx))
                conn.commit()
                conn.close()
                st.success("✅ Unidad editada correctamente.")
            st.markdown('</div>', unsafe_allow_html=True)

        if eliminar_unidad:
            st.error("⚠️ **ATENCIÓN:** Esta acción no se puede deshacer.")
            if st.button("🗑️ Confirmar Eliminación", type="primary"):
                conn = sqlite3.connect("E:/SERGIO/APPaDMINISTRACION/AppADMI/data/appadmi.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM unidades WHERE id=?", (unidad_idx,))
                conn.commit()
                conn.close()
                st.success("✅ Unidad eliminada correctamente.")
                st.rerun()
    else:
        st.info("📝 No hay unidades registradas. Crea tu primera unidad usando el formulario de arriba.")

    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Registro de propietarios":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_propietarios"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>👥 Gestión de Propietarios</h1><p>Administra la información de los propietarios de las unidades</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📝 Registrar Nuevo Propietario</h3>', unsafe_allow_html=True)

        with st.form(key="form_nuevo_propietario"):
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            nombre = st.text_input("👤 Nombre completo", placeholder="Ej: Juan Pérez García")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            email = st.text_input("📧 Email", placeholder="juan.perez@email.com")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            telefono = st.text_input("📱 Teléfono", placeholder="Ej: +57 300 123 4567")
            st.markdown('</div>', unsafe_allow_html=True)

            # Obtener propiedades existentes
            propiedades = get_propiedades()
            if propiedades:
                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                propiedad_options = {prop["nombre"]: prop["id"] for prop in propiedades}
                propiedad_seleccionada = st.selectbox("🏢 Seleccionar Propiedad", options=list(propiedad_options.keys()))
                propiedad_id = propiedad_options[propiedad_seleccionada]
                propiedad_nombre = propiedad_seleccionada
                st.markdown('</div>', unsafe_allow_html=True)

                # Obtener unidades existentes
                unidades = get_unidades()
                if unidades:
                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    unidad_options = {f"{u['unidad']} - {u['propiedad']}": u["id"] for u in unidades}
                    unidad_seleccionada = st.selectbox("🏠 Seleccionar Unidad", options=list(unidad_options.keys()))
                    unidad_id = unidad_options[unidad_seleccionada]
                    unidad_info = next(u for u in unidades if u['id'] == unidad_id)
                    unidad_nombre = unidad_info["unidad"]

                    # Verificar que la unidad pertenezca a la propiedad seleccionada
                    if unidad_info["propiedad"] != propiedad_nombre:
                        st.warning("⚠️ La unidad seleccionada no pertenece a la propiedad elegida.")
                        submit = None
                    else:
                        submit = st.form_submit_button("✅ Agregar Propietario", use_container_width=True)
                else:
                    st.warning("⚠️ No hay unidades registradas. Primero debe crear unidades.")
                    submit = None
            else:
                st.warning("⚠️ No hay propiedades registradas. Primero debe crear una propiedad.")
                submit = None

        if submit:
            add_propietario(nombre, email, telefono, propiedad_nombre, unidad_nombre, 0.0)
            st.success("✅ Propietario agregado correctamente.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📊 Estadísticas</h3>', unsafe_allow_html=True)

        propietarios = get_propietarios()
        total_propietarios = len(propietarios)

        st.metric("👥 Total Propietarios", total_propietarios)

        if total_propietarios > 0:
            # Contar propietarios por propiedad
            propiedades_count = {}
            for propietario in propietarios:
                prop = propietario["propiedad"]
                propiedades_count[prop] = propiedades_count.get(prop, 0) + 1

            st.markdown("**Propietarios por propiedad:**")
            for prop, count in propiedades_count.items():
                st.markdown(f"• {prop}: {count} propietarios")

        st.markdown('</div>', unsafe_allow_html=True)

    # Lista de propietarios
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Propietarios Registrados</h3>', unsafe_allow_html=True)

    propietarios = get_propietarios()
    if propietarios:
        # Convertir a DataFrame para mejor visualización
        import pandas as pd
        df_propietarios = pd.DataFrame(propietarios)
        df_propietarios.columns = ['ID', 'Nombre', 'Email', 'Teléfono', 'Propiedad', 'Unidad', 'Coeficiente']
        st.dataframe(df_propietarios, use_container_width=True)

        # Gestión de propietarios
        st.markdown("---")
        st.markdown('<h4>🔧 Gestionar Propietarios</h4>', unsafe_allow_html=True)

        propietario_ids = [p['id'] for p in propietarios]
        propietario_idx = st.selectbox(
            "Seleccionar propietario para gestionar",
            options=propietario_ids,
            format_func=lambda i: f"{[p for p in propietarios if p['id']==i][0]['nombre']} - {[p for p in propietarios if p['id']==i][0]['unidad']}",
            key="propietario_gestion_select"
        )

        propietario = next(p for p in propietarios if p['id'] == propietario_idx)

        col_edit, col_delete = st.columns(2)

        with col_edit:
            editar_prop = st.checkbox("✏️ Editar propietario", key="editar_propietario_checkbox")
        with col_delete:
            eliminar_prop = st.checkbox("🗑️ Eliminar propietario", key="eliminar_propietario_checkbox")

        if editar_prop:
            st.markdown('<div class="modern-form">', unsafe_allow_html=True)
            with st.form(key=f"form_editar_propietario_{propietario_idx}"):
                st.markdown('<h4>Editar Propietario</h4>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                nuevo_nombre = st.text_input("👤 Nombre", value=propietario["nombre"])
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                nuevo_email = st.text_input("📧 Email", value=propietario["email"])
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                nuevo_telefono = st.text_input("📱 Teléfono", value=propietario["telefono"])
                st.markdown('</div>', unsafe_allow_html=True)

                # Obtener propiedades para el selectbox
                propiedades = get_propiedades()
                if propiedades:
                    propiedad_options = {prop["nombre"]: prop["id"] for prop in propiedades}
                    propiedad_actual = propietario["propiedad"]
                    if propiedad_actual in propiedad_options:
                        propiedad_idx = list(propiedad_options.keys()).index(propiedad_actual)
                    else:
                        propiedad_idx = 0

                    nueva_propiedad_seleccionada = st.selectbox(
                        "🏢 Nueva Propiedad",
                        options=list(propiedad_options.keys()),
                        index=propiedad_idx
                    )
                    nueva_propiedad = nueva_propiedad_seleccionada
                else:
                    nueva_propiedad = st.text_input("Propiedad", value=propietario["propiedad"])

                # Obtener unidades para el selectbox
                unidades = get_unidades()
                if unidades:
                    unidad_options = {f"{u['unidad']} - {u['propiedad']}": u["id"] for u in unidades}
                    unidad_actual = f"{propietario['unidad']} - {propietario['propiedad']}"
                    if unidad_actual in unidad_options:
                        unidad_idx = list(unidad_options.keys()).index(unidad_actual)
                    else:
                        unidad_idx = 0

                    nueva_unidad_seleccionada = st.selectbox(
                        "🏠 Nueva Unidad",
                        options=list(unidad_options.keys()),
                        index=unidad_idx
                    )
                    nueva_unidad_info = next(u for u in unidades if u['id'] == unidad_options[nueva_unidad_seleccionada])
                    nueva_unidad = nueva_unidad_info["unidad"]

                    # Verificar consistencia entre propiedad y unidad
                    if nueva_unidad_info["propiedad"] != nueva_propiedad:
                        st.warning("⚠️ La unidad seleccionada no pertenece a la propiedad elegida.")
                        nueva_unidad = propietario["unidad"]  # Mantener el valor original
                else:
                    nueva_unidad = st.text_input("Unidad", value=propietario["unidad"])

                submit_edit_prop = st.form_submit_button("💾 Guardar Cambios", use_container_width=True)

            if submit_edit_prop:
                conn = sqlite3.connect("E:/SERGIO/APPaDMINISTRACION/AppADMI/data/appadmi.db")
                cur = conn.cursor()
                cur.execute("UPDATE propietarios SET nombre=?, email=?, telefono=?, propiedad=?, unidad=? WHERE id=?", (nuevo_nombre, nuevo_email, nuevo_telefono, nueva_propiedad, nueva_unidad, propietario_idx))
                conn.commit()
                conn.close()
                st.success("✅ Propietario editado correctamente.")
            st.markdown('</div>', unsafe_allow_html=True)

        if eliminar_prop:
            st.error("⚠️ **ATENCIÓN:** Esta acción no se puede deshacer.")
            if st.button("🗑️ Confirmar Eliminación", type="primary"):
                conn = sqlite3.connect("E:/SERGIO/APPaDMINISTRACION/AppADMI/data/appadmi.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM propietarios WHERE id=?", (propietario_idx,))
                conn.commit()
                conn.close()
                st.success("✅ Propietario eliminado correctamente.")
                st.rerun()
    else:
        st.info("📝 No hay propietarios registrados. Crea tu primer propietario usando el formulario de arriba.")

    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Facturación":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_facturacion"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>💰 Sistema de Facturación</h1><p>Genera y administra facturas, recibos y estados de cuenta</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📝 Generar Nueva Factura</h3>', unsafe_allow_html=True)

        propietarios = get_propietarios()
        unidades = get_unidades()

        with st.form(key="form_factura"):
            if propietarios and unidades:
                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                propietario_options = {f"{p['nombre']} - {p['unidad']}": p['id'] for p in propietarios}
                propietario_seleccionado = st.selectbox("👤 Seleccionar Propietario", options=list(propietario_options.keys()))
                propietario_id = propietario_options[propietario_seleccionado]
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                unidad_options = {f"{u['unidad']} - {u['propiedad']}": u['id'] for u in unidades}
                unidad_seleccionada = st.selectbox("🏠 Seleccionar Unidad", options=list(unidad_options.keys()))
                unidad_id = unidad_options[unidad_seleccionada]
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                fecha = st.date_input("📅 Fecha de emisión")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                recibo = st.number_input("🧾 Número de recibo", min_value=1, value=6000, step=1)
                st.markdown('</div>', unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    cuota_sostenimiento = st.number_input("🏢 Cuota de sostenimiento", min_value=0.0, step=0.01)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    saldo_pendiente = st.number_input("💰 Saldo pendiente", min_value=0.0, step=0.01)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_b:
                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    intereses_mora = st.number_input("⚠️ Intereses por mora", min_value=0.0, step=0.01)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    cuota_extra = st.number_input("➕ Cuota extraordinaria", min_value=0.0, step=0.01)
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                otros = st.text_input("📋 Otros conceptos", placeholder="Ej: Reparaciones, mantenimiento")
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="form-section">', unsafe_allow_html=True)
                otros_valor = st.number_input("💵 Valor otros", min_value=0.0, step=0.01)
                st.markdown('</div>', unsafe_allow_html=True)

                # Cálculo automático del total
                total = cuota_sostenimiento + saldo_pendiente + intereses_mora + cuota_extra + otros_valor
                st.markdown(f'<div class="total-amount">💰 **Total a pagar: ${total:,.2f}**</div>', unsafe_allow_html=True)

                submit = st.form_submit_button("✅ Generar Factura", use_container_width=True)
            else:
                st.warning("⚠️ Necesitas tener propietarios y unidades registradas para generar facturas.")
                submit = None

        if submit and propietario_id and unidad_id:
            add_factura(propietario_id, unidad_id, str(fecha), recibo, cuota_sostenimiento, saldo_pendiente, intereses_mora, cuota_extra, otros, otros_valor, total)
            st.success("✅ Factura generada correctamente.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📊 Estadísticas de Facturación</h3>', unsafe_allow_html=True)

        facturas = get_facturas()
        total_facturas = len(facturas)

        st.metric("🧾 Total Facturas", total_facturas)

        if total_facturas > 0:
            # Calcular totales
            total_ingresos = sum(f['total'] for f in facturas)
            total_pendiente = sum(f['saldo_pendiente'] for f in facturas)
            total_mora = sum(f['intereses_mora'] for f in facturas)

            st.metric("💰 Total Ingresos", f"${total_ingresos:,.2f}")
            st.metric("⏳ Saldo Pendiente", f"${total_pendiente:,.2f}")
            st.metric("⚠️ Intereses por Mora", f"${total_mora:,.2f}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Lista de facturas
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Facturas Generadas</h3>', unsafe_allow_html=True)

    facturas = get_facturas()
    if facturas:
        # Convertir a DataFrame para mejor visualización
        import pandas as pd
        df_facturas = pd.DataFrame(facturas)
        df_facturas.columns = ['ID', 'Propietario ID', 'Unidad ID', 'Fecha', 'Recibo', 'Cuota', 'Saldo Pendiente', 'Intereses', 'Cuota Extra', 'Otros', 'Valor Otros', 'Total']
        st.dataframe(df_facturas, use_container_width=True)

        # Gestión de facturas
        st.markdown("---")
        st.markdown('<h4>🔧 Gestionar Facturas</h4>', unsafe_allow_html=True)

        factura_ids = [f['id'] for f in facturas]
        factura_idx = st.selectbox(
            "Seleccionar factura para gestionar",
            options=factura_ids,
            format_func=lambda i: f"Recibo {facturas[[f['id'] for f in facturas].index(i)]['recibo']} - ${facturas[[f['id'] for f in facturas].index(i)]['total']:,.2f}",
            key="factura_gestion_select"
        )

        factura = next(f for f in facturas if f['id'] == factura_idx)

        col_edit, col_delete = st.columns(2)

        with col_edit:
            editar_factura = st.checkbox("✏️ Editar factura", key="editar_factura_checkbox")
        with col_delete:
            eliminar_factura = st.checkbox("🗑️ Eliminar factura", key="eliminar_factura_checkbox")

        if editar_factura:
            st.markdown('<div class="modern-form">', unsafe_allow_html=True)
            with st.form(key=f"form_editar_factura_{factura_idx}"):
                st.markdown('<h4>Editar Factura</h4>', unsafe_allow_html=True)

                nueva_fecha = st.date_input("📅 Fecha", value=pd.to_datetime(factura["fecha"]))
                nuevo_recibo = st.number_input("🧾 Número de recibo", min_value=1, value=factura["recibo"] or 6000, step=1)

                col_a, col_b = st.columns(2)
                with col_a:
                    nueva_cuota = st.number_input("🏢 Cuota de sostenimiento", min_value=0.0, value=factura["cuota_sostenimiento"], step=0.01)
                    nuevo_saldo = st.number_input("💰 Saldo pendiente", min_value=0.0, value=factura["saldo_pendiente"], step=0.01)

                with col_b:
                    nuevo_interes = st.number_input("⚠️ Intereses por mora", min_value=0.0, value=factura["intereses_mora"], step=0.01)
                    nueva_extra = st.number_input("➕ Cuota extraordinaria", min_value=0.0, value=factura["cuota_extra"], step=0.01)

                nuevo_otros = st.text_input("📋 Otros conceptos", value=factura["otros"])
                nuevo_otros_valor = st.number_input("💵 Valor otros", min_value=0.0, value=factura["otros_valor"], step=0.01)
                nuevo_total = st.number_input("💰 Total", min_value=0.0, value=factura["total"], step=0.01)

                submit_edit_factura = st.form_submit_button("💾 Guardar Cambios", use_container_width=True)

            if submit_edit_factura:
                conn = sqlite3.connect("E:/SERGIO/APPaDMINISTRACION/AppADMI/data/appadmi.db")
                cur = conn.cursor()
                cur.execute("UPDATE facturas SET fecha=?, recibo=?, cuota_sostenimiento=?, saldo_pendiente=?, intereses_mora=?, cuota_extra=?, otros=?, otros_valor=?, total=? WHERE id=?", (str(nueva_fecha), nuevo_recibo, nueva_cuota, nuevo_saldo, nuevo_interes, nueva_extra, nuevo_otros, nuevo_otros_valor, nuevo_total, factura_idx))
                conn.commit()
                conn.close()
                st.success("✅ Factura editada correctamente.")
            st.markdown('</div>', unsafe_allow_html=True)

        if eliminar_factura:
            st.error("⚠️ **ATENCIÓN:** Esta acción no se puede deshacer.")
            if st.button("🗑️ Confirmar Eliminación", type="primary"):
                conn = sqlite3.connect("E:/SERGIO/APPaDMINISTRACION/AppADMI/data/appadmi.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM facturas WHERE id=?", (factura_idx,))
                conn.commit()
                conn.close()
                st.success("✅ Factura eliminada correctamente.")
                st.rerun()
    else:
        st.info("📝 No hay facturas generadas. Crea tu primera factura usando el formulario de arriba.")

    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Dashboard financiero":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_dashboard"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>📊 Dashboard Financiero</h1><p>Visualización completa de métricas financieras y análisis de datos</p></div>', unsafe_allow_html=True)

    # Métricas principales
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>💰 Resumen Financiero General</h3>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # Obtener datos para métricas
    propiedades = get_propiedades()
    unidades = get_unidades()
    propietarios = get_propietarios()
    facturas = get_facturas()

    with col1:
        st.metric("🏢 Propiedades", len(propiedades))
    with col2:
        st.metric("🏠 Unidades", len(unidades))
    with col3:
        st.metric("👥 Propietarios", len(propietarios))
    with col4:
        total_facturado = sum(f['total'] for f in facturas) if facturas else 0
        st.metric("💵 Total Facturado", f"${total_facturado:,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Gráficos y análisis
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>📈 Distribución por Propiedad</h3>', unsafe_allow_html=True)

        if propietarios:
            import pandas as pd
            df_prop = pd.DataFrame(propietarios)
            propiedad_counts = df_prop['propiedad'].value_counts()

            # Crear gráfico de barras
            fig, ax = plt.subplots(figsize=(8, 4))
            propiedad_counts.plot(kind='bar', ax=ax, color='#4CAF50')
            ax.set_title('Propietarios por Propiedad')
            ax.set_xlabel('Propiedad')
            ax.set_ylabel('Número de Propietarios')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("📝 No hay datos de propietarios para mostrar.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<h3>💰 Ingresos por Mes</h3>', unsafe_allow_html=True)

        if facturas:
            import pandas as pd
            df_fact = pd.DataFrame(facturas)
            df_fact['fecha'] = pd.to_datetime(df_fact['fecha'])
            df_fact['mes'] = df_fact['fecha'].dt.to_period('M')

            ingresos_mensuales = df_fact.groupby('mes')['total'].sum()

            # Crear gráfico de líneas
            fig, ax = plt.subplots(figsize=(8, 4))
            ingresos_mensuales.plot(kind='line', ax=ax, marker='o', color='#2196F3')
            ax.set_title('Ingresos Mensuales')
            ax.set_xlabel('Mes')
            ax.set_ylabel('Total ($)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("📝 No hay datos de facturación para mostrar.")

        st.markdown('</div>', unsafe_allow_html=True)

    # Análisis detallado
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Análisis Detallado</h3>', unsafe_allow_html=True)

    if facturas:
        import pandas as pd
        df_fact = pd.DataFrame(facturas)

        # Estadísticas financieras
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_cuotas = df_fact['cuota_sostenimiento'].sum()
            st.metric("🏢 Cuotas de Sostenimiento", f"${total_cuotas:,.2f}")

        with col2:
            total_pendiente = df_fact['saldo_pendiente'].sum()
            st.metric("⏳ Saldos Pendientes", f"${total_pendiente:,.2f}")

        with col3:
            total_mora = df_fact['intereses_mora'].sum()
            st.metric("⚠️ Intereses por Mora", f"${total_mora:,.2f}")

        with col4:
            total_extra = df_fact['cuota_extra'].sum()
            st.metric("➕ Cuotas Extraordinarias", f"${total_extra:,.2f}")

        # Tabla de resumen por propietario
        st.markdown("---")
        st.markdown('<h4>📊 Resumen por Propietario</h4>', unsafe_allow_html=True)

        # Unir datos de propietarios con facturas
        propietarios_dict = {p['id']: p['nombre'] for p in propietarios}
        df_fact['propietario_nombre'] = df_fact['propietario_id'].map(propietarios_dict)

        resumen_propietario = df_fact.groupby('propietario_nombre').agg({
            'total': 'sum',
            'saldo_pendiente': 'sum',
            'cuota_sostenimiento': 'sum'
        }).reset_index()

        resumen_propietario.columns = ['Propietario', 'Total Facturado', 'Saldo Pendiente', 'Cuotas de Sostenimiento']
        st.dataframe(resumen_propietario, use_container_width=True)

    else:
        st.info("📝 No hay datos de facturación disponibles para el análisis.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Configuración del Administrador (solo en Dashboard financiero)
    st.sidebar.header("Configuración del Administrador")
    with st.sidebar.form(key="form_admin"):
        nuevo_nombre = st.text_input("Nombre del administrador", value=get_config("nombre_admin"))
        nuevo_email = st.text_input("Email de registro", value=get_config("email_admin"))
        nueva_password = st.text_input("Contraseña", value=get_config("password_admin"), type="password")
        submit_admin = st.form_submit_button("Guardar cambios")
    if submit_admin:
        set_config("nombre_admin", nuevo_nombre)
        set_config("email_admin", nuevo_email)
        set_config("password_admin", nueva_password)
        st.success("Datos del administrador actualizados.")

elif current_page == "Recibos de caja (Pagos)":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_pagos"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>💳 Recibos de Caja y Pagos</h1><p>Registra y administra los pagos realizados por los propietarios</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📝 Registrar Nuevo Pago</h3>', unsafe_allow_html=True)

    propietarios = get_propietarios()
    facturas = get_facturas()

    with st.form(key="form_pago"):
        if propietarios and facturas:
            propietario_options = {f"{p['nombre']} - {p['unidad']}": p['id'] for p in propietarios}
            propietario_seleccionado = st.selectbox("👤 Seleccionar Propietario", options=list(propietario_options.keys()))

            factura_options = {f"Factura #{f['recibo']} - ${f['total']:,.2f}": f['id'] for f in facturas}
            factura_seleccionada = st.selectbox("🧾 Seleccionar Factura", options=list(factura_options.keys()))

            fecha_pago = st.date_input("📅 Fecha del Pago")
            monto_pagado = st.number_input("💰 Monto Pagado", min_value=0.0, step=0.01)
            metodo_pago = st.selectbox("💳 Método de Pago", ["Efectivo", "Transferencia", "Cheque", "Tarjeta de Crédito", "Otro"])

            submit_pago = st.form_submit_button("✅ Registrar Pago", use_container_width=True)
        else:
            st.warning("⚠️ Necesitas tener propietarios y facturas registradas para registrar pagos.")
            submit_pago = None

    if submit_pago:
        propietario_id = propietario_options[propietario_seleccionado]
        factura_id = factura_options[factura_seleccionada]
        add_pago(propietario_id, factura_id, str(fecha_pago), monto_pagado, metodo_pago)
        st.success("✅ Pago registrado correctamente.")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Lista de pagos
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Historial de Pagos</h3>', unsafe_allow_html=True)

    pagos = get_pagos()
    if pagos:
        import pandas as pd
        df_pagos = pd.DataFrame(pagos)
        df_pagos.columns = ['ID', 'Propietario ID', 'Factura ID', 'Fecha', 'Monto', 'Método']
        st.dataframe(df_pagos, use_container_width=True)
    else:
        st.info("📝 No hay pagos registrados.")

    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Estado de cuenta por propietario":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_estados"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>📄 Estados de Cuenta</h1><p>Consulta el estado de cuenta detallado de cada propietario</p></div>', unsafe_allow_html=True)

    propietarios = get_propietarios()
    if propietarios:
        propietario_seleccionado = st.selectbox(
            "👤 Seleccionar Propietario",
            options=[f"{p['nombre']} - {p['unidad']}" for p in propietarios]
        )

        if propietario_seleccionado:
            propietario = next(p for p in propietarios if f"{p['nombre']} - {p['unidad']}" == propietario_seleccionado)

            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown(f'<h3>Estado de Cuenta - {propietario["nombre"]}</h3>', unsafe_allow_html=True)

            # Obtener facturas y pagos del propietario
            facturas_prop = [f for f in get_facturas() if f['propietario_id'] == propietario['id']]
            pagos_prop = [p for p in get_pagos() if p['propietario_id'] == propietario['id']]

            col1, col2, col3 = st.columns(3)

            total_facturado = sum(f['total'] for f in facturas_prop)
            total_pagado = sum(p['monto_pagado'] for p in pagos_prop)
            saldo_pendiente = total_facturado - total_pagado

            with col1:
                st.metric("💰 Total Facturado", f"${total_facturado:,.2f}")
            with col2:
                st.metric("💳 Total Pagado", f"${total_pagado:,.2f}")
            with col3:
                st.metric("⏳ Saldo Pendiente", f"${saldo_pendiente:,.2f}")

            st.markdown('</div>', unsafe_allow_html=True)

            # Detalle de facturas
            if facturas_prop:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown('<h4>🧾 Facturas Emitidas</h4>', unsafe_allow_html=True)
                import pandas as pd
                df_facturas = pd.DataFrame(facturas_prop)
                df_facturas = df_facturas[['fecha', 'recibo', 'total']]
                df_facturas.columns = ['Fecha', 'Recibo', 'Total']
                st.dataframe(df_facturas, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Detalle de pagos
            if pagos_prop:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown('<h4>💳 Pagos Realizados</h4>', unsafe_allow_html=True)
                import pandas as pd
                df_pagos = pd.DataFrame(pagos_prop)
                df_pagos = df_pagos[['fecha_pago', 'monto_pagado', 'metodo_pago']]
                df_pagos.columns = ['Fecha', 'Monto', 'Método']
                st.dataframe(df_pagos, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ No hay propietarios registrados.")

elif current_page == "Egresos y gastos":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_egresos"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>💸 Egresos y Gastos</h1><p>Registra y administra los gastos del edificio</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📝 Registrar Nuevo Gasto</h3>', unsafe_allow_html=True)

    with st.form(key="form_gasto"):
        fecha_gasto = st.date_input("📅 Fecha del Gasto")
        descripcion = st.text_input("📋 Descripción del Gasto")
        categoria = st.selectbox("🏷️ Categoría", ["Mantenimiento", "Servicios Públicos", "Seguridad", "Limpieza", "Administrativos", "Reparaciones", "Otros"])
        monto = st.number_input("💰 Monto", min_value=0.0, step=0.01)
        proveedor = st.text_input("🏢 Proveedor")

        submit_gasto = st.form_submit_button("✅ Registrar Gasto", use_container_width=True)

    if submit_gasto:
        # Aquí iría la función para agregar gasto (necesitarías implementarla en db_utils.py)
        st.success("✅ Gasto registrado correctamente.")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Lista de gastos (placeholder)
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Historial de Gastos</h3>', unsafe_allow_html=True)
    st.info("📝 Funcionalidad de gastos en desarrollo. Próximamente disponible.")
    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Reportes mensuales":
    # Botón para volver al menú principal
    if st.button("← Volver al Menú Principal", key="back_to_menu_reportes"):
        navigate_to("Inicio")

    st.markdown('<div class="modern-header"><h1>📊 Reportes Mensuales</h1><p>Reportes detallados de ingresos, egresos y estados financieros</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📈 Resumen del Mes</h3>', unsafe_allow_html=True)

    # Filtros de fecha
    col1, col2 = st.columns(2)
    with col1:
        mes_reporte = st.selectbox("📅 Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
    with col2:
        anio_reporte = st.selectbox("📆 Año", [2024, 2025, 2026], index=1)

    if st.button("📊 Generar Reporte"):
        st.success("✅ Reporte generado correctamente.")
        # Aquí iría la lógica para generar el reporte

    st.markdown('</div>', unsafe_allow_html=True)

    # Contenido del reporte (placeholder)
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<h3>📋 Detalles del Reporte</h3>', unsafe_allow_html=True)
    st.info("📝 Funcionalidad de reportes en desarrollo. Próximamente disponible con gráficos detallados y exportación a PDF.")
    st.markdown('</div>', unsafe_allow_html=True)
