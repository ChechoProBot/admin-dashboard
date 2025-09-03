import streamlit as st
import time

# Configuración de la página
st.set_page_config(
    page_title="APPADMI - Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Verificar si ya está autenticado
if st.session_state.get("logged_in", False):
    st.success("Ya estás autenticado.")
    st.info("Redirigiendo a la aplicación principal...")
    time.sleep(1)
    # Redirigir automáticamente usando JavaScript
    st.markdown("""
        <script>
            window.location.href = window.location.origin;
        </script>
    """, unsafe_allow_html=True)
    st.stop()  # Detener ejecución para evitar mostrar el formulario de login

# Estilos CSS personalizados
st.markdown("""
<style>
/* Estilos generales */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    margin: 0;
    padding: 0;
}

/* Contenedor principal */
.login-container {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin: 2rem auto;
    max-width: 400px;
}

/* Título */
.login-title {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 2rem;
    font-size: 2.5em;
    font-weight: bold;
}

/* Logo o ícono */
.login-icon {
    text-align: center;
    font-size: 4em;
    margin-bottom: 1rem;
}

/* Campos de entrada */
.stTextInput input {
    border-radius: 8px;
    border: 2px solid #e1e5e9;
    padding: 0.75rem;
    font-size: 1em;
    width: 100%;
    box-sizing: border-box;
}

.stTextInput input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* Botones */
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-size: 1em;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Pestañas */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 6px;
    color: #666;
    font-weight: 500;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #667eea;
    color: white;
}

/* Mensajes de éxito y error */
.success-message {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #c3e6cb;
    margin: 1rem 0;
}

.error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #f5c6cb;
    margin: 1rem 0;
}

/* Footer */
.footer {
    text-align: center;
    color: #666;
    font-size: 0.9em;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Función para verificar credenciales
def verificar_credenciales(email, password):
    # Credenciales por defecto para demo
    admin_email = "admin@appadmi.com"
    admin_password = "admin123"

    # Verificar si las credenciales coinciden
    if email == admin_email and password == admin_password:
        return True, "Administrador"
    else:
        return False, None

# Función para registrar nuevo usuario
def registrar_usuario(email, password, nombre):
    # En una aplicación real, aquí guardarías en la base de datos
    # Por ahora, solo simulamos el registro
    st.session_state["user_email"] = email
    st.session_state["user_password"] = password
    st.session_state["user_name"] = nombre
    return True

# Título principal
st.markdown('<div class="login-icon">🔐</div>', unsafe_allow_html=True)
st.markdown('<h1 class="login-title">APPADMI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Sistema de Administración de Propiedades</p>', unsafe_allow_html=True)

# Crear pestañas para Login y Registro
tab1, tab2, tab3 = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse", "🔄 Recuperar Contraseña"])

# Pestaña de Login
with tab1:
    st.markdown("### Iniciar Sesión")

    with st.form("login_form"):
        email = st.text_input("Correo electrónico", placeholder="admin@appadmi.com")
        password = st.text_input("Contraseña", type="password", placeholder="admin123")
        remember_me = st.checkbox("Recordarme", key="login_remember_checkbox")

        submitted = st.form_submit_button("🚀 Iniciar Sesión")

        if submitted:
            if not email or not password:
                st.error("Por favor, complete todos los campos.")
            else:
                # Verificar credenciales
                login_success, user_role = verificar_credenciales(email, password)

                if login_success:
                    # Guardar información en la sesión
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_role"] = user_role

                    st.success(f"¡Bienvenido, {user_role}!")

                    # Pequeña pausa antes de redirigir
                    time.sleep(1)

                    # Establecer estado de login
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_role"] = user_role

                    # Redirigir automáticamente usando JavaScript
                    st.success("¡Login exitoso! Redirigiendo...")
                    st.markdown("""
                        <script>
                            setTimeout(function(){
                                window.location.href = window.location.origin;
                            }, 1500);
                        </script>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Credenciales incorrectas. Intente nuevamente.")

# Pestaña de Registro
with tab2:
    st.markdown("### Crear Nueva Cuenta")

    with st.form("register_form"):
        nombre = st.text_input("Nombre completo", placeholder="Juan Pérez")
        email_reg = st.text_input("Correo electrónico", placeholder="juan@email.com")
        password_reg = st.text_input("Contraseña", type="password", placeholder="Mínimo 6 caracteres")
        password_confirm = st.text_input("Confirmar contraseña", type="password")

        submitted_reg = st.form_submit_button("📝 Crear Cuenta")

        if submitted_reg:
            if not nombre or not email_reg or not password_reg or not password_confirm:
                st.error("Por favor, complete todos los campos.")
            elif password_reg != password_confirm:
                st.error("Las contraseñas no coinciden.")
            elif len(password_reg) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                # Registrar usuario
                if registrar_usuario(email_reg, password_reg, nombre):
                    st.success("¡Cuenta creada exitosamente!")
                    st.info("Ahora puede iniciar sesión con sus credenciales.")
                else:
                    st.error("Error al crear la cuenta. Intente nuevamente.")

# Pestaña de Recuperación de Contraseña
with tab3:
    st.markdown("### Recuperar Contraseña")

    with st.form("recovery_form"):
        email_recovery = st.text_input("Correo electrónico registrado", placeholder="tu@email.com")

        submitted_recovery = st.form_submit_button("📧 Enviar Instrucciones")

        if submitted_recovery:
            if not email_recovery:
                st.error("Por favor, ingrese su correo electrónico.")
            else:
                # Simular envío de email de recuperación
                st.success("¡Instrucciones enviadas!")
                st.info("Se ha enviado un enlace de recuperación a su correo electrónico.")

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 APPADMI - Sistema de Administración de Propiedades</p>
    <p>Versión 1.0.0</p>
</div>
""", unsafe_allow_html=True)

# Información adicional
with st.expander("ℹ️ Información del Sistema"):
    st.markdown("""
    **Credenciales de prueba:**
    - **Email:** admin@appadmi.com
    - **Contraseña:** admin123

    **Características:**
    - 🔐 Autenticación segura
    - 📊 Dashboard administrativo
    - 🏢 Gestión de propiedades
    - 👥 Administración de propietarios
    - 💰 Control financiero
    """)
