# 📚 Sistema de Gestión Académica - Django

## 🎯 Descripción del Proyecto

Este proyecto es un **Sistema de Gestión Académica** desarrollado en Django que permite administrar carreras, materias, alumnos, usuarios e inscripciones de una institución educativa. El sistema implementa principios de **Programación Orientada a Objetos (POO)**, separación de capas, y un sistema de roles robusto.

## 🏗️ Arquitectura del Sistema

### Principios Aplicados
- **Herencia**: Clase abstracta `Persona` heredada por `Alumno`
- **Encapsulamiento**: Lógica de negocio separada en servicios
- **Abstracción**: Modelos con validaciones y métodos específicos
- **Separación de Responsabilidades**: Modelos, Servicios, Vistas, Forms y Templates

### Estructura del Proyecto
```
demo/
├── demo/                           # Configuración del proyecto
│   ├── settings.py                 # Configuración Django
│   ├── urls.py                     # URLs principales
│   └── wsgi.py
├── gestion_academica/              # App principal
│   ├── models.py                   # Modelos de datos
│   ├── services.py                 # Lógica de negocio
│   ├── forms.py                    # Formularios y validaciones
│   ├── views.py                    # Vistas (controladores)
│   ├── urls.py                     # URLs de la app
│   ├── management/commands/        # Comandos personalizados
│   │   └── cargar_datos_iniciales.py
│   └── templates/gestion_academica/ # Templates HTML
│       ├── base.html
│       ├── dashboard.html
│       ├── auth/                   # Autenticación
│       ├── carreras/               # CRUD Carreras
│       ├── materias/               # CRUD Materias
│       ├── alumnos/                # CRUD Alumnos
│       ├── usuarios/               # CRUD Usuarios
│       ├── inscripciones/          # CRUD Inscripciones
│       ├── alumno/                 # Vistas específicas de alumno
│       └── publico/                # Vistas públicas (invitados)
├── requirements.txt                # Dependencias
├── README.md                       # Instrucciones básicas
├── CHECKLIST_REQUISITOS.md         # Lista de verificación
└── DOCUMENTACION_PROYECTO.md       # Esta documentación
```

## 🗄️ Modelo de Datos

### Diagrama de Entidades
```
Persona (Abstracta)
    ↓
Usuario (hereda atributos base)
    ↓
Alumno (hereda de Persona + relación Usuario)
    ↓
Inscripcion ← → Materia → Carrera
```

### Entidades Principales

#### 1. **Persona** (Clase Abstracta)
```python
- username (DNI - 8 dígitos)
- nombre
- apellido  
- email (único)
- telefono
- fecha_nacimiento
- fecha_creacion/modificacion
```

#### 2. **Usuario** (hereda de AbstractUser)
```python
- rol: [administrador, alumno, invitado]
- primer_login (booleano)
- relación OneToOne con Alumno
```

#### 3. **Carrera**
```python
- nombre (único)
- codigo (formato: AA1234)
- descripcion
- duracion_años (1-10)
- activa
```

#### 4. **Materia**
```python
- nombre
- codigo (formato: ABC123)
- carrera (FK)
- año (1-6)
- cuatrimestre (1-2)
- cupo_maximo
- descripcion
```

#### 5. **Alumno** (hereda de Persona)
```python
- legajo (único, 4-10 dígitos)
- carrera (FK)
- usuario (OneToOne)
- año_ingreso (2000-2030)
- activo
```

#### 6. **Inscripcion** (Tabla Intermedia)
```python
- alumno (FK)
- materia (FK)
- fecha_inscripcion
- activa
- nota (opcional)
```

## 🔐 Sistema de Autenticación y Roles

### Roles Implementados

#### 🔧 **Administrador**
- **Permisos**: CRUD completo sobre todas las entidades
- **Funcionalidades**:
  - Gestionar carreras, materias, alumnos, usuarios
  - Ver todas las inscripciones
  - Acceso a reportes y estadísticas
  - Dashboard con resumen del sistema

#### 👨‍🎓 **Alumno**
- **Permisos**: Lectura y gestión de sus propios datos
- **Funcionalidades**:
  - Ver sus materias inscritas
  - Consultar oferta académica de su carrera
  - Inscribirse/darse de baja de materias (con validaciones)
  - Cambiar contraseña
  - Dashboard personalizado

#### 👤 **Invitado**
- **Permisos**: Solo lectura de información pública
- **Funcionalidades**:
  - Consultar carreras disponibles
  - Ver materias por carrera
  - Consultar materias con cupo disponible
  - Acceso a estadísticas generales

### Autenticación
- **Login**: Email o DNI + contraseña
- **Contraseña inicial**: DNI del usuario
- **Primer login**: Obligatorio cambio de contraseña
- **Sesiones**: Manejo de roles y permisos

## 💼 Lógica de Negocio (Servicios)

### CarreraService
```python
- crear_carrera(datos)
- actualizar_carrera(carrera, datos)
- eliminar_carrera(carrera_id)
- obtener_estadisticas_carrera(carrera)
- buscar_carreras(filtros)
```

### MateriaService
```python
- crear_materia(datos)
- actualizar_materia(materia, datos)
- eliminar_materia(materia_id)
- materias_por_carrera(carrera)
- materias_con_cupo()
- validar_cupo_disponible(materia)
```

### AlumnoService
```python
- crear_alumno(datos)
- actualizar_alumno(alumno, datos)
- eliminar_alumno(alumno_id)
- buscar_alumnos(filtros)
- obtener_materias_alumno(alumno)
```

### InscripcionService
```python
- inscribir_alumno(alumno, materia)
- dar_de_baja(inscripcion_id)
- validar_inscripcion(alumno, materia)
- obtener_inscripciones_activas(alumno)
```

## 🎨 Interface de Usuario

### Características del Frontend
- **HTML Puro**: Sin frameworks CSS (Bootstrap, etc.)
- **Responsive**: Adaptable a diferentes pantallas
- **Navegación por Roles**: Menús dinámicos según permisos
- **Formularios Validados**: Feedback en tiempo real
- **Mensajes**: Sistema de notificaciones (éxito/error)

### Templates Principales

#### Base Template
```html
- Estructura común (header, nav, content, footer)
- Navegación dinámica por rol
- Sistema de mensajes
- Enlaces contextuales
```

#### Dashboard
```html
- Panel de control personalizado por rol
- Estadísticas relevantes
- Accesos rápidos
- Información del usuario
```

#### CRUD Templates
```html
- List: Listado con filtros y paginación
- Form: Formulario create/edit con validaciones
- Confirm Delete: Confirmación de eliminación
- Detail: Vista detallada (para consultas)
```

## 🔍 Funcionalidades Avanzadas

### Filtros y Consultas
1. **Materias por Carrera**: Filtrado dinámico
2. **Alumnos por Materia**: Con información de inscripción
3. **Materias con Cupo**: Disponibilidad en tiempo real
4. **Estadísticas por Carrera**: Reportes automáticos

### Validaciones Implementadas
- **DNI**: 8 dígitos únicos
- **Email**: Formato válido y único
- **Códigos**: Formatos específicos (carreras/materias)
- **Cupos**: Validación antes de inscripción
- **Fechas**: Rangos lógicos
- **Teléfonos**: Formato internacional

### Características de Seguridad
- **Protección CSRF**: Tokens en formularios
- **Validación de Roles**: Decoradores y mixins
- **Sanitización**: Limpieza de datos de entrada
- **Sesiones Seguras**: Configuración Django

## 📊 Datos de Ejemplo

### Carreras Precargadas
1. **Técnico Superior en Programación** (TSP2024)
2. **Técnico Superior en Análisis de Sistemas** (TSAS2024)
3. **Técnico Superior en Redes y Comunicaciones** (TSRC2024)

### Usuarios de Prueba
```
Administrador:
- Email: admin@crui.edu.ar
- Contraseña: admin123

Invitado:
- Email: invitado@ejemplo.com  
- Contraseña: 87654321

Alumnos (4 usuarios):
- juan.gonzalez@estudiante.crui.edu.ar / 20123456
- maria.rodriguez@estudiante.crui.edu.ar / 20234567
- carlos.fernandez@estudiante.crui.edu.ar / 20345678
- ana.lopez@estudiante.crui.edu.ar / 20456789
```

## 🚀 Instalación y Configuración

### Requisitos Previos
```bash
Python 3.8+
Django 4.x+
SQLite (incluido)
```

### Pasos de Instalación
```bash
1. Clonar/descargar el proyecto
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py cargar_datos_iniciales
6. python manage.py runserver
```

### Configuración Inicial
```python
# settings.py destacados
- LANGUAGE_CODE = 'es-ar'
- TIME_ZONE = 'America/Argentina/Buenos_Aires'
- AUTH_USER_MODEL = 'gestion_academica.Usuario'
- LOGIN_URL = '/auth/login/'
- LOGIN_REDIRECT_URL = '/'
```

## 🔧 Comandos Personalizados

### cargar_datos_iniciales
```bash
# Cargar datos de ejemplo
python manage.py cargar_datos_iniciales

# Resetear y cargar datos limpios
python manage.py cargar_datos_iniciales --reset
```

Este comando crea:
- Usuarios de prueba con diferentes roles
- Carreras con materias asociadas
- Alumnos con inscripciones de ejemplo
- Datos realistas para testing

## 📱 Recorrido por la Aplicación

### 1. **Página de Inicio**
- Dashboard adaptativo según rol del usuario
- Estadísticas generales del sistema
- Enlaces rápidos a funcionalidades principales

### 2. **Autenticación**
- Login con email o DNI
- Primer login obliga cambio de contraseña
- Logout seguro con limpieza de sesión

### 3. **Panel de Administrador**
- CRUD completo de todas las entidades
- Gestión de usuarios y roles
- Reportes y estadísticas avanzadas
- Consultas por carrera y materia

### 4. **Panel de Alumno**
- Vista de materias propias
- Oferta académica de su carrera
- Inscripción/baja de materias
- Información personal editable

### 5. **Vista Pública (Invitados)**
- Carreras disponibles
- Materias por carrera
- Materias con cupo disponible
- Estadísticas generales sin datos sensibles

## 🏆 Características Destacadas

### ✅ **Cumplimiento de Requisitos**
- **POO**: Herencia, encapsulamiento, abstracción
- **Separación de Capas**: Modelos → Servicios → Vistas → Templates
- **Autenticación Robusta**: Roles y permisos granulares
- **CRUD Completo**: Todas las entidades gestionables
- **Validaciones**: En modelos, forms y servicios
- **Datos de Prueba**: Comando para carga automática

### ✅ **Buenas Prácticas**
- **Código Limpio**: Comentarios y documentación
- **Nomenclatura Consistente**: Español, convenciones Django
- **Manejo de Errores**: Try/catch y validaciones
- **Optimización**: Queries eficientes, select_related
- **Seguridad**: Validación de entrada, protección CSRF

### ✅ **Extensibilidad**
- **Modular**: Fácil agregar nuevas entidades
- **Configurable**: Settings centralizados
- **Escalable**: Estructura preparada para crecimiento
- **Mantenible**: Código documentado y organizado

## 🔮 Posibles Mejoras Futuras

### Funcionalidades
- **Sistema de Notas**: Calificaciones y promedios
- **Calendario Académico**: Fechas importantes
- **Reportes PDF**: Exports automáticos
- **Notificaciones**: Email/SMS para eventos
- **API REST**: Para integración con otros sistemas

### Tecnológicas
- **Base de Datos**: PostgreSQL para producción
- **Cache**: Redis para optimización
- **Frontend**: React/Vue para SPA
- **Deployment**: Docker + CI/CD
- **Monitoring**: Logs y métricas

---

## 📞 Soporte y Contacto

Este proyecto fue desarrollado como sistema académico completo, implementando todas las mejores prácticas de desarrollo Django y patrones de diseño de software.

**Documentación adicional:**
- `README.md`: Instrucciones rápidas de uso
- `CHECKLIST_REQUISITOS.md`: Verificación de cumplimiento
- Comentarios en código: Explicaciones técnicas detalladas

---

*Sistema de Gestión Académica - Desarrollado con Django 4.x y Python 3.8+*
