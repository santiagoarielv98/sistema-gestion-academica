# Commit 14: Vistas Públicas y Consultas

## Responsable: Lourdes

### Descripción
Implementar las vistas públicas del sistema que permiten consultar información sin autenticación.

### Tareas a realizar

#### 1. Crear vistas públicas
- Implementar `CarrerasPublicasView` en `gestion_academica/views.py`
- Implementar `MateriasPublicasView` - lista todas las materias activas
- Implementar `ConsultasCarreraView` - materias por carrera específica
- Implementar `ConsultasMateriaView` - detalles de materia específica
- Implementar `MateriasConCupoView` - solo materias con cupo disponible

#### 2. Crear formularios de consulta pública
- Ampliar `FiltroMateriaForm` para vistas públicas
- Filtros por carrera, año, cuatrimestre
- Búsqueda por nombre de materia

#### 3. Crear templates públicos
- `templates/gestion_academica/publico/carreras.html`
- `templates/gestion_academica/publico/materias.html`
- `templates/gestion_academica/publico/consultas_carrera.html`
- `templates/gestion_academica/publico/consultas_materia.html`
- `templates/gestion_academica/publico/materias_con_cupo.html`

#### 4. Agregar URLs públicas
- Actualizar `gestion_academica/urls.py` con rutas públicas
- Configurar namespace para vistas públicas
- URLs amigables para SEO

#### 5. Mejorar navegación
- Actualizar template base con menú público
- Links a vistas públicas desde la home

### Archivos a crear/modificar
- `gestion_academica/views.py` - Vistas públicas
- `gestion_academica/urls.py` - URLs públicas
- Templates en `gestion_academica/publico/`
- `templates/gestion_academica/base.html` - Navegación

### Resultado esperado
Sistema de consultas públicas funcional que permite ver carreras, materias y cupos sin necesidad de login.