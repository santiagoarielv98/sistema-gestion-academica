# Commit 08: Creación de la App Alumno

## Responsable: Paula

### Descripción
Crear la aplicación `alumno` para gestionar los datos específicos de estudiantes usando composición con el modelo Usuario.

### Tareas a realizar

#### 1. Crear la app alumno
```bash
python manage.py startapp alumno
```

#### 2. Implementar modelo Alumno
- Crear clase `Alumno` con relación OneToOne a Usuario
- Campos específicos:
  - `usuario` (OneToOneField a Usuario)
  - `legajo` (CharField único con validación 4-10 dígitos)
  - `carrera` (ForeignKey a Carrera)
  - `año_ingreso` (PositiveIntegerField 2000-2030)
  - `activo` (BooleanField)
- Implementar propiedades `nombre_completo`, `email`, `dni`
- Implementar método `clean()` para validaciones
- Configurar Meta con ordering

#### 3. Crear señal para manejo automático
- Implementar señal `post_save` en Usuario para gestión de grupos
- Asignar automáticamente grupo "alumnos" cuando se crea un Alumno

#### 4. Configurar en settings.py
- Agregar `'alumno'` a `INSTALLED_APPS`

#### 5. Crear y aplicar migración
```bash
python manage.py makemigrations alumno
python manage.py migrate
```

#### 6. Configurar admin
- Registrar modelo con campos relacionados

### Archivos a crear/modificar
- `alumno/models.py` - Clase Alumno y señales
- `alumno/admin.py` - Configuración admin
- `myapp/settings.py` - INSTALLED_APPS

### Resultado esperado
Modelo Alumno funcional con composición Usuario, validaciones y asignación automática de grupos.