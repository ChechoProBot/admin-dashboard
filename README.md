# 🏢 AppADMI - Sistema de Administración de Propiedades

Un sistema completo de administración de propiedades horizontales desarrollado con Streamlit, SQLite y Python.

## 📋 Características Principales

### ✅ Funcionalidades Implementadas
- **🔐 Sistema de Autenticación**: Login seguro con sesiones
- **🏢 Gestión de Propiedades**: Registro y administración de edificios/conjuntos
- **🏠 Administración de Unidades**: Control de apartamentos/casas con coeficientes
- **👥 Gestión de Propietarios**: Base de datos completa de residentes
- **💰 Sistema de Facturación**: Generación automática de recibos y facturas
- **📊 Dashboard Financiero**: Análisis y visualización de datos financieros
- **📈 Estados de Cuenta**: Consulta detallada por propietario
- **⚙️ Configuración Avanzada**: Porcentajes globales y coeficientes por unidad

### 🎨 Interfaz Moderna
- Diseño responsivo con CSS moderno
- Tema profesional con gradientes y sombras
- Navegación intuitiva con menú lateral inteligente
- Gráficos interactivos con Matplotlib
- Tablas dinámicas con Pandas

## 🚀 Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Base de Datos**: SQLite
- **Visualización**: Matplotlib, Pandas
- **Estilos**: CSS con variables modernas
- **Control de Versiones**: Git

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Paso a Paso

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/ChechoProBot/admin-dashboard.git
   cd admin-dashboard
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   streamlit run frontend/app.py
   ```

## 🗂️ Estructura del Proyecto

```
admin-dashboard/
├── frontend/
│   ├── app.py              # Aplicación principal
│   ├── pages/
│   │   └── login.py        # Página de login
│   └── styles.css          # Estilos CSS modernos
├── backend/
│   ├── db_utils.py         # Utilidades de base de datos
│   └── db_init.py          # Inicialización de BD
├── data/                   # Archivos de base de datos (generados)
├── .gitignore             # Archivos ignorados por git
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🗄️ Base de Datos

El sistema utiliza SQLite con las siguientes tablas principales:

- **propiedades**: Información de edificios/conjuntos
- **unidades**: Apartamentos/casas con coeficientes
- **propietarios**: Datos de residentes
- **facturas**: Historial de facturación
- **pagos**: Registro de pagos realizados

## 🎯 Uso del Sistema

### Primeros Pasos
1. **Registro de Administrador**: Crear cuenta de administrador
2. **Configuración Inicial**: Establecer porcentajes globales
3. **Registro de Propiedad**: Agregar el edificio/conjunto
4. **Crear Unidades**: Registrar apartamentos con coeficientes
5. **Agregar Propietarios**: Vincular residentes a unidades
6. **Generar Facturas**: Sistema automático de facturación

### Funcionalidades Avanzadas
- **Coeficientes por Unidad**: Distribución personalizada de gastos
- **Dashboard Financiero**: Análisis completo con gráficos
- **Estados de Cuenta**: Consulta detallada por propietario
- **Reportes**: Generación automática de informes

## 🔧 Configuración

### Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# Configuración de base de datos
DATABASE_URL=sqlite:///data/appadmi.db

# Configuración de email (opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-password
```

### Personalización de Estilos
Los estilos se pueden modificar en `frontend/styles.css`:
- Variables CSS para colores y temas
- Clases responsivas para diferentes dispositivos
- Animaciones y transiciones

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- 📧 Email: soporte@appadmi.com
- 🐛 Reportar issues en GitHub
- 📖 Documentación completa en desarrollo

## 🔄 Actualizaciones Automáticas

El proyecto está configurado con GitHub Actions para:
- ✅ Tests automáticos en cada push
- ✅ Verificación de código con linting
- ✅ Despliegue automático (próximamente)
- ✅ Generación de documentación

---

**Desarrollado con ❤️ por ChechoProBot**

*Sistema profesional de administración de propiedades para copropiedades y conjuntos residenciales.*
