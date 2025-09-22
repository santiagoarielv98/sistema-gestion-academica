# Commit 01: Inicialización del Proyecto Django

## Responsable: Santiago

### Descripción
Inicializar el proyecto Django con la configuración básica y estructura de directorios.

### Tareas a realizar

#### 1. Crear el proyecto Django
```bash
django-admin startproject myapp
cd myapp
```

#### 2. Configurar settings.py básico
- Configurar `INSTALLED_APPS` con apps de Django por defecto
- Configurar base de datos SQLite
- Configurar idioma español (`LANGUAGE_CODE = 'es-ar'`)
- Configurar zona horaria Argentina (`TIME_ZONE = 'America/Argentina/Buenos_Aires'`)

#### 3. Crear estructura de directorios
- Crear directorio `templates` en la raíz del proyecto
- Configurar `DIRS` en `TEMPLATES` para apuntar a este directorio

#### 4. Verificar instalación
```bash
python manage.py runserver
```

### Archivos modificados
- `myapp/settings.py`
- `manage.py` (creado automáticamente)

### Resultado esperado
Proyecto Django funcional que responda en http://127.0.0.1:8000/ con la página de bienvenida.