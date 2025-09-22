# Commit 05: CRUD de Carreras con Views y Templates

## Responsable: Daiana

### Descripción
Implementar el sistema completo CRUD para carreras con vistas basadas en clases, formularios y templates.

### Tareas a realizar

#### 1. Crear formularios para Carrera
- Implementar `CarreraForm` en `carrera/forms.py`
- Configurar widgets y validaciones personalizadas
- Añadir clases CSS para styling

#### 2. Crear vistas basadas en clases
- `CarreraListView` - Lista todas las carreras
- `CarreraDetailView` - Detalle de carrera específica  
- `CarreraCreateView` - Crear nueva carrera
- `CarreraUpdateView` - Editar carrera existente
- `CarreraDeleteView` - Eliminar carrera
- Aplicar `AdminRequiredMixin` donde corresponda

#### 3. Crear servicios de Carrera
- Implementar `CarreraService` en `carrera/services.py`
- Métodos para validaciones de negocio
- Manejo de exceptions personalizadas

#### 4. Crear templates
- `templates/gestion_academica/carreras/list.html`
- `templates/gestion_academica/carreras/form.html`
- `templates/gestion_academica/carreras/confirm_delete.html`

#### 5. Configurar URLs
- Crear `carrera/urls.py` con todas las rutas CRUD
- Incluir en `myapp/urls.py`

### Archivos a crear/modificar
- `carrera/forms.py` - Formularios
- `carrera/views.py` - Vistas CRUD
- `carrera/services.py` - Lógica de negocio
- `carrera/urls.py` - URLs
- Templates en `gestion_academica/carreras/`

### Resultado esperado
CRUD completo de carreras accesible vía web, con validaciones y control de acceso por roles.