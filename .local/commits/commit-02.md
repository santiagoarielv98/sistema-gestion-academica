# Commit 02: Creación de la App Usuario

## Responsable: Jorge

### Descripción
Crear la aplicación `usuario` que manejará el sistema de autenticación personalizado basado en email y DNI.

### Tareas a realizar

#### 1. Crear la app usuario
```bash
python manage.py startapp usuario
```

#### 2. Implementar modelo Usuario personalizado
- Crear clase `Usuario` que herede de `AbstractUser`
- Configurar email como campo único y USERNAME_FIELD
- Agregar campo `username` como DNI con validación de 8 dígitos
- Agregar campo `primer_login` (boolean)
- Implementar métodos `__str__` y propiedad `rol`

#### 3. Configurar settings.py
- Agregar `'usuario'` a `INSTALLED_APPS`
- Configurar `AUTH_USER_MODEL = 'usuario.Usuario'`

#### 4. Crear y aplicar migración
```bash
python manage.py makemigrations usuario
python manage.py migrate
```

### Archivos a crear/modificar
- `usuario/models.py` - Clase Usuario
- `usuario/admin.py` - Configuración admin básica
- `myapp/settings.py` - AUTH_USER_MODEL

### Resultado esperado
Modelo de usuario personalizado funcionando con email como login y DNI como username.