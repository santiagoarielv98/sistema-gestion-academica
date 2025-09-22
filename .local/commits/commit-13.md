# Commit 13: Dashboard y Vistas del Sistema

## Responsable: Paula

### Descripción
Implementar el dashboard principal y vistas centrales del sistema de gestión académica.

### Tareas a realizar

#### 1. Crear vista Dashboard
- Implementar `DashboardView` en `gestion_academica/views.py`
- Mostrar estadísticas según rol del usuario
- Redirigir automáticamente si primer_login es True
- Contexto diferenciado para administrador vs alumno

#### 2. Crear vistas de cambio de contraseña
- `CambiarPasswordView` - cambio general
- Integración con formularios de Django Auth
- Actualizar sesión después del cambio
- Mensajes de confirmación apropiados

#### 3. Crear vistas para alumnos
- `MisMateriasView` - materias del alumno logueado
- `OfertaAcademicaView` - materias disponibles para inscripción
- Filtros por cuatrimestre y año

#### 4. Crear templates del sistema
- `templates/gestion_academica/dashboard.html`
- `templates/gestion_academica/alumno/mis_materias.html`
- `templates/gestion_academica/alumno/oferta_academica.html`
- `templates/gestion_academica/auth/cambiar_password.html`

#### 5. Configurar URLs principales
- Crear `gestion_academica/urls.py`
- Configurar `myapp/urls.py` como incluir todas las apps
- Ruta raíz que redirija a dashboard

### Archivos a crear/modificar
- `gestion_academica/views.py` - Dashboard y vistas centrales
- `gestion_academica/urls.py` - URLs principales
- `myapp/urls.py` - Incluir todas las apps
- Templates del dashboard y vistas de alumno

### Resultado esperado
Dashboard funcional con información específica por rol y vistas para alumnos.