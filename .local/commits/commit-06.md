# Commit 06: Creación de la App Materia

## Responsable: Santiago

### Descripción
Crear la aplicación `materia` para gestionar las materias académicas asociadas a carreras.

### Tareas a realizar

#### 1. Crear la app materia
```bash
python manage.py startapp materia
```

#### 2. Implementar modelo Materia
- Crear clase `Materia` con campos:
  - `nombre` (CharField)
  - `codigo` (CharField con validación formato ABC123)
  - `carrera` (ForeignKey a Carrera)
  - `año` (PositiveIntegerField 1-6)
  - `cuatrimestre` (PositiveIntegerField con choices)
  - `cupo_maximo` (PositiveIntegerField 1-100, default 30)
  - `descripcion` (TextField opcional)
  - `activa` (BooleanField)
  - `fecha_creacion` (DateTimeField auto)
- Configurar `unique_together` para carrera y código
- Implementar método `clean()` para validaciones
- Añadir propiedades `cupo_disponible` y `inscriptos_count`

#### 3. Configurar en settings.py
- Agregar `'materia'` a `INSTALLED_APPS`

#### 4. Crear y aplicar migración
```bash
python manage.py makemigrations materia
python manage.py migrate
```

#### 5. Configurar admin
- Registrar modelo Materia en admin con filtros

### Archivos a crear/modificar
- `materia/models.py` - Clase Materia
- `materia/admin.py` - Configuración admin
- `myapp/settings.py` - INSTALLED_APPS

### Resultado esperado
Modelo Materia funcional con relación a Carrera y control de cupos, accesible desde admin.