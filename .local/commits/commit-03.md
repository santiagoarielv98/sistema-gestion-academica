# Commit 03: Implementación de Vistas de Autenticación

## Responsable: Paula

### Descripción
Crear el sistema de login, logout y cambio de contraseña para usuarios con primer login.

### Tareas a realizar

#### 1. Crear formularios de autenticación
- Implementar `CustomAuthenticationForm` en `usuario/forms.py`
- Crear formulario para cambio de contraseña en primer login
- Validaciones personalizadas para email y contraseña

#### 2. Crear vistas de autenticación
- `LoginView` personalizada
- `LogoutView` personalizada  
- `CambiarPasswordView` para primer login
- `CambiarPasswordGeneralView` para cambios posteriores

#### 3. Crear mixins de autorización
- `AdminRequiredMixin` - Solo administradores
- `AlumnoRequiredMixin` - Solo alumnos

#### 4. Crear templates de autenticación
- `templates/gestion_academica/auth/login.html`
- `templates/gestion_academica/auth/cambiar_password_primer_login.html`
- `templates/gestion_academica/auth/cambiar_password.html`

#### 5. Configurar URLs
- Crear `usuario/urls.py` con rutas de autenticación
- Incluir URLs en `myapp/urls.py`

### Archivos a crear/modificar
- `usuario/forms.py` - Formularios de autenticación
- `usuario/views.py` - Vistas de login/logout
- `usuario/urls.py` - URLs de autenticación
- Templates en `gestion_academica/auth/`

### Resultado esperado
Sistema de login funcional con email, cambio de contraseña obligatorio en primer login y control de acceso por roles.