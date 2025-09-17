# Sistema de Gestión Académica

Sistema web desarrollado en Django para la gestión académica de instituciones educativas.

## Características

- **Gestión de Usuarios**: Sistema de autenticación con roles diferenciados
- **Gestión de Carreras**: CRUD completo para carreras académicas
- **Gestión de Materias**: CRUD completo para materias por carrera
- **Gestión de Alumnos**: CRUD completo para alumnos
- **Sistema de Inscripciones**: Inscripción y baja de alumnos en materias
- **Control de Cupos**: Validación automática de cupos disponibles
- **Filtros y Consultas**: Búsquedas por carrera, materia y alumno
- **Roles de Usuario**: Administrador, Alumno, Invitado

## Tecnologías

- **Python 3.8+**
- **Django 4.x**
- **SQLite** (base de datos por defecto)
- **HTML puro** (sin frameworks CSS)

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/santiagoarielv98/sistema-gestion-academica.git
cd sistema-gestion-academica
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. (Opcional) Crear superusuario (administrador principal)
```bash
python manage.py createsuperuser
```

### 6. Cargar Grupos y Permisos Iniciales (Obligatorio)
```bash
python manage.py crear_grupos
```

### 7. Cargar datos de ejemplo (Recomendado)
```bash
python manage.py cargar_datos_iniciales
```

### 8. Ejecutar el servidor
```bash
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/

## Usuarios de Prueba

Después de ejecutar `cargar_datos_iniciales`:

- **Administrador**: admin@crui.edu.ar / admin123
- **Invitado**: invitado@ejemplo.com / 87654321 TODO: quitar grupo invitado, y permitir acceso sin login
- **Alumnos**: usar email del alumno / contraseña: su DNI

## Estructura del Proyecto

```
demo/
├── demo/                          # Configuración principal
├── gestion_academica/             # Aplicación principal
│   ├── models.py                  # Modelos de datos
│   ├── views.py                   # Vistas
│   ├── forms.py                   # Formularios
│   ├── services.py                # Lógica de negocio
│   ├── urls.py                    # URLs de la app
│   └── templates/                 # Plantillas HTML
├── manage.py                      # Script de gestión
└── requirements.txt               # Dependencias
```

## Funcionalidades por Rol

### Administrador
- CRUD completo de carreras, materias, alumnos y usuarios
- Gestión de inscripciones
- Acceso a reportes y estadísticas
- Control total del sistema

### Alumno
- Ver sus materias inscriptas
- Inscribirse a materias de su carrera
- Darse de baja de materias
- Ver oferta académica

### Invitado
- Consultar carreras disponibles
- Ver materias por carrera
- Acceso de solo lectura

## Validaciones Implementadas

- **Unicidad**: DNI, email, legajo, códigos de carrera/materia
- **Integridad referencial**: No eliminar con relaciones activas
- **Cupos**: Control automático de cupos disponibles
- **Carreras**: Materias solo de la carrera del alumno
- **Duplicados**: Prevención de inscripciones duplicadas

## Consultas Disponibles

1. **Materias por Carrera**: Filtrar materias de una carrera específica
2. **Alumnos por Materia**: Ver alumnos inscritos en una materia
3. **Materias con Cupo**: Listar materias con cupo disponible

## Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
python manage.py cargar_datos_iniciales

# Cargar datos limpiando anteriores
python manage.py cargar_datos_iniciales --reset

# Ejecutar servidor
python manage.py runserver
```

## Arquitectura

El proyecto implementa una **arquitectura en capas**:

- **Modelos**: Definición de datos y validaciones
- **Servicios**: Lógica de negocio
- **Formularios**: Validaciones y presentación
- **Vistas**: Control de flujo
- **Templates**: Presentación HTML

## Principios POO Implementados

- **Herencia**: Clase abstracta `Persona` para `Alumno`
- **Encapsulamiento**: Propiedades y métodos privados
- **Abstracción**: Servicios para lógica de negocio
- **Polimorfismo**: Métodos sobrescritos en modelos

## Desarrollo

Para continuar el desarrollo:

1. Las vistas están organizadas por funcionalidad
2. Los servicios contienen la lógica de negocio
3. Los formularios incluyen validaciones completas
4. Los templates son HTML puro (sin estilos)

## Soporte

Para consultas sobre el sistema, contactar al equipo de desarrollo.