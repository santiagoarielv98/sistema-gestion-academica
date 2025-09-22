# Commit 15: Comandos de Gestión y Datos Iniciales

## Responsable: Daiana

### Descripción
Crear comandos de gestión de Django para inicializar datos y configurar grupos de usuarios automáticamente.

### Tareas a realizar

#### 1. Crear estructura de comandos
- Crear directorio `gestion_academica/management/`
- Crear directorio `gestion_academica/management/commands/`
- Crear archivos `__init__.py` en ambos directorios

#### 2. Implementar comando de datos iniciales
- Crear `cargar_datos_iniciales.py` en commands/
- Cargar carreras de ejemplo:
  - Ingeniería en Sistemas (ISYS2024)
  - Licenciatura en Administración (LADM2024)
  - Contador Público (CONT2024)
- Cargar materias por carrera con diferentes años y cuatrimestres
- Crear usuario administrador por defecto

#### 3. Implementar comando de grupos
- Crear `crear_grupos.py` en commands/
- Crear grupos: 'administradores', 'alumnos', 'invitados'
- Configurar permisos básicos por grupo
- Método para asignar usuarios a grupos automáticamente

#### 4. Crear datos de prueba opcionales
- Alumnos de ejemplo con diferentes carreras
- Inscripciones de prueba respetando cupos
- Validar integridad de datos

#### 5. Documentar comandos
- Instrucciones de uso en comentarios
- Manejo de errores y validaciones
- Opción de limpiar datos existentes

### Archivos a crear
- `gestion_academica/management/__init__.py`
- `gestion_academica/management/commands/__init__.py`
- `gestion_academica/management/commands/cargar_datos_iniciales.py`
- `gestion_academica/management/commands/crear_grupos.py`

### Comandos para ejecutar después
```bash
python manage.py crear_grupos
python manage.py cargar_datos_iniciales
```

### Resultado esperado
Comandos funcionales que permiten inicializar el sistema con datos de prueba y configurar grupos de usuarios automáticamente.