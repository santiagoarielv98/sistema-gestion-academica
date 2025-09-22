# Commit 11: Sistema de Inscripciones con Servicios

## Responsable: Santiago

### Descripción
Implementar el sistema completo de inscripciones con servicios especializados, validaciones de negocio y manejo de cupos.

### Tareas a realizar

#### 1. Crear servicios de Inscripción
- Implementar `InscripcionService` en `inscripcion/services.py`
- Método `inscribir_alumno(alumno, materia)` con validaciones
- Método `dar_de_baja_inscripcion(inscripcion)`
- Método `verificar_cupo_disponible(materia)`
- Método `obtener_inscripciones_activas_por_alumno()`
- Método `obtener_inscripciones_por_materia()`
- Manejo de excepciones personalizadas

#### 2. Crear formularios para Inscripción
- Implementar `InscripcionForm` en `inscripcion/forms.py`
- Filtrar materias según carrera del alumno
- Validaciones dinámicas de cupo
- Formulario de baja con observaciones

#### 3. Crear vistas especializadas
- `InscripcionCreateView` - Nueva inscripción
- `InscripcionListView` - Lista con filtros
- `InscripcionDeleteView` - Dar de baja (no eliminar)
- `InscripcionReactivarView` - Reactivar inscripción
- Aplicar mixins de autorización apropiados

#### 4. Crear templates
- `templates/gestion_academica/inscripciones/form.html`
- `templates/gestion_academica/inscripciones/list.html`
- Incluir información de cupos disponibles

#### 5. Configurar URLs
- Crear `inscripcion/urls.py`
- Incluir en URLs principales

### Archivos a crear/modificar
- `inscripcion/services.py` - Lógica compleja de negocio
- `inscripcion/forms.py` - Formularios con validaciones
- `inscripcion/views.py` - Vistas especializadas
- `inscripcion/urls.py` - URLs
- Templates en `gestion_academica/inscripciones/`

### Resultado esperado
Sistema completo de inscripciones con control automático de cupos, validaciones robustas y manejo de estados.