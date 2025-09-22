# Commit 09: CRUD de Alumnos y Servicios

## Responsable: Lourdes

### Descripción
Implementar el sistema completo CRUD para alumnos con servicios especializados y validaciones de negocio.

### Tareas a realizar

#### 1. Crear formularios para Alumno
- Implementar `AlumnoForm` en `alumno/forms.py`
- Incluir campos de Usuario y Alumno en un solo formulario
- Validaciones personalizadas para email único y legajo
- Widget personalizado para contraseña

#### 2. Crear servicios de Alumno
- Implementar `AlumnoService` en `alumno/services.py`
- Método `crear_alumno_completo()` - maneja Usuario y Alumno
- Método `obtener_alumnos_por_carrera()`
- Método `generar_legajo_automatico()`
- Validaciones de negocio complejas

#### 3. Crear vistas CRUD especializadas
- `AlumnoListView` con filtros por carrera y estado
- `AlumnoDetailView` con información completa
- `AlumnoCreateView` que maneja Usuario + Alumno
- `AlumnoUpdateView` con lógica especial
- `AlumnoDeleteView` con validaciones
- Aplicar `AdminRequiredMixin`

#### 4. Crear templates
- `templates/gestion_academica/alumnos/list.html`
- `templates/gestion_academica/alumnos/detail.html`
- `templates/gestion_academica/alumnos/form.html`
- `templates/gestion_academica/alumnos/confirm_delete.html`

#### 5. Configurar URLs
- Crear `alumno/urls.py` con rutas completas
- Incluir en URLs principales

### Archivos a crear/modificar
- `alumno/forms.py` - Formularios complejos
- `alumno/views.py` - Vistas CRUD especializadas
- `alumno/services.py` - Lógica de negocio
- `alumno/urls.py` - URLs
- Templates en `gestion_academica/alumnos/`

### Resultado esperado
CRUD completo de alumnos que maneja tanto datos de Usuario como de Alumno, con validaciones robustas.