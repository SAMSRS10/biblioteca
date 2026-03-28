# 📚 Sistema de Gestión Bibliotecaria Transaccional

Este proyecto es una solución robusta desarrollada en **Django**, diseñada para resolver la logística de una biblioteca moderna. Implementa un control estricto de inventario, un motor de préstamos con cálculo de penalizaciones y una interfaz inteligente que se transforma según el rol del usuario (**Staff o Lector**).

## 🧠 Ingeniería del Sistema

### 🛠️ Lógica de Backend (Core)
*   **Transacciones Seguras:** Uso de `select_for_update()` para garantizar la integridad de los datos y evitar la "doble reserva" de ejemplares en colisiones de milisegundos.
*   **Motor de Multas:** Algoritmo automático que calcula penalizaciones basadas en la fecha límite de devolución esperada.
*   **Enrutamiento Inteligente:** La ruta `/redireccionar/` actúa como un cerebro lógico que valida si el usuario es `is_staff` o `Lector` para entregar el panel correspondiente.

### 🎨 UX/UI y Frontend
*   **Arquitectura MVT:** Separación profesional entre Modelos (datos), Vistas (lógica) y Templates (interfaz).
*   **Herencia de Plantillas:** Uso de un `base.html` maestro para mantener consistencia visual en todo el sitio y reducir la duplicidad de código.
*   **Feedback en Tiempo Real:** Sistema de mensajería dinámico (`django.contrib.messages`) para notificar éxitos, errores o advertencias al usuario.

---

 ## 📂 Estructura del Repositorio
 ```text
 ├── config/             # Configuración global y rutas raíz (URLs)
 ├── catalog/            # Gestión de libros, autores y stock
 ├── loans/              # Motor de préstamos, estados y transacciones
 ├── users/              # Registro, perfiles y permisos de acceso
 ├── templates/          # Pantallas globales y componentes reutilizables
 └── static/             # Estilos CSS modernos y assets visuales
 ```

# 🚀 Guía de Instalación (Paso a Paso)

Sigue estos pasos para replicar el entorno de desarrollo desde cero:

## 1. Preparar el Entorno Virtual
Esto crea un espacio aislado para que el proyecto funcione correctamente.

**Windows (PowerShell):**
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
**macOS / Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
```
# 2. Sincronización de Dependencias
Una vez activado el entorno, instalamos Django:
```
pip install --upgrade pip
pip install django
```
# 3. Construcción de la Base de Datos
Prepara las tablas donde se guardarán los libros y usuarios:
```
python manage.py makemigrations
python manage.py migrate
```
# 4. Crear Cuenta de Administrador (Staff)
Necesaria para gestionar la biblioteca y aprobar préstamos:
```
python manage.py createsuperuser
```
# 5. Inicializar el Servidor
```
python manage.py runserver
```
📍 Acceso Local: http://127.0.0.1:8000

# 📖 Guía de Uso del Sistema
## 👤 Rol: Lector (Usuario General)
Explorar el Catálogo: Revisa libros disponibles con búsqueda por nombre o autor.
Detalle de Libros: Consulta información específica (ISBN) y el estado del último préstamo.
Mis Préstamos: Panel para ver libros en tu poder y fechas de entrega esperadas.
## 👨‍💼 Rol: Staff (Administrador)
Gestión de Catálogo: Acceso a formularios para editar datos de libros o eliminarlos.
Gestión de Préstamos: Aprueba solicitudes y recibe devoluciones. El sistema calcula automáticamente las multas si existen retrasos.

# ❄️ Solución para Equipos con Congelador (DeepFreeze)
Si trabajas en computadoras de laboratorio que borran todo al reiniciar, sigue estas reglas para no perder tu progreso:
## 📍 Ubicación Crítica: 
Guarda siempre tu carpeta de proyecto en una USB o en la partición D: del disco duro. No uses el Escritorio ni Descargas.
## 📂 El archivo Sagrado:
El archivo db.sqlite3 es el que contiene todos tus libros y usuarios creados. Asegúrate de que esté siempre dentro de tu carpeta en la unidad persistente (USB/Disco D).
## ⚡ Recuperación de Entorno: 
Si al encender la PC el entorno virtual .venv no funciona o desapareció, solo repite los pasos de creación y activación del entorno virtual. Tu código y tus datos (libros) seguirán ahí.

## 🛠️ Solución de Errores Comunes


| Error | Solución |
| :--- | :--- |
| **"Scripts deshabilitados"** (Windows) | Abre PowerShell como administrador y ejecuta: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| **"Python no se reconoce"** | Asegúrate de haber marcado la casilla "Add Python to PATH" al instalar Python o reinstálalo marcándola. |
| **TemplateDoesNotExist** | Revisa que la carpeta `templates/` esté en la raíz y que en `settings.py` esté configurado `BASE_DIR / 'templates'`. |
| **Port 8000 already in use** | El servidor ya se está ejecutando en otra ventana o proceso. Ciérralo o usa `python manage.py runserver 8001`. |
| **Static files not loading** | Verifica que tengas `{% load static %}` al inicio de tu archivo HTML y `STATIC_URL` configurado en settings. |
