# Solución para las rutas de cambio de contraseña

## Problema actual
Tienes dos vistas para cambiar contraseña que se superponen y causan confusión:
- `CambiarPasswordView` (usuario/views.py) - solo primer login
- `CambiarPasswordPrimerLoginView` (gestion_academica/views.py) - también primer login
- No hay una vista para cambio de contraseña general (cuando el usuario ya completó el primer login)

## Solución propuesta

### 1. Mantener solo UNA vista para primer login
**Ubicación:** `gestion_academica/views.py`
**Ruta:** `/cambiar-password-primer-login/`
**Propósito:** Solo para alumnos en su primer login

### 2. Crear/Modificar vista para cambio general
**Ubicación:** `usuario/views.py` 
**Ruta:** `/cambiar-password/`
**Propósito:** Para cualquier usuario autenticado que quiera cambiar su contraseña

### 3. Flujo de usuario claro:

#### Primer login (solo alumnos):
1. Alumno hace login → LoginView detecta `primer_login=True`
2. Redirecciona a `/cambiar-password-primer-login/`
3. Alumno cambia contraseña → se marca `primer_login=False`
4. Redirecciona al dashboard

#### Cambio de contraseña posterior:
1. Usuario autenticado va a `/cambiar-password/`
2. Cambia su contraseña sin restricciones
3. Permanece en la misma sesión

## Archivos a modificar:

### 1. `usuario/views.py`
- Eliminar restricción `primer_login` de `CambiarPasswordView`
- Permitir que cualquier usuario autenticado cambie su contraseña

### 2. `usuario/urls.py`  
- La ruta `cambiar-password/` debe ser para cambio general

### 3. `gestion_academica/views.py`
- Mantener `CambiarPasswordPrimerLoginView` solo para primer login

### 4. Templates
- `cambiar_password.html` → Para cambio general
- `cambiar_password_primer_login.html` → Para primer login (ya existe)

## Beneficios:
- ✅ Separación clara de responsabilidades
- ✅ Flujo de usuario intuitivo
- ✅ Sin duplicación de código
- ✅ Fácil mantenimiento
- ✅ Mejor experiencia de usuario