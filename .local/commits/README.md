# Tutorial de Desarrollo: Sistema de Gestión Académica

## Descripción del Proyecto

Este tutorial presenta el desarrollo paso a paso de un **Sistema de Gestión Académica** para instituciones educativas, implementado con Django. El sistema permite gestionar usuarios, carreras, materias, alumnos e inscripciones de forma integral.

## Características del Sistema

El sistema desarrollado incluye las siguientes funcionalidades:

- **🔐 Sistema de Autenticación Personalizado**: Login con email, cambio de contraseña obligatorio en primer acceso
- **👥 Gestión de Usuarios**: Roles diferenciados (administrador, alumno, invitado)
- **🎓 Gestión de Carreras**: CRUD completo con validaciones de negocio
- **📚 Gestión de Materias**: Control de cupos, organización por años y cuatrimestres
- **🎒 Gestión de Alumnos**: Registro completo con legajos únicos
- **📝 Sistema de Inscripciones**: Control automático de cupos y validaciones cruzadas
- **📊 Dashboard**: Información específica según el rol del usuario
- **🌐 Vistas Públicas**: Consulta de carreras y materias sin autenticación
- **⚙️ Comandos de Gestión**: Carga automática de datos iniciales

## Equipo de Desarrollo

El desarrollo se distribuye entre **5 integrantes**, cada uno responsable de commits específicos:

- **Santiago** - Inicialización, modelos core y validaciones finales
- **Jorge** - Apps de usuario y materia, servicios especializados  
- **Paula** - Autenticación, alumnos y dashboard
- **Lourdes** - Carreras, CRUD de alumnos y vistas públicas
- **Daiana** - CRUD de carreras, inscripciones y comandos de gestión

## Arquitectura del Sistema

### Aplicaciones Django
- `usuario` - Modelo de usuario personalizado con roles
- `carrera` - Gestión de carreras académicas
- `materia` - Materias por carrera con control de cupos
- `alumno` - Datos específicos de estudiantes
- `inscripcion` - Relación alumnos-materias con validaciones
- `gestion_academica` - App central con dashboard y vistas públicas

### Patrón de Diseño
- **Modelos**: Definición de entidades y validaciones de negocio
- **Servicios**: Lógica de negocio compleja y operaciones transversales
- **Formularios**: Validaciones de entrada y widgets personalizados
- **Vistas**: CBVs (Class Based Views) con mixins de autorización
- **Templates**: Jerarquía con template base y vistas especializadas

## Cómo Usar Este Tutorial

### 1. Orden de Commits
Los commits están numerados del 01 al 16 y deben seguirse **secuencialmente**. Cada commit incluye:
- Responsable del desarrollo
- Descripción de tareas
- Comandos específicos a ejecutar
- Archivos a crear o modificar
- Resultado esperado

### 2. Estructura de Cada Commit
```
commit-XX.md
├── Responsable: [Nombre del desarrollador]
├── Descripción: [Explicación de la funcionalidad]
├── Tareas a realizar: [Pasos detallados]
├── Archivos a crear/modificar: [Lista de archivos]
└── Resultado esperado: [Validación del commit]
```

### 3. Comandos Iniciales
Antes de comenzar, asegúrate de tener:
```bash
# Python 3.8+ instalado
# Django 4.x+
pip install django
pip install django-widget-tweaks
```

### 4. Validación por Commit
Después de cada commit, verifica que el resultado esperado se cumple antes de continuar al siguiente.

## Flujo de Desarrollo Recomendado

1. **Commits 01-03**: Base del proyecto con autenticación
2. **Commits 04-07**: Módulos de carreras y materias
3. **Commits 08-11**: Módulos de alumnos e inscripciones  
4. **Commits 12-14**: Dashboard y funcionalidades transversales
5. **Commits 15-16**: Datos iniciales y testing

## Comandos Útiles Durante el Desarrollo

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones  
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos iniciales
python manage.py crear_grupos
python manage.py cargar_datos_iniciales

# Ejecutar servidor
python manage.py runserver

# Ejecutar tests
python manage.py test
```

## Tecnologías y Dependencias

- **Framework**: Django 5.2+
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción recomendada)
- **Frontend**: HTML5 + CSS3 (sin frameworks JS)
- **Formularios**: django-widget-tweaks para styling
- **Autenticación**: Sistema personalizado basado en AbstractUser

## Resultados de Aprendizaje

Al completar este tutorial, habrás aprendido:

- ✅ Configuración avanzada de proyectos Django
- ✅ Modelos personalizados con validaciones complejas
- ✅ Sistema de autenticación y autorización robusto
- ✅ Patrón de servicios para lógica de negocio
- ✅ Vistas basadas en clases con mixins
- ✅ Formularios Django con validaciones personalizadas
- ✅ Comandos de gestión personalizados
- ✅ Tests unitarios y de integración
- ✅ Buenas prácticas de desarrollo en equipo

---

**¡Comienza con el commit-01.md y desarrolla tu sistema de gestión académica paso a paso!**