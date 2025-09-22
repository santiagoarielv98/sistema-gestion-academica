# Commit 12: Creación de la App Gestión Académica

## Responsable: Jorge

### Descripción
Crear la aplicación central `gestion_academica` que agrupa funcionalidades transversales, dashboard y vistas públicas.

### Tareas a realizar

#### 1. Crear la app gestion_academica
```bash
python manage.py startapp gestion_academica
```

#### 2. Implementar servicios de reportes
- Crear `ReportesService` en `gestion_academica/services.py`
- Método `obtener_estadisticas_dashboard()`
- Método `obtener_resumen_inscripciones()`
- Método `obtener_materias_con_cupo_disponible()`
- Servicios de consultas agregadas

#### 3. Crear formularios de filtros
- Implementar `FiltroMateriaForm` en `gestion_academica/forms.py`
- Formularios para filtros avanzados en consultas públicas
- Validaciones para rangos de fechas y parámetros

#### 4. Configurar en settings.py
- Agregar `'gestion_academica'` a `INSTALLED_APPS`
- Configurar widget_tweaks para formularios mejorados

#### 5. Crear estructura base de templates
- Crear `templates/gestion_academica/base.html`
- Template base con navegación y estilos
- Incluir CDN de Bootstrap o CSS personalizado

#### 6. Aplicar migración (si es necesaria)
```bash
python manage.py migrate
```

### Archivos a crear/modificar
- `gestion_academica/services.py` - Servicios de reportes
- `gestion_academica/forms.py` - Formularios de filtros
- `templates/gestion_academica/base.html` - Template base
- `myapp/settings.py` - INSTALLED_APPS y widget_tweaks

### Resultado esperado
App central configurada con servicios de reportes y estructura base de templates.