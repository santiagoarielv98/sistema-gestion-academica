# Commit 10: Creación de la App Inscripción

## Responsable: Daiana

### Descripción
Crear la aplicación `inscripcion` para gestionar las inscripciones de alumnos a materias con control de cupos y validaciones.

### Tareas a realizar

#### 1. Crear la app inscripcion
```bash
python manage.py startapp inscripcion
```

#### 2. Implementar modelo Inscripcion
- Crear clase `Inscripcion` con campos:
  - `alumno` (ForeignKey a Alumno)
  - `materia` (ForeignKey a Materia)
  - `fecha_inscripcion` (DateTimeField auto)
  - `fecha_baja` (DateTimeField nullable)
  - `activa` (BooleanField)
  - `observaciones` (TextField opcional)
- Configurar `unique_together` para alumno y materia
- Implementar método `clean()` con validaciones:
  - Materia debe pertenecer a carrera del alumno
  - Verificar cupo disponible
- Implementar método `dar_de_baja()`

#### 3. Configurar en settings.py
- Agregar `'inscripcion'` a `INSTALLED_APPS`

#### 4. Crear y aplicar migración
```bash
python manage.py makemigrations inscripcion
python manage.py migrate
```

#### 5. Configurar admin
- Registrar modelo con filtros por carrera, materia y estado
- Mostrar información relevante en list_display

### Archivos a crear/modificar
- `inscripcion/models.py` - Clase Inscripcion
- `inscripcion/admin.py` - Configuración admin
- `myapp/settings.py` - INSTALLED_APPS

### Resultado esperado
Modelo Inscripcion funcional con validaciones de negocio, control de cupos y gestión de estados.