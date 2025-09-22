# Commit 07: CRUD de Materias y Servicios

## Responsable: Jorge

### Descripción
Implementar el sistema completo CRUD para materias con servicios de negocio y validaciones avanzadas.

### Tareas a realizar

#### 1. Crear formularios para Materia
- Implementar `MateriaForm` en `materia/forms.py`
- Filtrar carreras activas en el dropdown
- Validaciones personalizadas de código por carrera

#### 2. Crear servicios de Materia
- Implementar `MateriaService` en `materia/services.py`
- Método `obtener_materias_con_cupo_disponible()`
- Método `obtener_materias_por_carrera(año, cuatrimestre)`
- Método `filtrar_materias(filtros)`
- Validaciones de negocio para creación/edición

#### 3. Crear vistas CRUD
- `MateriaListView` con filtros por carrera, año, cuatrimestre
- `MateriaDetailView` 
- `MateriaCreateView`
- `MateriaUpdateView`
- `MateriaDeleteView`
- Aplicar `AdminRequiredMixin`

#### 4. Crear templates
- `templates/gestion_academica/materias/list.html`
- `templates/gestion_academica/materias/form.html`
- `templates/gestion_academica/materias/confirm_delete.html`

#### 5. Configurar URLs
- Crear `materia/urls.py`
- Incluir en URLs principales

### Archivos a crear/modificar
- `materia/forms.py` - Formularios
- `materia/views.py` - Vistas CRUD
- `materia/services.py` - Lógica de negocio
- `materia/urls.py` - URLs
- Templates en `gestion_academica/materias/`

### Resultado esperado
CRUD de materias con filtros avanzados, validaciones de negocio y control de cupos.