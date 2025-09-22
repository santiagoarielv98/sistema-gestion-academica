# Commit 04: Creación de la App Carrera

## Responsable: Lourdes

### Descripción
Crear la aplicación `carrera` para gestionar las carreras académicas de la institución.

### Tareas a realizar

#### 1. Crear la app carrera
```bash
python manage.py startapp carrera
```

#### 2. Implementar modelo Carrera
- Crear clase `Carrera` con campos:
  - `nombre` (CharField único)
  - `codigo` (CharField con validación formato AA1234)
  - `descripcion` (TextField opcional)
  - `duracion_años` (PositiveIntegerField con validación 1-10)
  - `activa` (BooleanField)
  - `fecha_creacion` (DateTimeField auto)
- Implementar método `clean()` para validaciones
- Implementar método `delete()` personalizado
- Configurar Meta class con ordenamiento

#### 3. Configurar en settings.py
- Agregar `'carrera'` a `INSTALLED_APPS`

#### 4. Crear y aplicar migración
```bash
python manage.py makemigrations carrera
python manage.py migrate
```

#### 5. Configurar admin básico
- Registrar modelo Carrera en admin
- Configurar campos a mostrar

### Archivos a crear/modificar
- `carrera/models.py` - Clase Carrera
- `carrera/admin.py` - Configuración admin
- `myapp/settings.py` - INSTALLED_APPS

### Resultado esperado
Modelo Carrera funcional con validaciones, accesible desde el admin de Django.